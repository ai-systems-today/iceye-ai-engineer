# AI Engineer Technical Homework Task

This repository is being implemented strictly against [AI Engineer Technical Homework Task.pdf](AI%20Engineer%20Technical%20Homework%20Task.pdf).

## Scope

The PDF is the governing brief for this repository.

What has been implemented in this session:

- Part 1 document ingestion with `kreuzberg`
- Part 1 named entity detection with `glinker`
- Part 1 local entity persistence to JSON
- Part 1 single-turn CLI chatbot using Pydantic AI and answering only from the stored entity file
- Part 2 connected-component blob detection from a 2D NumPy binary mask
- Part 2 rotated bounding box CSV generation

What has been completed for delivery packaging in this session:

- Created the current-state archive [iceye-ai-engineer-current-state.zip](iceye-ai-engineer-current-state.zip)

## Phase Status

This repository was executed against the original 11-phase implementation plan derived from [AI Engineer Technical Homework Task.pdf](AI%20Engineer%20Technical%20Homework%20Task.pdf).

1. Repository skeleton: done
2. Exact dependency pinning: done
3. Part 1 ingestion with `kreuzberg` then `glinker`: done
4. Part 1 structured Pydantic output model: done
5. Part 1 single-turn chatbot logic using only stored entities: done
6. Part 2 blob identification from a 2D NumPy mask: done
7. Part 2 rotated rectangle computation: done
8. Part 2 CSV output generation: done
9. One unit test per task in [tests](tests): done
10. README with install, execute, and test guidance: done
11. Final compliance verification: done

Why the final three phases are now marked done:

- Phase 9 is done because the repository now contains one focused unit test for Part 1 and one focused unit test for Part 2 under [tests](tests).
- Phase 10 is done because install, execute, and test instructions are now all documented.
- Phase 11 is done because the implementation, tests, and delivery archive have all been validated in this session.

## Session Trace

This section records the work completed from the beginning of the session.

1. Read [AI Engineer Technical Homework Task.pdf](AI%20Engineer%20Technical%20Homework%20Task.pdf) and extracted the task requirements.
2. Confirmed the workspace initially contained only the PDF and a Git repository.
3. Checked Python availability and found that the pre-existing local virtual environment was initially Python 3.14, which is not allowed by the PDF.
4. Verified that Python 3.12 was installed on the machine and used that interpreter for the compliant project setup.
5. Installed `uv` with Python 3.12 because the PDF requires a `uv`-based workflow.
6. Created the initial repository skeleton with [pyproject.toml](pyproject.toml), [README.md](README.md), [REQUIREMENTS_TRACE.md](REQUIREMENTS_TRACE.md), and [tests](tests).
7. Pinned all declared dependencies to exact versions and constrained the project to Python 3.12.
8. Validated the project setup with `py -3.12 -m uv sync`.
9. Implemented Part 1 ingestion in [iceye_ai_engineer/part1_ingest.py](iceye_ai_engineer/part1_ingest.py).
10. Validated that Part 1 extraction runs with `kreuzberg` first, then entity detection with `glinker`, and persists entities locally to [data/part1_entities.json](data/part1_entities.json).
11. Implemented the single-turn Part 1 chatbot in [iceye_ai_engineer/part1_chatbot.py](iceye_ai_engineer/part1_chatbot.py).
12. Validated that the chatbot reads only the stored entity file and returns structured output with a conversational reply, unique entities, and labels.
13. Implemented Part 2 blob processing in [iceye_ai_engineer/part2_blob_boxes.py](iceye_ai_engineer/part2_blob_boxes.py).
14. Validated that Part 2 accepts a 2D NumPy binary mask, identifies connected blobs, computes rotated bounding boxes, and writes `blob_bounding_boxes.csv` with the required columns.
15. Revalidated the repository after implementation with `py -3.12 -m uv sync`.
16. Added [tests/test_part1.py](tests/test_part1.py) to verify normalized unique entity output and question-based mention counting.
17. Added [tests/test_part2.py](tests/test_part2.py) to verify two-blob detection and CSV writing.
18. Added [iceye_ai_engineer/__init__.py](iceye_ai_engineer/__init__.py) so the application package imports cleanly during test collection.
19. Added [tests/conftest.py](tests/conftest.py) so `pytest` collects tests with the repository root on `sys.path`.
20. Validated the tests with `uv run pytest`.

## Environment

Validated environment for the implemented solution:

