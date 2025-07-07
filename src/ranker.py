from sentence_transformers import SentenceTransformer, util
import pandas as pd
import numpy as np

# Load Sentence-BERT model once globally
model = SentenceTransformer('all-MiniLM-L6-v2')

# Define high-priority role/context keywords
important_keywords = [
    "founder", "chief technology officer", "cto",
    "scaling", "ai", "growth", "series a",
    "decision maker", "venture", "startup", "ceo"
]

# Pre-encode keywords once for efficiency
keyword_embeddings = model.encode(important_keywords)

def rank_leads(csv_path="data/leads_raw.csv", top_n=20):
    try:
        df = pd.read_csv(csv_path)
    except FileNotFoundError:
        print(f"[ERROR] File not found: {csv_path}")
        return pd.DataFrame()

    if 'title' not in df.columns:
        print(f"[ERROR] Column 'title' not found in file: {csv_path}")
        return pd.DataFrame()

    scores = []
    for title in df['title'].fillna(""):
        try:
            title_embedding = model.encode(title)
            sim_scores = util.cos_sim(title_embedding, keyword_embeddings)
            score = sim_scores.mean().item()
        except Exception as e:
            print(f"[WARN] Failed to process title '{title}': {e}")
            score = 0
        scores.append(score)

    df["relevance_score"] = pd.Series(scores, dtype='float64')
    df.sort_values(by="relevance_score", ascending=False, inplace=True)
    df.reset_index(drop=True, inplace=True)

    output_path = "data/leads_ranked.csv"
    df.to_csv(output_path, index=False)
    print(f"[SUCCESS] Ranked leads saved to: {output_path}")
    print(f"[INFO] Top {top_n} Leads:")
    print(df.head(top_n)[["title", "company", "relevance_score"]])

    return df
