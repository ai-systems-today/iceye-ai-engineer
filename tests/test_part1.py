from iceye_ai_engineer.part1_chatbot import build_reply, build_unique_entities
from iceye_ai_engineer.part1_ingest import EntityStore, ExtractedEntity


def test_part1_entity_store_drives_unique_entities_and_reply() -> None:
    store = EntityStore(
        document_path="sample.pdf",
        labels=["person"],
        entities=[
            ExtractedEntity(
                text="AI Engineer",
                label="person",
                start=0,
                end=11,
                left_context="",
                right_context="technical homework",
            ),
            ExtractedEntity(
                text="AI\nEngineer",
                label="person",
                start=20,
                end=31,
                left_context="forward deployed",
                right_context="role",
            ),
            ExtractedEntity(
                text="Candidates",
                label="person",
                start=40,
                end=50,
                left_context="",
                right_context="are expected",
            ),
        ],
    )

    unique_entities = build_unique_entities(store)

    assert [(item.entity, item.label) for item in unique_entities] == [
        ("AI Engineer", "person"),
        ("Candidates", "person"),
    ]

    reply = build_reply(
        question="How many mentions of AI Engineer are in the doc?",
        store=store,
        unique_entities=unique_entities,
    )

    assert "2 mention(s) of AI Engineer" in reply
