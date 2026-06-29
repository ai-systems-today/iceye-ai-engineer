from iceye_ai_engineer.part1_chatbot import build_reply, build_unique_entities
from iceye_ai_engineer.part1_ingest import EntityStore, ExtractedEntity


def test_part1_merges_whitespace_variants_and_counts_mentions() -> None:
    # Arrange: build a minimal in-memory store.
    # "AI Engineer" appears twice with different whitespace, while "Candidates"
    # is a separate control entity that should remain unique.
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

    # Act: derive the user-facing unique entity list from the stored entities.
    unique_entities = build_unique_entities(store)

    # Assert: whitespace variants are normalized into one displayed entity,
    # while the unrelated control entity is preserved.
    assert len(unique_entities) == 2
    assert any(item.entity == "AI Engineer" and item.label == "person" for item in unique_entities)
    assert any(item.entity == "Candidates" and item.label == "person" for item in unique_entities)

    # Act: ask the chatbot a count question using the already-extracted store.
    reply = build_reply(
        question="How many mentions of AI Engineer are in the doc?",
        store=store,
        unique_entities=unique_entities,
    )

    # Assert: the answer is based on stored entity occurrences, not PDF re-reading.
    assert "2 mention(s) of AI Engineer" in reply
