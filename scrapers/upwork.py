from .base import BaseScraper, Job
import re


class UpworkScraper(BaseScraper):
    async def fetch_jobs(self) -> list[Job]:
        jobs = []

        try:
            search_urls = [
                "https://www.upwork.com/ab/jobs/search/?q=AI+chatbot+automation&sort=recency",
                "https://www.upwork.com/ab/jobs/search/?q=AI+web+app+development&sort=recency",
                "https://www.upwork.com/ab/jobs/search/?q=machine+learning+python&sort=recency"
            ]

            job_urls = set()

            for url in search_urls:
                await self.page.goto(url, wait_until="networkidle", timeout=45000)
                await self.random_delay(3, 5)

                links = await self.page.query_selector_all("a[href*='/jobs/']")
                for link in links[:10]:
                    try:
                        href = await link.get_attribute("href")
                        if href and "/jobs/" in href and "?" in href:
                            job_urls.add(href)
                    except:
                        continue

            print(f"Found {len(job_urls)} Upwork job URLs, visiting each...")

            for job_url in list(job_urls)[:10]:
                try:
                    await self.page.goto(job_url, wait_until="networkidle", timeout=30000)
                    await self.random_delay(2, 3)

                    title_elem = await self.page.query_selector("h1")
                    title = await title_elem.inner_text() if title_elem else ""

                    desc_elem = await self.page.query_selector("div[class*='description']")
                    description = await desc_elem.inner_text() if desc_elem else ""

                    if not description:
                        desc_elem = await self.page.query_selector("section")
                        description = await desc_elem.inner_text() if desc_elem else ""

                    budget_elem = await self.page.query_selector("[class*='budget'], [class*='price']")
                    budget = await budget_elem.inner_text() if budget_elem else ""

                    if title and len(title) > 10:
                        jobs.append(Job(
                            title=title.strip()[:200],
                            description=description.strip()[:1500] if description else "",
                            url=job_url,
                            platform="Upwork",
                            budget=budget.strip() if budget else ""
                        ))

                    await self.random_delay(1, 2)

                except Exception as e:
                    print(f"Error visiting Upwork job: {e}")
                    continue

        except Exception as e:
            print(f"Upwork scraper error: {e}")

        return jobs