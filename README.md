# AI Engineer Technical Homework Task

This repository is being implemented strictly against [AI Engineer Technical Homework Task.pdf](AI%20Engineer%20Technical%20Homework%20Task.pdf).

## Scope

The PDF is the governing brief for this repository.

Important interpretation rule used in this repository:

- If the PDF explicitly requires something, it was treated as mandatory.
- If the PDF leaves something open, the smallest compliant implementation was chosen.
- If something is good engineering practice but not explicitly required by the PDF, it is called out separately as a recommendation rather than presented as a requirement.

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

## Best Practices And Non-PDF Extras

These are good engineering practices that are relevant, but they are not all explicitly required by the PDF.

### .gitignore

The repository now includes [.gitignore](.gitignore).

Best-practice recommendation:

- add `.venv/`
- add `__pycache__/`
- add `.pytest_cache/`
- add generated output files such as `blob_bounding_boxes.csv`
- add large local caches if they appear during model downloads

Why it matters:

- avoids committing local environments
- avoids committing generated files
- keeps the repo cleaner for delivery

### .gitattributes

The repository now includes [.gitattributes](.gitattributes).

Best-practice recommendation:

- normalize line endings for text files
- optionally mark binary artifacts such as the PDF and zip archive as binary

Why it matters:

- prevents line-ending noise across systems
- makes diffs more predictable

### Packaging The Delivery Zip

The current archive is [iceye-ai-engineer-current-state.zip](iceye-ai-engineer-current-state.zip).

How it was created:

```powershell
Compress-Archive -Path AI* , data , iceye_ai_engineer , pyproject.toml , README.md , REQUIREMENTS_TRACE.md , tests , uv.lock , .gitignore , .gitattributes -DestinationPath iceye-ai-engineer-current-state.zip -Force
```

Why this shape was used:

- includes the PDF, source, tests, lock file, and documentation
- includes `.gitignore` and `.gitattributes`
- excludes `.git/` and `.venv/`
- matches the PDF request for a repo zip rather than a virtual environment bundle

### Recreate The Archive

If you make any final edits before submission, recreate the delivery archive with:

```powershell
Compress-Archive -Path AI* , data , iceye_ai_engineer , pyproject.toml , README.md , REQUIREMENTS_TRACE.md , tests , uv.lock , .gitignore , .gitattributes -DestinationPath iceye-ai-engineer-current-state.zip -Force
```

Why rerun this step:

- ensures the zip matches the latest saved files
- keeps the documentation and tests synchronized with the delivered archive

## Part 1 Design Choices

### DB Or JSON

The PDF says the detected named entities can be saved in the format you prefer, for example a local DB or JSON.

This repository uses JSON:

- output file: [data/part1_entities.json](data/part1_entities.json)

Why JSON was chosen:

- simplest compliant local persistence format
- easy to inspect manually
- easy to use from the CLI chatbot
- avoids adding a database dependency that the PDF does not require

### Why The Chatbot Uses Stored Data Only

The PDF explicitly says the chatbot should answer based purely on the already detected entity DB/file and not on the original text.

That is why the Part 1 chatbot:

- loads [data/part1_entities.json](data/part1_entities.json)
- does not reopen the PDF
- does not depend on the extracted text once the entity store exists

### Interface Creativity

The PDF leaves the chatbot interface open and says to use creativity, but it still says the interface should be command line.

Current choice:

- a CLI for ingestion
- a CLI for the single-turn question path

Why this is compliant:

- command line is explicitly allowed
- no GUI is required by the PDF
- single-turn behavior is easier to validate and explain

## Part 2 Input And Reasoning

### Where Does `mask.npy` Come From?

There is no `mask.npy` file included in the repository because the PDF does not provide one.

What the PDF actually says:

- input is a 2D NumPy array representing a binary semantic segmentation mask

What that means in practice:

- the implementation expects the user or assessor to provide a NumPy mask file
- the README command uses `path/to/mask.npy` as a placeholder input path
- for local validation, a synthetic mask was generated during testing rather than stored permanently in the repo

So the short answer is:

- you will not find `mask.npy` in this repo
- it must come from the real task input or be generated for testing

### Why Part 2 Has Three Separate Requirement Sections

The PDF breaks Part 2 into three conceptually different requirements.

1. Input

Why it exists:

- defines the contract for what data the algorithm receives
- tells us the mask is binary, 2D, and contains distinct non-overlapping blobs

Why the code needs it:

- input validation depends on this assumption
- connected-component detection only makes sense once the input format is clear

2. Task

Why it exists:

- defines the actual algorithmic work
- identify each blob
- compute a rotated rectangle for each blob
- maximize IoU between the blob and the filled rectangle mask

Why the code needs it:

- this is the heart of Part 2
- it explains why we do connected components first and geometry second

3. Output format

Why it exists:

- defines exactly how results must be delivered
- removes ambiguity about filenames and columns

Why the code needs it:

- the implementation must emit `blob_bounding_boxes.csv`
- the CSV columns must match exactly or the submission is not compliant

### Why The Part 2 Pipeline Is Structured This Way

The current Part 2 flow is:

1. Load a 2D binary mask
2. Find connected components
3. Treat each component as one blob instance
4. Search over rotation angles
5. Pick the smallest enclosing rotated rectangle from that search
6. Write the required CSV

Why this order is used:

- you cannot compute one box per object until the objects are separated first
- once a blob is isolated, the box search is local to that blob
- once boxes are computed, the PDF requires a CSV export in a specific schema

### Why No Permanent Example Mask Is Included

The PDF does not provide a source mask asset in the repo.

The local tests intentionally generate tiny synthetic masks instead because:

- they are deterministic
- they keep the test self-contained
- they prove the algorithm on known input without inventing an external artifact that the PDF did not provide

## UI Question

There is no UI in the current repository.

Why no UI was added:

- the PDF does not require a web UI or desktop UI
- for Part 1 it explicitly says the interface should be command line
- for Part 2 it defines an algorithm and CSV output, not a visual application

About the idea of sliders, bounded panels, or a parameter UI:

- that could be added as an optional extra
- it is not required by the PDF
- adding it would increase scope and introduce frontend code that is not necessary for compliance

So the current choice was to stay minimal and strictly within the brief.

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

Input note for Part 2:

- `path/to/mask.npy` is a placeholder path
- the repository does not ship with a permanent sample mask because the PDF does not provide one
- use a real assessor-provided mask or generate a local test mask

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

## Questions Answered Explicitly

### Did I read the PDF in detail?

Yes. I extracted the full available text from [AI Engineer Technical Homework Task.pdf](AI%20Engineer%20Technical%20Homework%20Task.pdf) and used it as the governing brief.

Important nuance:

- the textual requirements were extracted and followed
- page 3 also contains an example semantic segmentation mask image
- that image is illustrative input context, not an additional text specification with hidden fields

### What was missing before this documentation pass?

Before this update, the README did not explicitly explain:

- why JSON was chosen instead of a DB
- why no sample `mask.npy` exists
- why no UI was added
- what `.gitignore` and `.gitattributes` would add as best practices
- why Part 2 is split into input, task, and output requirements

Those details are now documented above.

## Remaining Work

The implemented phases are complete for the current repository state. The only natural remaining step is delivery or further refinement if you want stricter integration tests.

## Requirement Status

For the detailed requirement-by-requirement trace and validation log, see [REQUIREMENTS_TRACE.md](REQUIREMENTS_TRACE.md).
