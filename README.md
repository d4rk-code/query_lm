# Query LM_

Query LM_ is an AI-powered analytics assistant that converts natural language questions into MariaDB SQL queries, executes them on a connected database, and generates analytical summaries using Large Language Models.

The project combines:
- Flask
- MariaDB
- Anthropic Claude API
- HTML/CSS frontend
- AI-powered SQL generation + summarization

---

# Features

- Natural language analytics queries
- Automatic SQL generation
- MariaDB query execution
- AI-generated business summaries
- Minimal black & white analytics UI
- Streaming-ready architecture

---

# Setup Guide

## 1. Clone the Repository

```bash
git clone https://github.com/d4rk-code/query_lm.git
cd query_lm
```

---

## 2. Create a Virtual Environment

### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

<<<<<<< HEAD
### Windows 
=======
### Windows
>>>>>>> 6ba72c53df073fa880aad978b6f757046eaf61ab

```bash
python -m venv venv
venv\Scripts\activate
```

---

## 3. Install Dependencies

```bash
pip install flask anthropic mysql-connector-python python-dotenv
```

---

# Environmental Variables

Create a `.env` file in the root directory of the project.

### Example:

```env
key=YOUR_ANTHROPIC_API_KEY
user=YOUR_DATABASE_USER
password=YOUR_DATABASE_PASSWORD
database=YOUR_DATABASE_NAME
```

# Variable Descriptions

| Variable   | Description                     |
| ---------- | ------------------------------- |
| `key`      | Anthropic API key               |
| `user`     | MariaDB/MySQL database username |
| `password` | Database password               |
| `database` | Database name                   |

---

# Running the Application

Start the Flask server:

```bash
python app.py
```

The application will run on:

```text
http://127.0.0.1:5000
```
