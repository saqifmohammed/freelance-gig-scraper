import httpx
from typing import List
from config import ollama_config, ai_keywords
from scrapers import Job


class AISummarizer:
    def __init__(self):
        self.base_url = ollama_config.base_url
        self.model = ollama_config.model

    async def summarize(self, text: str) -> str:
        prompt = f"""Summarize this job posting in 2-3 sentences. Focus on:
- What the client needs (the main deliverable)
- Key technical requirements
- Any AI/ML specific requirements

Job Description:
{text[:2000]}

Summary:"""

        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    f"{self.base_url}/api/generate",
                    json={
                        "model": self.model,
                        "prompt": prompt,
                        "stream": False
                    }
                )
                if response.status_code == 200:
                    return response.json().get("response", "").strip()
                else:
                    return text[:200] + "..."
        except Exception as e:
            print(f"Summarization error: {e}")
            return text[:200] + "..."


class JobFilter:
    def __init__(self):
        self.keywords = ai_keywords.keywords

    def is_relevant(self, job: Job) -> bool:
        combined_text = f"{job.title} {job.description}".lower()
        matches = [keyword for keyword in self.keywords if keyword.lower() in combined_text]
        return len(matches) > 0

    async def filter_jobs(self, jobs: List[Job]) -> List[Job]:
        relevant_jobs = []
        for job in jobs:
            if self.is_relevant(job):
                relevant_jobs.append(job)
        return relevant_jobs

    async def process_jobs(self, jobs: List[Job]) -> List[Job]:
        summarizer = AISummarizer()
        filtered = await self.filter_jobs(jobs)
        
        for job in filtered:
            if job.description:
                job.description = await summarizer.summarize(job.description)
        
        return filtered