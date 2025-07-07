

# Report: AI-Based Lead Prioritization Tool for enhacement- (Update-soom...)

### Objective
To build a simple AI-powered tool that ranks B2B leads based on title relevance and decision-making signals.

### Stack
- Python + Streamlit
- Sentence-BERT for semantic similarity
- BeautifulSoup for scraping

### Business Value
Improves sales outreach ROI by focusing on top 10% relevant leads. Useful for post-acquisition GTM strategies.

### Alignment
Caprae Capital aims to scale companies post-acquisition through AI. This tool helps identify better customer leads to accelerate GTM execution.

---


### 🚀 New Features
- **Multi-Website Scraping**: Scrapes from 5+ popular job websites
  - RemoteOK
  - Indeed
  - Stack Overflow Jobs
  - AngelList Talent
  - We Work Remotely
- **Advanced Filtering**: Filter by location, field, and experience level
- **Smart Categorization**: Automatically categorizes jobs by field and experience
- **Enhanced UI**: Modern Streamlit interface with real-time statistics
- **Comprehensive Results**: Shows source website, location, field, and experience for each job

### 🔍 Search Capabilities
- **Keyword Search**: Custom search terms (AI, Python, React, Nurse, etc.)
- **Location Filtering**: US, Europe, Worldwide, Remote
- **Field Categorization**: AI, DS, ML, Frontend, Backend, Nursing, DevOps, Mobile, Design, Marketing
- **Experience Levels**: Fresher, Mid-level, Senior
- **Website Selection**: Choose which websites to scrape from

### Features
- Multi-website job scraping with intelligent filtering
- Ranks job titles based on relevance to decision-makers using SentenceTransformers
- Advanced Streamlit UI with real-time progress tracking
- Export capabilities for both raw and filtered data
- Comprehensive statistics and visualizations

### Setup
```bash
git clone https://github.com/
cd AI LEADGEN TOOL
pip install -r requirements.txt
streamlit run app/app.py
```

### Usage
1. **Enter Search Keyword**: Type your search term (e.g., "Python", "AI", "React")
2. **Select Websites**: Choose which job websites to scrape from
3. **Apply Filters**: Set location, field, and experience preferences
4. **Scrape & Rank**: Click the button to start the process
5. **Review Results**: View ranked leads with detailed information
6. **Export Data**: Download filtered results as CSV

# Folder structure
```bash
project_root/
├── src/
│   ├── scraper.py          # Original web scraping logic
│   ├── scraper2.py         # Enhanced single-website scraper
│   ├── multi_scraper.py    # Multi-website scraping engine
│   ├── ranker.py           # Lead ranking logic using NLP
│   ├── verifier.py         # Email verification utility
│   └── utils.py            # Helper functions
├── app/
│   └── app.py              # Enhanced Streamlit UI
├── notebooks/
│   └── demo.ipynb          # Optional Jupyter notebook walkthrough
├── data/
│   ├── leads_raw.csv       # Raw scraped data
│   └── leads_ranked.csv    # Ranked, verified leads
├── requirements.txt        # Python dependencies
├── README.md               # Project overview & setup
└── report.md               # One-page submission rationale
```
---

## Installation

```bash
$ pip install -r requirements.txt
```

### Additional Setup (if needed)

  1. Install playwright for enhanced scraping function
  
  ```bash
  $ pip install playwright
  $ python -m playwright install
  ```

### Supported Websites
  - **RemoteOK**: Remote job listings (at-present)
  - **Indeed**: General job search (update_soon)
  - **Stack Overflow Jobs**: Tech-focused positions (update_soon)
  - **AngelList Talent**: Startup and tech jobs (update_soon)
  - **We Work Remotely**: Remote work opportunities (update_soon)

### Data Fields
Each scraped job includes:
- **Title**: Job position title
- **Company**: Hiring company name
- **Location**: Job location or remote status
- **Field**: Categorized field (AI, Frontend, etc.)
- **Experience**: Experience level classification
- **Source**: Website where job was found
- **Tags**: Relevant skills and technologies
- **Link**: Direct link to job posting
- **Relevance Score**: AI-calculated relevance score
