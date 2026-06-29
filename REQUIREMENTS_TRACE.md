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
- [ ] [README.md](README.md) fully documents install, execute, and test flows for the completed solution

## Part 1 requirements

- [ ] Single-turn CLI chatbot exists
- [ ] Uses `kreuzberg` for text extraction/OCR first
- [ ] Uses `glinker` for Named Entity Recognition
- [ ] Saves detected named entities locally
- [ ] Defines a Pydantic model for chatbot output
- [ ] Chatbot output includes a conversational reply acknowledging the query
- [ ] Chatbot output includes a list of all unique named entities
- [ ] Chatbot output includes each entity type/label
- [ ] Chatbot answers from stored entity data only, not from the original text

## Part 2 requirements

- [ ] Accepts a 2D NumPy binary mask
- [ ] Identifies each connected-component blob
- [ ] Computes a rotated rectangle per blob that maximizes IoU with the blob
- [ ] Writes [blob_bounding_boxes.csv](blob_bounding_boxes.csv) with one row per blob
- [ ] CSV columns are exactly `blob_id`, `center_x`, `center_y`, `width`, `height`, `angle`

## Step-by-step validation log

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