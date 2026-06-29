from pathlib import Path

import numpy as np

from iceye_ai_engineer.part2_blob_boxes import compute_rotated_boxes, write_boxes_csv


def test_part2_finds_two_blobs_and_writes_required_csv_header(tmp_path: Path) -> None:
    # Arrange: create two disconnected blobs in a small deterministic mask.
    # This keeps the test focused on blob detection and export behavior.
    mask = np.zeros((8, 8), dtype=np.uint8)
    mask[1:3, 1:4] = 1
    mask[5:7, 5:7] = 1

    # Act: compute rotated boxes from the binary mask.
    boxes = compute_rotated_boxes(mask.astype(bool))

    # Assert: both disconnected blobs are detected and assigned stable IDs.
    assert len(boxes) == 2
    assert [box.blob_id for box in boxes] == [1, 2]

    # Assert: each detected blob has a valid box shape.
    # Exact floating-point geometry is intentionally not asserted here because
    # this test checks structural correctness, not every rotation calculation.
    assert all(box.width > 0 for box in boxes)
    assert all(box.height > 0 for box in boxes)

    # Act: write the computed boxes to the required CSV output format.
    output_path = write_boxes_csv(boxes, tmp_path / "blob_bounding_boxes.csv")
    csv_text = output_path.read_text(encoding="utf-8")
    csv_lines = csv_text.splitlines()

    # Assert: the CSV export keeps the required filename, header, and row count.
    assert output_path.name == "blob_bounding_boxes.csv"
    assert csv_lines[0] == "blob_id,center_x,center_y,width,height,angle"
    assert len(csv_lines) == 3
