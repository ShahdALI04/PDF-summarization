# PDF Chat Bot API

An intelligent PDF document interaction system using Gemini AI.

## Features ✨

✅ **Large File Support** (2000+ pages)  
✅ **Natural Chat Interface** - Write anything and the system will understand  
✅ **Flexible Summarization** - Supports any type of summarization  
✅ **Smart Processing** - Automatically adapts to file size  
✅ **English Interface** - Clean English interface  
✅ **CORS Support** - Team-friendly API integration  

## Quick Start

### 1. Environment Setup
```bash
# Create virtual environment
python -m venv .venv1

# Activate virtual environment
# Windows:
.venv1\Scripts\activate.bat
# Linux/Mac:
source .venv1/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. API Key Setup
Create a `.env` file in the root directory:
```env
GEMINI_API_KEY=your_actual_api_key_here
AI_HOST=127.0.0.1
AI_PORT=5000
CORS_ALLOW_ORIGINS=http://localhost:3000,http://localhost:4000,http://127.0.0.1:3000,http://127.0.0.1:4000
CORS_ALLOW_CREDENTIALS=true
LOG_LEVEL=INFO
SPACY_MODEL=en_core_web_sm
```

### 3. Start Server
```bash
# Method 1: Using Python directly
python run.py

# Method 2: Using batch file (Windows)
start.bat

# Method 3: Using uvicorn directly
uvicorn main_fastapi:app --host 127.0.0.1 --port 5000 --reload
```

### 4. Test System
```bash
# Method 1: Using Python directly
python cli_test.py

# Method 2: Using batch file (Windows)
test.bat
```

## Important Links

- **Home Page**: http://127.0.0.1:5000/
- **Swagger UI**: http://127.0.0.1:5000/docs
- **Health Check**: http://127.0.0.1:5000/health

## Usage Examples

### Chat Interface Examples:
```
👤 You: Who is the author?
🤖 Assistant: [Answer]

👤 You: Explain object-oriented programming
🤖 Assistant: [Explanation]

👤 You: Summarize the content
🤖 Assistant: [Detailed Summary]

👤 You: Give me a brief summary
🤖 Assistant: [Brief Summary]
```

## API Endpoints

- `GET /` - API root endpoint
- `POST /upload/` - Upload PDF file
- `POST /ask/` - Ask a question (POST)
- `GET /ask/` - Ask a question (GET)
- `POST /summarize/` - Summarize document (POST)
- `GET /summarize/` - Summarize document (GET)
- `GET /health/` - Health check

## Getting API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new project
3. Get API Key
4. Add to `.env` file

## Project Structure

```
final-/
├── main_fastapi.py      # Main FastAPI application
├── run.py              # Server runner
├── cli_test.py         # CLI interface
├── start.bat           # Windows server starter
├── test.bat            # Windows CLI tester
├── requirements.txt    # Python dependencies
├── README.md          # This file
├── .gitignore         # Git ignore rules
├── .env               # Environment variables (create this)
├── agents/            # AI agent modules
├── utils/             # Utility functions
├── services/          # Service modules
└── storage/           # Storage modules
```

## Troubleshooting

### Server Not Responding
1. Ensure virtual environment is activated
2. Check `.env` file configuration
3. Verify API key is set correctly
4. Use `start.bat` for Windows

### API Key Issues
1. Verify Gemini API key is valid
2. Check API quota limits
3. Ensure key is properly set in `.env`

### Virtual Environment Issues
1. Make sure you're using `.venv1` (not `.venv`)
2. Activate environment before running commands
3. Install requirements: `pip install -r requirements.txt`

---

**🎉 Now you can chat with any PDF naturally!**

