# Movie Watchlist

A minimal starter repository using Python, SQLite, and the OMDb API.

## Setup

**Option A — uv (recommended):**
```bash
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
```

**Option B — standard Python/pip:**
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Configuration

Set your OMDb API key:

```bash
export OMDB_API_KEY=your_api_key_here
```

## Database

Rebuild the seeded SQLite database:

```bash
python scripts/seed_db.py
```

## Run

```bash
python main.py
```
