from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

from pydantic import BaseModel
from pydantic_ai import Agent
from pydantic_ai.messages import ModelMessage, ModelResponse, TextPart, UserPromptPart
from pydantic_ai.models.function import FunctionModel

from iceye_ai_engineer.part1_ingest import EntityStore


class NamedEntityAnswer(BaseModel):
    entity: str
    label: str | None


class ChatbotOutput(BaseModel):
    reply: str
    entities: list[NamedEntityAnswer]


def normalize_entity_text(value: str) -> str:
    return " ".join(value.split())


def load_entity_store(store_path: Path) -> EntityStore:
    return EntityStore.model_validate_json(store_path.read_text(encoding="utf-8"))


def build_unique_entities(store: EntityStore) -> list[NamedEntityAnswer]:
    unique_entities: dict[tuple[str, str | None], NamedEntityAnswer] = {}
    for entity in store.entities:
        normalized_text = normalize_entity_text(entity.text)
        key = (normalized_text, entity.label)
        unique_entities.setdefault(key, NamedEntityAnswer(entity=normalized_text, label=entity.label))
    return sorted(unique_entities.values(), key=lambda item: (item.entity.lower(), item.label or ""))


def extract_user_question(messages: list[ModelMessage]) -> str:
    for message in reversed(messages):
        parts = getattr(message, "parts", [])
        for part in parts:
            if isinstance(part, UserPromptPart):
                if isinstance(part.content, str):
                    return part.content
    raise ValueError("No user question found")


def build_reply(question: str, store: EntityStore, unique_entities: list[NamedEntityAnswer]) -> str:
    normalized_question = question.casefold()
    mention_counts = Counter(normalize_entity_text(entity.text).casefold() for entity in store.entities)

    for entity in unique_entities:
        entity_name = entity.entity.casefold()
        if entity_name and entity_name in normalized_question:
            count = mention_counts[entity_name]
            return f"I checked the stored entity file for '{question}' and found {count} mention(s) of {entity.entity}."

    return (
        f"I checked the stored entity file for '{question}'. "
        f"I can return the unique named entities and their labels from the persisted extraction results."
    )


def build_chatbot_agent(store: EntityStore) -> Agent[None, ChatbotOutput]:
    unique_entities = build_unique_entities(store)

    def respond(messages: list[ModelMessage], _info: object) -> ModelResponse:
        question = extract_user_question(messages)
        payload = ChatbotOutput(
            reply=build_reply(question=question, store=store, unique_entities=unique_entities),
            entities=unique_entities,
        )
        return ModelResponse(parts=[TextPart(content=payload.model_dump_json())])

    return Agent(
        FunctionModel(respond, model_name="part1-entity-chatbot"),
        output_type=ChatbotOutput,
        instructions=(
            "Answer using only the stored entity data loaded by the application. "
            "Return the required structured output."
        ),
    )


def build_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("entity_store_path", type=Path)
    parser.add_argument("question")
    return parser


def main() -> int:
    args = build_argument_parser().parse_args()
    store = load_entity_store(args.entity_store_path)
    result = build_chatbot_agent(store).run_sync(args.question)
    print(json.dumps(result.output.model_dump(), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())