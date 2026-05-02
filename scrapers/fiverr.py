from .base import BaseScraper, Job
import re


class FiverrScraper(BaseScraper):
    async def fetch_jobs(self) -> list[Job]:
        jobs = []

        try:
            search_urls = [
                "https://www.fiverr.com/search/gigs?query=AI+chatbot+automation",
                "https://www.fiverr.com/search/gigs?query=AI+web+app+development",
                "https://www.fiverr.com/search/gigs?query=machine+learning+python"
            ]

            job_urls = set()

            for url in search_urls:
                await self.page.goto(url, wait_until="networkidle", timeout=45000)
                await self.random_delay(3, 5)

                links = await self.page.query_selector_all("a[href*='/services/']")
                for link in links[:10]:
                    try:
                        href = await link.get_attribute("href")
                        if href and "/services/" in href:
                            job_urls.add(href)
                    except:
                        continue

            print(f"Found {len(job_urls)} Fiverr gig URLs, visiting each...")

            for job_url in list(job_urls)[:10]:
                try:
                    await self.page.goto(job_url, wait_until="networkidle", timeout=30000)
                    await self.random_delay(2, 3)

                    title_elem = await self.page.query_selector("h1")
                    title = await title_elem.inner_text() if title_elem else ""

                    desc_elem = await self.page.query_selector("div.description, div.gig-description")
                    description = await desc_elem.inner_text() if desc_elem else ""

                    if not description:
                        desc_elem = await self.page.query_selector("div[class*='desc']")
                        description = await desc_elem.inner_text() if desc_elem else ""

                    price_elem = await self.page.query_selector("span.price, div.price")
                    price = await price_elem.inner_text() if price_elem else ""

                    if title and len(title) > 10:
                        jobs.append(Job(
                            title=title.strip()[:200],
                            description=description.strip()[:1500] if description else "",
                            url=job_url,
                            platform="Fiverr",
                            budget=price.strip() if price else ""
                        ))

                    await self.random_delay(1, 2)

                except Exception as e:
                    print(f"Error visiting Fiverr gig: {e}")
                    continue

        except Exception as e:
            print(f"Fiverr scraper error: {e}")

        return jobs