from tavily import TavilyClient
from scrapers import Job
import os
import html
from dotenv import load_dotenv

load_dotenv()


class TavilyFreelancerScraper:
    def __init__(self):
        api_key = os.getenv("TAVILY_API_KEY")
        if not api_key:
            raise ValueError("TAVILY_API_KEY not found in .env file")
        self.client = TavilyClient(api_key=api_key)

    async def fetch_jobs(self) -> list[Job]:
        jobs = []
        
        search_queries = [
            "site:freelancer.in AI chatbot automation projects",
            "site:freelancer.in machine learning python projects",
            "site:freelancer.in LLM GPT integration projects",
            "site:freelancer.in AI web app development projects",
            "site:freelancer.in voice assistant AI projects"
        ]

        seen_urls = set()

        for query in search_queries:
            try:
                print(f"Searching: {query}")
                search_result = self.client.search(
                    query=query,
                    max_results=10
                )

                for result in search_result.get("results", []):
                    url = result.get("url", "")
                    title = result.get("title", "")
                    content = result.get("content", "")
                    
                    if title and url and "freelancer.in" in url and url not in seen_urls:
                        seen_urls.add(url)
                        jobs.append(Job(
                            title=title.strip()[:200],
                            description=content.strip()[:1500] if content else "",
                            url=url,
                            platform="Freelancer.in"
                        ))

            except Exception as e:
                print(f"Tavily search error for query '{query}': {e}")
                continue

        return jobs

    async def extract_job_details(self, job: Job) -> Job:
        return job