from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List
import asyncio
from playwright.async_api import async_playwright


@dataclass
class Job:
    title: str
    description: str
    url: str
    platform: str
    budget: str = ""
    posted_date: str = ""


class BaseScraper(ABC):
    def __init__(self):
        self.browser = None
        self.context = None
        self.page = None

    async def init_browser(self):
        playwright = await async_playwright().start()
        self.browser = await playwright.chromium.launch(headless=True)
        self.context = await self.browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        self.page = await self.context.new_page()

    async def close(self):
        if self.browser:
            await self.browser.close()

    @abstractmethod
    async def fetch_jobs(self) -> List[Job]:
        pass

    async def random_delay(self, min_sec=1, max_sec=3):
        import random
        await asyncio.sleep(random.uniform(min_sec, max_sec))