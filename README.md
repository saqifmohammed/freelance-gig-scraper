# Freelance Gig Scraper 🤖

Automated scraper that finds AI/ML jobs from freelance platforms and sends them to your email.

## Supported Platforms

- **Freelancer.in** - Via Tavily AI Search API
- Upwork, Fiverr, Toptal - (Web scraping - may be blocked)

## Features

- **AI-Powered Search**: Uses Tavily API to find relevant gigs
- **Auto-Extraction**: Gets job title, description, budget from each listing
- **Excel Export**: Saves all jobs to Excel with new sheet per run
- **Email Reports**: Sends Excel file to your email every 6 hours
- **AI Summarization**: Uses local Ollama for job description summarization

## Prerequisites

1. **Python 3.8+** installed
2. **Gmail Account** with App Password
3. **Tavily API Key** (free) from https://tavily.com
4. **Ollama** (optional, for AI summarization) from https://ollama.com

## Installation

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/freelance-gig-scraper.git
cd freelance-gig-scraper

# Install dependencies
pip install -r requirements.txt
```

## Configuration

### 1. Create `.env` file

Copy `.env.example` to `.env` and fill in your credentials:

```env
# Gmail Configuration
GMAIL_EMAIL=your_email@gmail.com
GMAIL_APP_PASSWORD=your_gmail_app_password
RECIPIENT_EMAIL=your_email@gmail.com

# Tavily API Key (required for AI search)
# Get free key at: https://tavily.com
TAVILY_API_KEY=tvly-xxxxxxxxxxxxxxxxxxxxxxxx
```

### 2. Get Gmail App Password

1. Go to https://myaccount.google.com/apppasswords
2. Sign in with your Gmail
3. Generate a new app password for "Mail"
4. Use that 16-character password in `GMAIL_APP_PASSWORD`

### 3. Get Tavily API Key

1. Go to https://tavily.com
2. Sign up for free account
3. Copy your API key from dashboard
4. Add to `TAVILY_API_KEY` in `.env`

## Usage

### Run Once (Test)
```bash
python main.py --once
```

### Run on Schedule (Every 6 Hours)
```bash
python main.py --schedule
```

## Output

- **Excel File**: `job_leads.xlsx`
  - Creates new sheet per run (e.g., `Run_2026-05-03_00-00`)
  - Columns: Platform, Job Title, Description, Budget, URL, Posted Date

- **Email**: Excel file sent as attachment with job count

## Project Structure

```
freelance-gig-scraper/
├── main.py              # Entry point
├── scheduler.py        # Job scheduler
├── config.py           # Configuration
├── ai_processor.py     # AI filtering & summarization
├── email_sender.py     # Gmail SMTP sender
├── excel_storage.py    # Excel export
├── scrapers/           # Platform scrapers
│   ├── base.py
│   ├── upwork.py
│   ├── freelancer.py
│   ├── toptal.py
│   ├── fiverr.py
│   └── tavily_freelancer.py
├── requirements.txt
├── .env.example
└── .gitignore
```

## Troubleshooting

### "No jobs found"
- Check your Tavily API key is correct
- Verify internet connection

### "Email not sent"
- Verify Gmail app password is correct
- Ensure less secure app access is enabled or use App Password

### "Permission denied" errors
- Make sure `.env` file exists
- Check file permissions

## License

MIT

## Disclaimer

This tool is for educational purposes. Respect platform terms of service when scraping.