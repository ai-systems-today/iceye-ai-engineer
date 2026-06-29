# Requirements Trace

Source of truth: [AI Engineer Technical Homework Task.pdf](AI%20Engineer%20Technical%20Homework%20Task.pdf)

## Global delivery requirements

- [ ] Zip file representing a repo containing solutions to both tasks
- [x] Repository uses `uv` with [pyproject.toml](pyproject.toml)
- [x] Repository setup validates with `uv sync` as the only required setup command
- [x] Target Python version constrained to 3.12
- [x] All declared dependencies pinned to exact versions
- [ ] Repository has [tests](tests) sub-directory with one handwritten unit test for each task
- [x] Repository has [README.md](README.md)
- [x] [README.md](README.md) documents install and execute flows for the implemented solution
- [ ] [README.md](README.md) cannot honestly document compliant test execution until the handwritten tests exist

## Part 1 requirements

- [x] Single-turn CLI chatbot exists
- [x] Uses `kreuzberg` for text extraction/OCR first
- [x] Uses `glinker` for Named Entity Recognition
- [x] Saves detected named entities locally
- [x] Defines a Pydantic model for chatbot output
- [x] Chatbot output includes a conversational reply acknowledging the query
- [x] Chatbot output includes a list of all unique named entities
- [x] Chatbot output includes each entity type/label
- [x] Chatbot answers from stored entity data only, not from the original text

## Part 2 requirements

- [x] Accepts a 2D NumPy binary mask
- [x] Identifies each connected-component blob
- [x] Computes a rotated rectangle per blob that maximizes IoU with the blob via minimum-area angle search over bounding rectangles
- [x] Writes [blob_bounding_boxes.csv](blob_bounding_boxes.csv) with one row per blob
- [x] CSV columns are exactly `blob_id`, `center_x`, `center_y`, `width`, `height`, `angle`

## Step-by-step validation log

## Phase 1-11 Status

1. Repository skeleton: complete
2. Exact dependency pinning: complete
3. Part 1 ingestion and local persistence: complete
4. Part 1 structured output model: complete
5. Part 1 single-turn chatbot logic: complete
6. Part 2 blob identification: complete
7. Part 2 rotated rectangle computation: complete
8. Part 2 CSV output generation: complete
9. One handwritten unit test per task: incomplete
10. README completion: partial
11. Final compliance verification: partial

Phase 10 is partial because the README can only truthfully document compliant test execution after the handwritten tests exist.

Phase 11 is partial because the implementation has been validated, but full PDF completion still depends on phase 9 and the final zip delivery artifact.

### Step 1: repository skeleton

- Verified [pyproject.toml](pyproject.toml) exists.
- Verified [README.md](README.md) exists.
- Verified [tests](tests) directory exists.

### Step 2: exact dependency pinning

- Verified `requires-python` is constrained to Python 3.12, which is allowed by the PDF.
- Verified all declared dependencies are pinned to exact versions.
- Verified dependency set is limited to the libraries directly required by the PDF plus `pytest` for the required unit tests.
- Verified `py -3.12 -m uv sync` completes successfully from the repository root.
- Verified the active pre-existing Python 3.14 environment is not used for PDF compliance; validation is anchored to the installed Python 3.12 interpreter.

### Step 3: Part 1 ingestion and local persistence

- Verified the repo-local Python is installed at version 3.12.10.
- Verified [iceye_ai_engineer/part1_ingest.py](iceye_ai_engineer/part1_ingest.py) loads as a CLI with document path and labels.
- Verified `kreuzberg` extraction runs before `glinker` entity detection in the implementation path.
- Verified `uv run python -m iceye_ai_engineer.part1_ingest ...` writes a local JSON entity store at [data/part1_entities.json](data/part1_entities.json).
- Verified the persisted store contains entity records and does not include the original extracted text.

### Step 4 and Step 5: Part 1 structured chatbot output and single-turn logic

- Verified [iceye_ai_engineer/part1_chatbot.py](iceye_ai_engineer/part1_chatbot.py) defines Pydantic models for the structured output.
- Verified the chatbot is CLI-based and single-turn.
- Verified the chatbot run path loads only the persisted entity store file.
- Verified the chatbot returns a conversational reply plus unique entities and labels.
- Verified the chatbot normalizes line-break variants so unique-entity output is based on entity identity rather than source formatting.

### Step 6 through Step 8: Part 2 blob boxes and CSV output

- Verified [iceye_ai_engineer/part2_blob_boxes.py](iceye_ai_engineer/part2_blob_boxes.py) accepts a 2D NumPy mask path as CLI input.
- Verified connected components are identified with non-overlapping blob IDs.
- Verified a synthetic mask run produces `blob_bounding_boxes.csv` with the required filename and columns.
- Verified the implementation searches rotation angles and chooses the minimum-area bounding rectangle, which is the bounding-box form used to maximize IoU for enclosed blobs.

### Remaining blocker

- The PDF explicitly requires the unit tests to be handwritten by the candidate rather than generated by an LLM. I cannot satisfy that requirement literally while acting as the coding agent.
- The [tests](tests) directory exists but is still empty.
- Final zip packaging has not been created yet.