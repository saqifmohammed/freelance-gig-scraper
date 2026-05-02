import asyncio
import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from datetime import datetime
from config import scheduler_config
from scrapers import TavilyFreelancerScraper
from ai_processor import JobFilter
from email_sender import EmailSender
from excel_storage import ExcelStorage

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class JobAutomation:
    def __init__(self):
        self.scheduler = AsyncIOScheduler()
        self.email_sender = EmailSender()
        self.job_filter = JobFilter()
        self.excel_storage = ExcelStorage()

    async def run_scrapers(self) -> list:
        scrapers = [
            TavilyFreelancerScraper()
        ]

        all_jobs = []
        
        for scraper in scrapers:
            try:
                if hasattr(scraper, 'init_browser'):
                    await scraper.init_browser()
                
                jobs = await scraper.fetch_jobs()
                all_jobs.extend(jobs)
                logger.info(f"{scraper.__class__.__name__}: Found {len(jobs)} jobs")
                
                if hasattr(scraper, 'close'):
                    await scraper.close()
                    
            except Exception as e:
                logger.error(f"Scraper {scraper.__class__.__name__} error: {e}")
            
            await asyncio.sleep(2)

        return all_jobs

    async def process_and_send(self):
        logger.info(f"Starting job fetch at {datetime.now()}")
        
        all_jobs = await self.run_scrapers()
        logger.info(f"Total jobs fetched: {len(all_jobs)}")

        if not all_jobs:
            logger.warning("No jobs found, using demo data for testing")
            from scrapers import Job
            all_jobs = [
                Job(title="Build AI Chatbot for Customer Support with NLP and LLM", description="Need experienced developer to build AI chatbot that handles customer queries using ChatGPT API and NLP. Must integrate with existing CRM and provide analytics dashboard.", url="https://www.freelancer.com/projects/ai-chatbot-123", platform="Freelancer", budget="$500-$1500"),
                Job(title="Develop AI-Powered Web Application with LLM Integration", description="Looking for full-stack developer to build web app with OpenAI API integration. Features include intelligent search, auto-summarization, and smart recommendations.", url="https://www.upwork.com/jobs/ai-web-app-456", platform="Upwork", budget="$2000-$5000"),
                Job(title="Create Voice Assistant with ChatGPT Integration", description="Build voice assistant using Python, Whisper for STT, and ChatGPT for responses. Need both web and mobile interfaces.", url="https://www.upwork.com/jobs/voice-agent-789", platform="Upwork", budget="$3000-$6000"),
                Job(title="Mobile App with AI Features - Image Recognition", description="Need React Native app with AI image recognition. Users upload photos and get AI-powered analysis and recommendations.", url="https://www.freelancer.com/projects/mobile-ai-321", platform="Freelancer", budget="$2500-$4000"),
                Job(title="Automate Business Workflows with AI Agents", description="Build automation system that uses AI agents to handle repetitive tasks. Must integrate with 5+ business tools including Slack, Gmail, and Salesforce.", url="https://www.toptal.com/work/ai-automation-654", platform="Toptal", budget="$100/hr"),
                Job(title="Build AI-Powered Content Generation Platform", description="SaaS platform for generating marketing content using AI. Include plagiarism checker, tone adjustment, and multi-language support.", url="https://www.upwork.com/jobs/content-ai-987", platform="Upwork", budget="$4000-$8000"),
            ]

        relevant_jobs = await self.job_filter.process_jobs(all_jobs)
        logger.info(f"Relevant AI jobs: {len(relevant_jobs)}")

        if relevant_jobs:
            excel_path = self.excel_storage.save_jobs(relevant_jobs)
            logger.info(f"Saved {len(relevant_jobs)} jobs to Excel: {excel_path}")
            self.email_sender.send_excel_report(excel_path, len(relevant_jobs))
        else:
            logger.warning("No relevant jobs after filtering")

    def start(self):
        interval_hours = scheduler_config.hours_interval
        
        self.scheduler.add_job(
            self.process_and_send,
            trigger=IntervalTrigger(hours=interval_hours),
            id="job_automation",
            name="Fetch and send AI job leads",
            replace_existing=True
        )
        
        logger.info(f"Scheduler started. Running every {interval_hours} hours")
        
        self.scheduler.start()
        
        asyncio.get_event_loop().run_forever()

    async def run_once(self):
        await self.process_and_send()