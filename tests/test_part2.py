from pathlib import Path

import numpy as np

from iceye_ai_engineer.part2_blob_boxes import compute_rotated_boxes, write_boxes_csv


def test_part2_computes_two_boxes_and_writes_csv(tmp_path: Path) -> None:
    mask = np.zeros((8, 8), dtype=np.uint8)
    mask[1:3, 1:4] = 1
    mask[5:7, 5:7] = 1

    boxes = compute_rotated_boxes(mask.astype(bool))

    assert len(boxes) == 2
    assert [box.blob_id for box in boxes] == [1, 2]
    assert all(box.width > 0 for box in boxes)
    assert all(box.height > 0 for box in boxes)

    output_path = write_boxes_csv(boxes, tmp_path / "blob_bounding_boxes.csv")
    csv_text = output_path.read_text(encoding="utf-8")

    assert output_path.name == "blob_bounding_boxes.csv"
    assert csv_text.splitlines()[0] == "blob_id,center_x,center_y,width,height,angle"
