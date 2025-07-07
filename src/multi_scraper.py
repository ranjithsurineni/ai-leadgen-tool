import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import time
import random
from urllib.parse import quote_plus, urljoin
import json

class MultiWebsiteScraper:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        
    def scrape_remoteok(self, keyword, location=None, field=None, experience=None):
        """Scrape from RemoteOK"""
        print(f"[INFO] Scraping RemoteOK for: {keyword}")
        jobs = []
        
        try:
            url = f"https://remoteok.com/remote-{keyword}-jobs"
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")
                
                for tr in soup.find_all("tr", class_="job"):
                    try:
                        title = tr.find("h2").text.strip()
                        company = tr.find("h3").text.strip()
                        tags = [tag.text.strip() for tag in tr.find_all("div", class_="tag")]
                        link = "https://remoteok.com" + tr["data-href"]
                        
                        job_data = self._process_job_data(title, company, tags, link, "RemoteOK")
                        if self._apply_filters(job_data, location, field, experience):
                            jobs.append(job_data)
                            
                    except Exception as e:
                        print(f"[WARN] RemoteOK: Error processing job: {e}")
                        continue
                        
        except Exception as e:
            print(f"[ERROR] RemoteOK scraping failed: {e}")
            
        return jobs
    
    def scrape_indeed(self, keyword, location=None, field=None, experience=None):
        """Scrape from Indeed"""
        print(f"[INFO] Scraping Indeed for: {keyword}")
        jobs = []
        
        try:
            # Indeed search URL
            search_query = quote_plus(keyword)
            location_query = quote_plus(location) if location else "remote"
            url = f"https://www.indeed.com/jobs?q={search_query}&l={location_query}&sort=date"
            
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")
                
                # Find job cards
                job_cards = soup.find_all("div", class_="job_seen_beacon")
                
                for card in job_cards[:20]:  # Limit to first 20 jobs
                    try:
                        title_elem = card.find("h2", class_="jobTitle")
                        title = title_elem.get_text(strip=True) if title_elem else "N/A"
                        
                        company_elem = card.find("span", class_="companyName")
                        company = company_elem.get_text(strip=True) if company_elem else "N/A"
                        
                        location_elem = card.find("div", class_="companyLocation")
                        job_location = location_elem.get_text(strip=True) if location_elem else "Remote"
                        
                        link_elem = card.find("a", class_="jcs-JobTitle")
                        link = "https://www.indeed.com" + link_elem["href"] if link_elem else "#"
                        
                        # Extract tags from job description
                        tags = []
                        desc_elem = card.find("div", class_="job-snippet")
                        if desc_elem:
                            tags = [tag.strip() for tag in desc_elem.get_text().split() if len(tag) > 3]
                        
                        job_data = self._process_job_data(title, company, tags, link, "Indeed", job_location)
                        if self._apply_filters(job_data, location, field, experience):
                            jobs.append(job_data)
                            
                    except Exception as e:
                        print(f"[WARN] Indeed: Error processing job: {e}")
                        continue
                        
        except Exception as e:
            print(f"[ERROR] Indeed scraping failed: {e}")
            
        return jobs
    
    def scrape_stackoverflow(self, keyword, location=None, field=None, experience=None):
        """Scrape from Stack Overflow Jobs"""
        print(f"[INFO] Scraping Stack Overflow for: {keyword}")
        jobs = []
        
        try:
            search_query = quote_plus(keyword)
            url = f"https://stackoverflow.com/jobs?q={search_query}&r=true"
            
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")
                
                # Find job listings
                job_listings = soup.find_all("div", class_="-job")
                
                for listing in job_listings[:20]:  # Limit to first 20 jobs
                    try:
                        title_elem = listing.find("h2", class_="mb4")
                        title = title_elem.get_text(strip=True) if title_elem else "N/A"
                        
                        company_elem = listing.find("h3", class_="mb4")
                        company = company_elem.get_text(strip=True) if company_elem else "N/A"
                        
                        link_elem = listing.find("a", class_="s-link")
                        link = "https://stackoverflow.com" + link_elem["href"] if link_elem else "#"
                        
                        # Extract tags
                        tags = []
                        tag_elements = listing.find_all("a", class_="post-tag")
                        tags = [tag.get_text(strip=True) for tag in tag_elements]
                        
                        job_data = self._process_job_data(title, company, tags, link, "Stack Overflow")
                        if self._apply_filters(job_data, location, field, experience):
                            jobs.append(job_data)
                            
                    except Exception as e:
                        print(f"[WARN] Stack Overflow: Error processing job: {e}")
                        continue
                        
        except Exception as e:
            print(f"[ERROR] Stack Overflow scraping failed: {e}")
            
        return jobs
    
    def scrape_angelco(self, keyword, location=None, field=None, experience=None):
        """Scrape from AngelList Talent"""
        print(f"[INFO] Scraping AngelList for: {keyword}")
        jobs = []
        
        try:
            search_query = quote_plus(keyword)
            url = f"https://angel.co/talent/jobs?keywords={search_query}&remote=true"
            
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")
                
                # Find job listings
                job_listings = soup.find_all("div", class_="listing")
                
                for listing in job_listings[:20]:  # Limit to first 20 jobs
                    try:
                        title_elem = listing.find("h3", class_="title")
                        title = title_elem.get_text(strip=True) if title_elem else "N/A"
                        
                        company_elem = listing.find("div", class_="company")
                        company = company_elem.get_text(strip=True) if company_elem else "N/A"
                        
                        link_elem = listing.find("a")
                        link = "https://angel.co" + link_elem["href"] if link_elem else "#"
                        
                        # Extract tags
                        tags = []
                        tag_elements = listing.find_all("span", class_="tag")
                        tags = [tag.get_text(strip=True) for tag in tag_elements]
                        
                        job_data = self._process_job_data(title, company, tags, link, "AngelList")
                        if self._apply_filters(job_data, location, field, experience):
                            jobs.append(job_data)
                            
                    except Exception as e:
                        print(f"[WARN] AngelList: Error processing job: {e}")
                        continue
                        
        except Exception as e:
            print(f"[ERROR] AngelList scraping failed: {e}")
            
        return jobs
    
    def scrape_we_work_remotely(self, keyword, location=None, field=None, experience=None):
        """Scrape from We Work Remotely"""
        print(f"[INFO] Scraping We Work Remotely for: {keyword}")
        jobs = []
        
        try:
            # Map keyword to category
            category_map = {
                "ai": "programming",
                "python": "programming", 
                "javascript": "programming",
                "react": "programming",
                "nurse": "customer-support",
                "design": "design",
                "marketing": "marketing"
            }
            
            category = category_map.get(keyword.lower(), "programming")
            url = f"https://weworkremotely.com/categories/remote-{category}-jobs"
            
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")
                
                # Find job listings
                job_listings = soup.find_all("li", class_="feature")
                
                for listing in job_listings[:20]:  # Limit to first 20 jobs
                    try:
                        title_elem = listing.find("span", class_="title")
                        title = title_elem.get_text(strip=True) if title_elem else "N/A"
                        
                        company_elem = listing.find("span", class_="company")
                        company = company_elem.get_text(strip=True) if company_elem else "N/A"
                        
                        link_elem = listing.find("a")
                        link = "https://weworkremotely.com" + link_elem["href"] if link_elem else "#"
                        
                        # Extract tags from title and company
                        tags = [keyword, category]
                        
                        job_data = self._process_job_data(title, company, tags, link, "We Work Remotely")
                        if self._apply_filters(job_data, location, field, experience):
                            jobs.append(job_data)
                            
                    except Exception as e:
                        print(f"[WARN] We Work Remotely: Error processing job: {e}")
                        continue
                        
        except Exception as e:
            print(f"[ERROR] We Work Remotely scraping failed: {e}")
            
        return jobs
    
    def _process_job_data(self, title, company, tags, link, source, location="Remote"):
        """Process and categorize job data"""
        title_lower = title.lower()
        tags_lower = [tag.lower() for tag in tags]
        
        # Get location from tags or description
        job_location = location
        for tag in tags:
            if any(loc in tag.lower() for loc in ["us", "europe", "worldwide", "remote"]):
                job_location = tag
                break
        
        # Get experience level from title or tags
        job_experience = "Not specified"
        experience_keywords = {
            "fresher": ["entry", "junior", "fresher", "0-1", "0-2", "intern"],
            "mid": ["mid", "intermediate", "2-3", "3-4", "2-5"],
            "senior": ["senior", "lead", "principal", "5+", "6+", "7+", "staff"]
        }
        
        for exp_level, keywords in experience_keywords.items():
            if any(keyword in title_lower or any(keyword in tag for tag in tags_lower) for keyword in keywords):
                job_experience = exp_level
                break
        
        # Get field from title or tags
        job_field = "General"
        field_keywords = {
            "AI": ["ai", "artificial intelligence", "machine learning", "ml", "deep learning", "neural"],
            "DS": ["data science", "data scientist", "analytics", "bi"],
            "ML": ["machine learning", "ml engineer", "mlops", "ai engineer"],
            "Frontend": ["frontend", "front-end", "react", "vue", "angular", "javascript", "typescript"],
            "Backend": ["backend", "back-end", "python", "java", "node", "api", "server"],
            "Nursing": ["nurse", "nursing", "healthcare", "medical", "patient"],
            "DevOps": ["devops", "sre", "infrastructure", "aws", "azure", "kubernetes"],
            "Mobile": ["mobile", "ios", "android", "react native", "flutter", "swift"],
            "Design": ["design", "ui", "ux", "graphic", "visual"],
            "Marketing": ["marketing", "growth", "seo", "content", "social media"]
        }
        
        for field_name, keywords in field_keywords.items():
            if any(keyword in title_lower or any(keyword in tag for tag in tags_lower) for keyword in keywords):
                job_field = field_name
                break
        
        return {
            "title": title,
            "company": company,
            "tags": ", ".join(tags),
            "link": link,
            "location": job_location,
            "field": job_field,
            "experience": job_experience,
            "source": source
        }
    
    def _apply_filters(self, job_data, location=None, field=None, experience=None):
        """Apply filters to job data"""
        if location and location.lower() != "any":
            if not any(loc in job_data['location'].lower() for loc in [location.lower(), "remote"]):
                return False
        
        if field and field.lower() != "any":
            if field.lower() not in job_data['field'].lower():
                return False
        
        if experience and experience.lower() != "any":
            if experience.lower() not in job_data['experience'].lower():
                return False
        
        return True
    
    def scrape_all_websites(self, keyword, location=None, field=None, experience=None, websites=None):
        """Scrape from multiple websites"""
        if websites is None:
            websites = ["remoteok", "indeed", "stackoverflow", "angelco", "we_work_remotely"]
        
        all_jobs = []
        
        website_scrapers = {
            "remoteok": self.scrape_remoteok,
            "indeed": self.scrape_indeed,
            "stackoverflow": self.scrape_stackoverflow,
            "angelco": self.scrape_angelco,
            "we_work_remotely": self.scrape_we_work_remotely
        }
        
        for website in websites:
            if website in website_scrapers:
                try:
                    jobs = website_scrapers[website](keyword, location, field, experience)
                    all_jobs.extend(jobs)
                    print(f"[SUCCESS] {website}: Found {len(jobs)} jobs")
                    
                    # Add delay between requests to be respectful
                    time.sleep(random.uniform(1, 3))
                    
                except Exception as e:
                    print(f"[ERROR] Failed to scrape {website}: {e}")
                    continue
        
        # Remove duplicates based on title and company
        unique_jobs = []
        seen = set()
        
        for job in all_jobs:
            job_key = (job['title'].lower(), job['company'].lower())
            if job_key not in seen:
                seen.add(job_key)
                unique_jobs.append(job)
        
        print(f"[INFO] Total unique jobs found: {len(unique_jobs)}")
        return unique_jobs

def scrape_remoteok_jobs(keyword="AI", location=None, field=None, experience=None, websites=None):
    """
    Main function to scrape jobs from multiple websites
    
    Args:
        keyword (str): Main search keyword
        location (str): Location filter
        field (str): Field filter
        experience (str): Experience level filter
        websites (list): List of websites to scrape from
    """
    scraper = MultiWebsiteScraper()
    
    if websites is None:
        websites = ["remoteok", "indeed", "stackoverflow", "angelco", "we_work_remotely"]
    
    jobs = scraper.scrape_all_websites(keyword, location, field, experience, websites)
    
    if jobs:
        df = pd.DataFrame(jobs)
        df.to_csv("data/leads_raw.csv", index=False)
        print(f"[SUCCESS] Scraped {len(df)} jobs from {len(websites)} websites → data/leads_raw.csv")
        return df
    else:
        print("[WARNING] No jobs found.")
        return pd.DataFrame()

if __name__ == "__main__":
    # Test the scraper
    jobs = scrape_remoteok_jobs("python", websites=["remoteok", "stackoverflow"])
    print(f"Found {len(jobs)} jobs") 