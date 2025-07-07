# 🚀 AI-Powered Lead Generation & Prioritization Tool

A smart, end-to-end system that scrapes remote job listings from the web and intelligently ranks them based on relevance using AI/NLP techniques. Designed to help founders, freelancers, recruiters, and sales teams identify the most promising leads with minimal effort.

---

## 🧠 What It Does

- **Scrapes job listings** based on user-defined filters like keyword, location, field, and experience level.
- **Ranks leads using AI** with Sentence-BERT (`MiniLM`) based on similarity to high-value keywords like "Founder", "CTO", "AI", "Series A", etc.
- **Visualizes and filters results** interactively using a Streamlit dashboard.
- **Exports results** to downloadable CSVs (`leads_raw.csv`, `leads_ranked.csv`, `leads_filtered.csv`).

---

## ⚙️ Technologies Used

- 🧠 `SentenceTransformers` for semantic similarity ranking
- 🌐 `Requests` + `BeautifulSoup` for job scraping
- 📊 `Pandas` for data processing
- 📈 `Streamlit` for interactive dashboard
- 📂 `CSV` export for raw, ranked, and filtered leads

---

## 💡 Features

| Feature                   | Description                                     |
| ------------------------- | ----------------------------------------------- |
| 🔄 Scraping System        | Gathers job listings from RemoteOK              |
| 🧠 AI Ranking             | Semantic similarity scoring with Sentence-BERT  |
| 🧭 Sidebar Flow Tracker   | Visual stage updates: Scraping → Ranking → Done |
| 🎯 Score Threshold Filter | Adjust minimum relevance score dynamically      |
| 📥 CSV Download           | Download full or filtered results               |
| 📊 Charting               | Bar chart of score distribution                 |
| 🔗 Clickable Job Links    | Direct access to job postings                   |
| 🧪 Smart Filters          | Keyword, field, location, experience            |

---

## 🧬 Core Execution Flow

1. **User Inputs Filters**
   - Keyword (e.g., "AI")
   - Location (e.g., "Worldwide")
   - Field (e.g., "DS", "Frontend", "Nursing")
   - Experience level
2. **Scrapes Jobs** from RemoteOK (`leads_raw.csv`)
3. **Ranks Jobs** via cosine similarity with high-value keywords → `leads_ranked.csv`
4. **Displays** filtered, downloadable results and score visualizations

---

## 📁 Folder Structure
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

## 🚀 How to Run It

```bash
# Clone the repo
git clone https://github.com/your-username/ai-leadgen-tool.git
cd ai-leadgen-tool

# Install dependencies
pip install -r requirements.txt

# Run Streamlit app
streamlit run app/app.py

```

## Future Enhancements:

  ✅ Captcha bypass or API-based scraping for anti-bot sites like LinkedIn/Indeed
  
  ✅ Multi-site scraping engine (Indeed, Wellfound, etc.)
  
  ✅ Auto Email/CRM integration for outreach
  
  ✅ SaaS deployment with login and usage analytics
  
  ✅ Customizable keyword embeddings for different industries
  
  ✅ Revenue Potential: Lead-selling SaaS, Recruiter/HR tool, Freelancer utility


---

## Who Can Use This?
  🔹 Founders & Sales Teams – to discover new B2B contacts or early adopters
  
  🔹 Freelancers – to spot AI/tech-focused gigs faster
  
  🔹 Recruiters – to automate resume-matching and prioritize outreach
  
  🔹 Job Seekers – to find top-aligned job roles quickly

--- 
❤️ Made By
Ranjith Kumar Surineni

🔗 [LinkedIn](https://www.linkedin.com/in/ranjith-kumar-surineni-b73b981b6/) • 📧 [ranjithsurineni.official@gmail.com](mailto:ranjithsurineni.official@gmail.com)

Open to freelance, internship, and AI-focused opportunities!
  
---