- Python: 3.12.10
- Project environment: `.venv`
- Setup command: `uv sync`

The repository was validated using Python 3.12 because the PDF allows only Python 3.12 or 3.13.

## Install

```powershell
uv sync
```

This is the required setup command for the repository state produced in this session.

## Files Added In This Session

- [pyproject.toml](pyproject.toml)
- [REQUIREMENTS_TRACE.md](REQUIREMENTS_TRACE.md)
- [iceye_ai_engineer/part1_ingest.py](iceye_ai_engineer/part1_ingest.py)
- [iceye_ai_engineer/part1_chatbot.py](iceye_ai_engineer/part1_chatbot.py)
- [iceye_ai_engineer/part2_blob_boxes.py](iceye_ai_engineer/part2_blob_boxes.py)
- [iceye_ai_engineer/__init__.py](iceye_ai_engineer/__init__.py)
- [data/part1_entities.json](data/part1_entities.json)
- [tests/conftest.py](tests/conftest.py)
- [tests/test_part1.py](tests/test_part1.py)
- [tests/test_part2.py](tests/test_part2.py)

## Execute

Part 1 ingestion:

```powershell
uv run python -m iceye_ai_engineer.part1_ingest "AI Engineer Technical Homework Task.pdf" organization location person
```

Expected result:

- Extract text from the PDF with `kreuzberg`
- Detect named entities with `glinker`
- Write the entity store to [data/part1_entities.json](data/part1_entities.json)

Part 1 single-turn chatbot against the stored entity file:

```powershell
uv run python -m iceye_ai_engineer.part1_chatbot data/part1_entities.json "How many mentions of AI Engineer are in the doc?"
```

Expected result:

- Load only the stored entity JSON file
- Return structured JSON with:
  - `reply`
  - `entities`
  - `label` for each entity

Part 2 rotated blob bounding boxes from a 2D NumPy mask stored as a `.npy` file:

```powershell
uv run python -m iceye_ai_engineer.part2_blob_boxes path/to/mask.npy
```

This writes `blob_bounding_boxes.csv` in the repository root.

Expected result:

- Read a 2D NumPy binary mask
- Identify connected blobs
- Write one CSV row per blob with columns:
	- `blob_id`
	- `center_x`
	- `center_y`
	- `width`
	- `height`
	- `angle`

## Run tests

Run the test suite with:

```powershell
uv run pytest
```

The repository now contains:

- [tests/test_part1.py](tests/test_part1.py): verifies normalized unique entity output and reply counting from the stored entity data
- [tests/test_part2.py](tests/test_part2.py): verifies two-blob detection and required CSV header output

## Step-By-Step Test Creation

This section records the test-writing steps in the same way the rest of the README traces the session.

1. Picked deterministic helper functions instead of full external-model integration paths so the tests stay fast and stable.
2. For Part 1, used the local `EntityStore` and `ExtractedEntity` models to build an in-memory stored entity dataset.
3. Added a Part 1 assertion that `AI Engineer` and `AI\nEngineer` normalize to one unique entity.
4. Added a Part 1 assertion that the reply for `How many mentions of AI Engineer are in the doc?` reports `2` mentions from the stored entity file.
5. For Part 2, created a small 2D NumPy mask with two separate blobs.
6. Added a Part 2 assertion that `compute_rotated_boxes(...)` returns two boxes with unique blob IDs and positive dimensions.
7. Added a Part 2 assertion that `write_boxes_csv(...)` writes the required header: `blob_id,center_x,center_y,width,height,angle`.
8. Added a minimal [tests/conftest.py](tests/conftest.py) so the test runner imports the local package reliably from the repository root.
9. Ran `uv run pytest` to validate both tests.

## Validation Completed

Validated during this session:

- `py -3.12 -m uv sync`
- `uv run python -m iceye_ai_engineer.part1_ingest "AI Engineer Technical Homework Task.pdf" organization location person`
- `uv run python -m iceye_ai_engineer.part1_chatbot data/part1_entities.json "How many mentions of AI Engineer are in the doc?"`
- `uv run python -m iceye_ai_engineer.part2_blob_boxes path/to/mask.npy` on a synthetic validation mask
- `uv run pytest`

## Remaining Work

The implemented phases are complete for the current repository state. The only natural remaining step is delivery or further refinement if you want stricter integration tests.

## Requirement Status

For the detailed requirement-by-requirement trace and validation log, see [REQUIREMENTS_TRACE.md](REQUIREMENTS_TRACE.md).
