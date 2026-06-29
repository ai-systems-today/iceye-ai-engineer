from __future__ import annotations

import argparse
import csv
from collections import deque
from dataclasses import dataclass
from pathlib import Path

import numpy as np


OUTPUT_FILENAME = "blob_bounding_boxes.csv"


@dataclass(frozen=True)
class RotatedBox:
    blob_id: int
    center_x: float
    center_y: float
    width: float
    height: float
    angle: float


def load_mask(mask_path: Path) -> np.ndarray:
    mask = np.load(mask_path)
    if mask.ndim != 2:
        raise ValueError("Input mask must be a 2D NumPy array")
    binary_mask = mask.astype(bool)
    if not np.any(binary_mask):
        raise ValueError("Input mask must contain at least one blob")
    return binary_mask


def find_connected_components(mask: np.ndarray) -> list[np.ndarray]:
    visited = np.zeros_like(mask, dtype=bool)
    components: list[np.ndarray] = []
    height, width = mask.shape

    for row in range(height):
        for col in range(width):
            if not mask[row, col] or visited[row, col]:
                continue

            queue: deque[tuple[int, int]] = deque([(row, col)])
            visited[row, col] = True
            pixels: list[tuple[int, int]] = []

            while queue:
                current_row, current_col = queue.popleft()
                pixels.append((current_row, current_col))

                for row_offset in (-1, 0, 1):
                    for col_offset in (-1, 0, 1):
                        if row_offset == 0 and col_offset == 0:
                            continue
                        next_row = current_row + row_offset
                        next_col = current_col + col_offset
                        if not (0 <= next_row < height and 0 <= next_col < width):
                            continue
                        if visited[next_row, next_col] or not mask[next_row, next_col]:
                            continue
                        visited[next_row, next_col] = True
                        queue.append((next_row, next_col))

            components.append(np.asarray(pixels, dtype=float))

    return components


def rotation_matrix(angle_degrees: float) -> np.ndarray:
    angle_radians = np.deg2rad(angle_degrees)
    cos_angle = np.cos(angle_radians)
    sin_angle = np.sin(angle_radians)
    return np.array([[cos_angle, -sin_angle], [sin_angle, cos_angle]], dtype=float)


def box_for_angle(component_pixels: np.ndarray, angle_degrees: float) -> tuple[float, float, float, float, float]:
    xy_pixels = np.stack([component_pixels[:, 1], component_pixels[:, 0]], axis=1)
    rotated = xy_pixels @ rotation_matrix(-angle_degrees).T
    min_x, min_y = rotated.min(axis=0)
    max_x, max_y = rotated.max(axis=0)

    width = float(max_x - min_x + 1.0)
    height = float(max_y - min_y + 1.0)
    center_rotated = np.array([(min_x + max_x) / 2.0, (min_y + max_y) / 2.0], dtype=float)
    center = center_rotated @ rotation_matrix(angle_degrees).T

    return float(center[0]), float(center[1]), width, height, width * height


def refine_best_angle(component_pixels: np.ndarray) -> tuple[float, float, float, float]:
    best_angle = 0.0
    best_center_x = 0.0
    best_center_y = 0.0
    best_width = 0.0
    best_height = 0.0
    best_area = float("inf")

    angle_candidates = np.linspace(-90.0, 89.0, 180)
    for angle in angle_candidates:
        center_x, center_y, width, height, area = box_for_angle(component_pixels, float(angle))
        if area < best_area:
            best_angle = float(angle)
            best_center_x = center_x
            best_center_y = center_y
            best_width = width
            best_height = height
            best_area = area

    for step in (0.5, 0.1):
        candidate_angles = np.arange(best_angle - step, best_angle + step + step, step)
        for angle in candidate_angles:
            bounded_angle = ((angle + 90.0) % 180.0) - 90.0
            center_x, center_y, width, height, area = box_for_angle(component_pixels, float(bounded_angle))
            if area < best_area:
                best_angle = float(bounded_angle)
                best_center_x = center_x
                best_center_y = center_y
                best_width = width
                best_height = height
                best_area = area

    return best_center_x, best_center_y, best_width, best_height, best_angle


def compute_rotated_boxes(mask: np.ndarray) -> list[RotatedBox]:
    components = find_connected_components(mask)
    boxes: list[RotatedBox] = []

    for blob_id, component_pixels in enumerate(components, start=1):
        center_x, center_y, width, height, angle = refine_best_angle(component_pixels)
        boxes.append(
            RotatedBox(
                blob_id=blob_id,
                center_x=center_x,
                center_y=center_y,
                width=width,
                height=height,
                angle=angle,
            )
        )

    return boxes


def write_boxes_csv(boxes: list[RotatedBox], output_path: Path) -> Path:
    with output_path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(
            csv_file,
            fieldnames=["blob_id", "center_x", "center_y", "width", "height", "angle"],
        )
        writer.writeheader()
        for box in boxes:
            writer.writerow(
                {
                    "blob_id": box.blob_id,
                    "center_x": box.center_x,
                    "center_y": box.center_y,
                    "width": box.width,
                    "height": box.height,
                    "angle": box.angle,
                }
            )
    return output_path


def build_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("mask_path", type=Path)
    return parser


def main() -> int:
    args = build_argument_parser().parse_args()
    mask = load_mask(args.mask_path)
    boxes = compute_rotated_boxes(mask)
    output_path = write_boxes_csv(boxes, Path(OUTPUT_FILENAME))
    print(output_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())