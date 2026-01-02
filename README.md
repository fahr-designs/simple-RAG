# RAG application

A Retrieval Augmented Generation (RAG) system that allows you to query documents using semantic search and generate answers using a local LLM via Ollama.

## Overview

This project:
- Ingests text documents from the `documents/` folder
- Chunks and embeds them using SentenceTransformers
- Stores embeddings in ChromaDB for semantic search
- Retrieves relevant context for queries
- Generates answers using Ollama (Mistral 7B by default)

## Prerequisites

This guide assumes you're starting from scratch with no Python installed.

### 1. Install Python

#### Windows
1. Visit [python.org/downloads](https://www.python.org/downloads/)
2. Download the latest Python 3.11+ installer
3. Run the installer
   - **IMPORTANT**: Check "Add Python to PATH" before clicking Install
4. Verify installation:
   ```bash
   python --version
   ```

#### macOS
```bash
# Using Homebrew (install Homebrew first from brew.sh if needed)
brew install python@3.11
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install python3.11 python3.11-venv python3-pip
```

### 2. Install pipx

pipx allows you to install Python applications in isolated environments.

#### Windows/macOS/Linux
```bash
python -m pip install --user pipx
python -m pipx ensurepath
```

After installation, **close and reopen your terminal** for the PATH changes to take effect.

Verify installation:
```bash
pipx --version
```

### 3. Install virtualenv using pipx

```bash
pipx install virtualenv
```

Verify installation:
```bash
virtualenv --version
```

### 4. Install Ollama

Ollama is required to run the LLM locally.

#### Windows/macOS
1. Visit [ollama.com/download](https://ollama.com/download)
2. Download and install Ollama for your OS
3. Verify installation:
   ```bash
   ollama --version
   ```

#### Linux
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

### 5. Pull the Mistral Model

```bash
ollama pull mistral:7b
```

This downloads the Mistral 7B model (approximately 4GB). You can change the model in `config.py` if you prefer a different one.

## Setup Instructions

### 1. Navigate To Project Directory

```
cd /path/to/project
```

### 2. Create Virtual Environment

```bash
virtualenv venv
```

This creates a `venv/` folder containing an isolated Python environment.

### 3. Activate Virtual Environment

#### Windows (PowerShell)
```powershell
.\venv\Scripts\Activate.ps1
```

#### Windows (CMD)
```cmd
.\venv\Scripts\activate.bat
```

#### Windows (Git Bash/MINGW)
```bash
source venv/Scripts/activate
```

#### macOS/Linux
```bash
source venv/bin/activate
```

You should see `(venv)` prefix in your terminal prompt when activated.

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- `chromadb` - Vector database for storing document embeddings
- `sentence-transformers` - For generating text embeddings
- `requests` - For communicating with Ollama API

**Note**: First installation may take several minutes as it downloads ML models.

## Usage

### 1. Add Documents

Place your `.txt` files in the `documents/` folder. The system will process all text files in this directory.

Example:
```
documents/
  your_document.txt
  another_document.txt
```

### 2. Ingest Documents

This processes your documents and stores them in the vector database:

```bash
python ingest.py
```

You should see output like:
```
Loading documents...
Found 1 documents
Loading embedding model...
  documents/meditations_by_marcus_aurelius.txt: 142 chunks

Generating embeddings for 142 chunks...
Storing in ChromaDB...
✓ Indexed 142 chunks from 1 documents
```

### 3. Query Your Documents

Start the interactive query interface:

```bash
python query.py
```

Example interaction:
```
RAG System ready (using mistral:7b)
Type 'quit' to exit

Ask a question: What does Marcus Aurelius say about anger?

Retrieving relevant context...
Found 3 relevant chunks

Generating answer...

Answer: [Generated answer based on your documents]

Sources:
  - documents/meditations_by_marcus_aurelius.txt
```

Type `quit`, `exit`, or `q` to exit or CTRL + c

## Configuration
Edit `config.py` to customize

## Deactivating Virtual Environment
When you're done working, deactivate the virtual environment:
```bash
deactivate
```

## Troubleshooting

### "python: command not found"
- Make sure Python is installed and added to PATH
- Try `python3` instead of `python`

### "pipx: command not found" after installation
- Close and reopen your terminal
- Ensure PATH was updated with `python -m pipx ensurepath`

### "virtualenv: command not found"
- Make sure pipx is working first
- Reinstall: `pipx install virtualenv`

### Ollama connection errors
- Ensure Ollama is running: `ollama serve`
- Check if model is pulled: `ollama list`

### Import errors after pip install
- Ensure virtual environment is activated (you should see `(venv)` in prompt)
- Try upgrading pip: `pip install --upgrade pip`

### Slow embedding generation
- First run downloads the `all-MiniLM-L6-v2` model (80MB)
- Subsequent runs will be faster

## Project Structure

```
rag_system/
├── documents/          # Place your .txt files here
├── chroma_db/         # Vector database (auto-generated)
├── venv/              # Virtual environment (auto-generated)
├── config.py          # Configuration settings
├── ingest.py          # Document ingestion script
├── query.py           # Query interface
├── requirements.txt   # Python dependencies
└── readme.md          # This file
```