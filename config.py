import os
from dataclasses import dataclass


@dataclass
class EmailConfig:
    smtp_server: str = "smtp.gmail.com"
    smtp_port: int = 587
    sender_email: str = os.getenv("GMAIL_EMAIL", "")
    sender_password: str = os.getenv("GMAIL_APP_PASSWORD", "")
    recipient_email: str = os.getenv("RECIPIENT_EMAIL", "")


@dataclass
class OllamaConfig:
    base_url: str = "http://localhost:11434"
    model: str = "llama3.2:latest"


@dataclass
class SchedulerConfig:
    hours_interval: int = 6


@dataclass
class AIKeywords:
    keywords = [
        "ai", "artificial intelligence", "machine learning", "ml",
        "chatbot", "conversational ai", "voice agent", "voice bot",
        "llm", "large language model", "gpt", "openai", "anthropic",
        "automation", "workflow automation", "rpa",
        "web app", "mobile app", "ios", "android", "react", "flutter",
        "python", "data science", "data analysis", "nlp", "nlu",
        "computer vision", "image recognition", "ocr",
        "api integration", "webhook", "integration",
        "custom gpt", "chatgpt plugin", "ai assistant",
        "bot development", "telegram bot", "discord bot",
        "ai agent", "autonomous agent", "ai workflow"
    ]


@dataclass
class TavilyConfig:
    api_key: str = os.getenv("TAVILY_API_KEY", "")


config = EmailConfig()
ollama_config = OllamaConfig()
scheduler_config = SchedulerConfig()
ai_keywords = AIKeywords()
tavily_config = TavilyConfig()