from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Sequence

from pydantic import BaseModel, Field
from glinker.l1.component import L1GlinerComponent
from glinker.l1.models import L1GlinerConfig
from kreuzberg import extract_file_sync


DEFAULT_GLINER_MODEL = "urchade/gliner_small-v2.1"


class ExtractedEntity(BaseModel):
    text: str
    label: str | None
    start: int
    end: int
    left_context: str
    right_context: str


class EntityStore(BaseModel):
    document_path: str
    labels: list[str]
    entities: list[ExtractedEntity]


def extract_document_text(document_path: Path) -> str:
    result = extract_file_sync(document_path)
    if not result.content.strip():
        raise ValueError(f"No text extracted from {document_path}")
    return result.content


def detect_entities(text: str, labels: Sequence[str], model: str) -> list[ExtractedEntity]:
    component = L1GlinerComponent(
        L1GlinerConfig(
            model=model,
            labels=list(labels),
            device="cpu",
            threshold=0.3,
            flat_ner=True,
            multi_label=False,
        )
    )
    entities = component.extract_entities(text)
    return [ExtractedEntity.model_validate(entity.model_dump()) for entity in entities]


def persist_entities(document_path: Path, labels: Sequence[str], entities: Sequence[ExtractedEntity], output_path: Path) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    store = EntityStore(
        document_path=str(document_path),
        labels=list(labels),
        entities=list(entities),
    )
    output_path.write_text(store.model_dump_json(indent=2), encoding="utf-8")
    return output_path


def build_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("document_path", type=Path)
    parser.add_argument("labels", nargs="+", help="Entity labels for GLiNER extraction")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("data") / "part1_entities.json",
        help="Path for the persisted entity JSON file",
    )
    parser.add_argument(
        "--model",
        default=DEFAULT_GLINER_MODEL,
        help="GLiNER model identifier; defaults to the documented small model",
    )
    return parser


def main() -> int:
    args = build_argument_parser().parse_args()
    text = extract_document_text(args.document_path)
    entities = detect_entities(text=text, labels=args.labels, model=args.model)
    output_path = persist_entities(
        document_path=args.document_path,
        labels=args.labels,
        entities=entities,
        output_path=args.output,
    )
    print(output_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())