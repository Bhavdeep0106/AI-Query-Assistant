# AI Data Analyst

An AI-powered Text-to-SQL application that converts natural language questions into SQL, validates and executes the queries, automatically corrects SQL errors, and visualizes results.

## Features

* Natural language to SQL using GPT-OSS 20B via Groq
* SQL validation with SQLGlot
* Automatic SQL error correction
* SQLite database execution
* Query history with persistent storage
* Automatic result visualization with Plotly
* Query execution metrics
* Streamlit web interface

## Architecture

```text
User Question
      ↓
GPT-OSS 20B
      ↓
SQL Generation
      ↓
SQLGlot Validation
      ↓
SQLite Execution
      ↓
Results + Visualization

SQL Error
      ↓
AI SQL Correction
      ↓
Retry
```

## Tech Stack

* Python
* Streamlit
* Groq
* GPT-OSS 20B
* SQLite
* SQLGlot
* Pandas
* Plotly

## Project Structure

```text
AI-SQL-Tool/
├── app.py
├── text_to_sql.py
├── database.py
├── query_history.py
├── evaluation.py
├── evaluation_correction.py
├── test_correction.py
├── requirements.txt
└── .streamlit/
    └── config.toml
```

## Evaluation

The Text-to-SQL system was evaluated against 10 predefined queries.

**Result Accuracy: 100% (10/10)**

The SQL self-correction mechanism was also tested using intentionally invalid SQL and successfully generated an executable correction.

## Setup

```bash
git clone <repository-url>
cd AI-SQL-Tool
pip install -r requirements.txt
```

Create a `.env` file:

```env
GROQ_API_KEY=your_groq_api_key
```

Run:

```bash
streamlit run app.py
```

## Deployment

The application is deployed using Streamlit Community Cloud with the Groq API key configured through deployment secrets.

## Future Improvements

* CSV upload and dynamic table creation
* Dynamic schema discovery
* Support for multiple datasets
* Persistent cloud database
* Advanced visualization selection
