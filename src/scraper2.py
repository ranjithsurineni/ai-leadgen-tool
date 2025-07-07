import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

def scrape_remoteok_jobs(keyword=None, location=None, field=None, experience=None):
    """
    Scrape remote jobs with filtering options
    
    Args:
        keyword (str): Main search keyword
        location (str): Location filter (e.g., "US", "Europe", "Worldwide")
        field (str): Field filter (e.g., "AI", "DS", "ML", "Frontend", "Backend", "Nursing")
        experience (str): Experience level filter (e.g., "Fresher", "2", "3", "Senior")
    """
    url = f"https://remoteok.com/remote-{keyword}-jobs"
    headers = {"User-Agent": "Mozilla/5.0"}

    r = requests.get(url, headers=headers)
    if r.status_code != 200:
        print(f"[ERROR] Failed to fetch page. Status code: {r.status_code}")
        return pd.DataFrame()

    soup = BeautifulSoup(r.text, "html.parser")
    jobs = []

    for tr in soup.find_all("tr", class_="job"):
        try:
            title = tr.find("h2").text.strip()
            company = tr.find("h3").text.strip()
            tags = [tag.text.strip() for tag in tr.find_all("div", class_="tag")]
            link = "https://remoteok.com" + tr["data-href"]
            
            # Get location from tags or description
            job_location = "Remote"  # Default
            for tag in tags:
                if any(loc in tag.lower() for loc in ["us", "europe", "worldwide", "remote"]):
                    job_location = tag
                    break
            
            # Get experience level from title or tags
            job_experience = "Not specified"
            experience_keywords = {
                "fresher": ["entry", "junior", "fresher", "0-1", "0-2"],
                "mid": ["mid", "intermediate", "2-3", "3-4", "2-5"],
                "senior": ["senior", "lead", "principal", "5+", "6+", "7+"]
            }
            
            title_lower = title.lower()
            tags_lower = [tag.lower() for tag in tags]
            
            for exp_level, keywords in experience_keywords.items():
                if any(keyword in title_lower or any(keyword in tag for tag in tags_lower) for keyword in keywords):
                    job_experience = exp_level
                    break
            
            # Get field from title or tags
            job_field = "General"
            field_keywords = {
                "AI": ["ai", "artificial intelligence", "machine learning", "ml", "deep learning"],
                "DS": ["data science", "data scientist", "analytics"],
                "ML": ["machine learning", "ml engineer", "mlops"],
                "Frontend": ["frontend", "front-end", "react", "vue", "angular", "javascript"],
                "Backend": ["backend", "back-end", "python", "java", "node", "api"],
                "Nursing": ["nurse", "nursing", "healthcare", "medical"],
                "DevOps": ["devops", "sre", "infrastructure", "aws", "azure"],
                "Mobile": ["mobile", "ios", "android", "react native", "flutter"]
            }
            
            for field_name, keywords in field_keywords.items():
                if any(keyword in title_lower or any(keyword in tag for tag in tags_lower) for keyword in keywords):
                    job_field = field_name
                    break

            jobs.append({
                "title": title,
                "company": company,
                "tags": ", ".join(tags),
                "link": link,
                "location": job_location,
                "field": job_field,
                "experience": job_experience
            })
        except Exception as e:
            print(f"[WARN] Skipping a row due to error: {e}")
            continue

    # Apply filters
    if jobs:
        df = pd.DataFrame(jobs)
        
        # Filter by location
        if location and location.lower() != "any":
            df = df[df['location'].str.contains(location, case=False, na=False)]
        
        # Filter by field
        if field and field.lower() != "any":
            df = df[df['field'].str.contains(field, case=False, na=False)]
        
        # Filter by experience
        if experience and experience.lower() != "any":
            df = df[df['experience'].str.contains(experience, case=False, na=False)]
        
        if not df.empty:
            df.to_csv("data/leads_raw.csv", index=False)
            print(f"[SUCCESS] Scraped {len(df)} jobs → data/leads_raw.csv")
            return df
        else:
            print(f"[WARNING] No jobs found matching the specified filters.")
            return pd.DataFrame()
    else:
        print("[WARNING] No jobs found.")
        return pd.DataFrame()

if __name__ == "__main__":
    scrape_remoteok_jobs("ai")
