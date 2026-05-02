from .base import BaseScraper, Job
import re


class ToptalScraper(BaseScraper):
    async def fetch_jobs(self) -> list[Job]:
        jobs = []

        try:
            url = "https://www.toptal.com/work"
            await self.page.goto(url, wait_until="networkidle", timeout=45000)
            await self.random_delay(3, 5)

            links = await self.page.query_selector_all("a[href*='/work/']")

            job_urls = set()
            for link in links[:20]:
                try:
                    href = await link.get_attribute("href")
                    text = await link.inner_text()
                    if href and "/work/" in href and text and len(text) > 20:
                        job_urls.add(href)
                except:
                    continue

            print(f"Found {len(job_urls)} Toptal job URLs, visiting each...")

            for job_url in list(job_urls)[:10]:
                try:
                    full_url = job_url if job_url.startswith("http") else f"https://www.toptal.com{job_url}"
                    await self.page.goto(full_url, wait_until="networkidle", timeout=30000)
                    await self.random_delay(2, 3)

                    title_elem = await self.page.query_selector("h1")
                    title = await title_elem.inner_text() if title_elem else ""

                    desc_elem = await self.page.query_selector("div[class*='description'], article")
                    description = await desc_elem.inner_text() if desc_elem else ""

                    budget_elem = await self.page.query_selector("[class*='budget'], [class*='rate'], [class*='price']")
                    budget = await budget_elem.inner_text() if budget_elem else ""

                    if title and len(title) > 10:
                        jobs.append(Job(
                            title=title.strip()[:200],
                            description=description.strip()[:1500] if description else "",
                            url=full_url,
                            platform="Toptal",
                            budget=budget.strip() if budget else ""
                        ))

                    await self.random_delay(1, 2)

                except Exception as e:
                    print(f"Error visiting Toptal job: {e}")
                    continue

        except Exception as e:
            print(f"Toptal scraper error: {e}")

        return jobs