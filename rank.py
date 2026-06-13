import json
import csv

AI_SKILLS = {
    "nlp",
    "machine learning",
    "deep learning",
    "fine-tuning llms",
    "lora",
    "milvus",
    "pinecone",
    "weaviate",
    "qdrant",
    "faiss",
    "embeddings",
    "retrieval",
    "ranking",
    "huggingface",
    "transformers",
    "bert",
    "llm",
    "rag",
    "tensorflow",
    "pytorch"
}

GOOD_TITLES = [
    "ai engineer",
    "ml engineer",
    "machine learning engineer",
    "applied ml engineer",
    "data scientist",
    "machine learning scientist",
    "applied scientist",
    "software engineer",
    "backend engineer",
    "platform engineer",
    "senior ai engineer",
    "senior machine learning engineer",
    "lead ai engineer"
]

BAD_TITLES = [
    "marketing manager",
    "hr manager",
    "accountant",
    "sales executive",
    "graphic designer",
    "content writer",
    "operations manager",
    "customer support"
]

JD_KEYWORDS = [
    "retrieval",
    "ranking",
    "embeddings",
    "vector",
    "recommendation",
    "search",
    "rag",
    "llm",
    "fine-tuning",
    "pinecone",
    "milvus",
    "weaviate",
    "qdrant",
    "faiss",
    "ndcg",
    "mrr",
    "map",
    "evaluation",
    "re-ranking"
]

SERVICE_COMPANIES = {
    "tcs",
    "infosys",
    "wipro",
    "cognizant",
    "accenture",
    "capgemini",
    "mindtree"
}

VECTOR_KEYWORDS = {
    "pinecone",
    "milvus",
    "weaviate",
    "qdrant",
    "faiss",
    "vector search",
    "vector database",
    "pgvector"
}


def score_candidate(candidate):

    score = 0.0

    profile = candidate.get("profile", {})
    signals = candidate.get("redrob_signals", {})

    title = profile.get("current_title", "").lower()
    years = profile.get("years_of_experience", 0)

    # Experience scoring
    if 5 <= years <= 9:
        score += 80
    elif 4 <= years < 5:
        score += 10
    elif 9 < years <= 12:
        score -= 40
    elif years > 12:
        score -= 150    
    else:
        score -= 80

    # Title scoring
    for t in GOOD_TITLES:
        if t in title:
            score += 30

    for t in BAD_TITLES:
        if t in title:
            score -= 40

    # Skills scoring
    ai_skill_count = 0

    for skill in candidate.get("skills", []):

        name = skill.get("name", "").lower()

        if name in AI_SKILLS:
            ai_skill_count += 1
            score += 8

            prof = skill.get("proficiency", "").lower()

            if prof == "advanced":
                score += 3
            elif prof == "expert":
                score += 5

        if name in {
            "learning to rank",
            "vector search",
            "information retrieval",
            "recommendation systems",
            "sentence transformers",
            "bm25"
        }:
            score += 60

    score += ai_skill_count * 3
    
    # Evaluation framework bonus
    for skill in candidate.get("skills", []):

     s = skill.get("name", "").lower()

     if s in {
        "ndcg",
        "mrr",
        "map",
        "evaluation",
        "ab testing",
        "a/b testing"
     }:
        score += 25

    # Career history text
    career_text = ""

    for job in candidate.get("career_history", []):
        career_text += " " + job.get("description", "").lower()

    # JD keyword matching
    for kw in JD_KEYWORDS:
        if kw in career_text:
            score += 10

    # Vector DB / retrieval bonus
    for kw in VECTOR_KEYWORDS:
        if kw in career_text:
            score += 15

    # Product vs service company penalty
    service_count = 0

    for job in candidate.get("career_history", []):

        company = job.get("company", "").lower()

        if company in SERVICE_COMPANIES:
            service_count += 1

    total_jobs = len(candidate.get("career_history", []))

    if total_jobs > 0 and service_count == total_jobs:
        score -= 50

    # Recruiter engagement
    score += signals.get("recruiter_response_rate", 0) * 25
    score += signals.get("interview_completion_rate", 0) * 15
    rr = signals.get("recruiter_response_rate", 0)

    if rr < 0.10:
     score -= 150
    elif rr < 0.20:
     score -= 100
    elif rr < 0.30:
     score -= 40
    # Open to work
    if signals.get("open_to_work_flag", False):
        score += 10

    # GitHub activity
    github = signals.get("github_activity_score", -1)

    if github > 60:
        score += 25
    elif github > 30:
        score += 15
    elif github > 10:
        score += 5

    # Notice period
     
    
    notice = signals.get("notice_period_days", 180)

    if notice <= 30:
      score += 20
    elif notice <= 60:
      score += 10
    elif notice >= 120:
      score -= 30

    # Recruiter interest
    score += min(signals.get("saved_by_recruiters_30d", 0), 20)
    score += min(signals.get("search_appearance_30d", 0) / 50, 10)

    # Preferred locations
    location = profile.get("location", "").lower()

    if any(city in location for city in [
        "pune",
        "noida",
        "delhi",
        "gurgaon",
        "hyderabad",
        "mumbai",
        "bangalore",
        "bengaluru"
    ]):
        score += 10

    if signals.get("willing_to_relocate", False):
     score += 15    

    return round(score, 4)
    


results = []

with open("candidates.json", "r", encoding="utf-8") as f:

    for line in f:

        line = line.strip()

        if not line:
            continue

        try:

            candidate = json.loads(line)

            score = score_candidate(candidate)

            results.append((score, candidate))

        except Exception:
            continue

results.sort(
    key=lambda x: (-x[0], x[1]["candidate_id"])
)

top100 = results[:100]

with open("submission.csv", "w", newline="", encoding="utf-8") as f:

    writer = csv.writer(f)

    writer.writerow([
        "candidate_id",
        "rank",
        "score",
        "reasoning"
    ])

    for rank, (score, candidate) in enumerate(top100, start=1):

        profile = candidate.get("profile", {})
        signals = candidate.get("redrob_signals", {})

        skills = [
            s.get("name", "")
            for s in candidate.get("skills", [])
        ]

        top_skills = ", ".join(skills[:3])

        reasoning = (
            f"{profile.get('current_title')} with "
            f"{profile.get('years_of_experience')} years experience; "
            f"skills include {top_skills}; "
            f"response rate {signals.get('recruiter_response_rate', 0):.2f}; "
            f"notice period {signals.get('notice_period_days', 0)} days."
        )

        writer.writerow([
            candidate["candidate_id"],
            rank,
            score,
            reasoning
        ])

print("Done. Created submission.csv")