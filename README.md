# Intelligent Candidate Discovery

## Overview

This project was developed for the **Data & AI Challenge – Intelligent Candidate Discovery**.

The objective is to identify and rank the most relevant candidates for AI/ML-focused roles from a large candidate dataset. The solution processes candidate profiles, evaluates their skills, experience, career history, and recruiter engagement signals, and generates a ranked list of the top candidates.

---

## Problem Statement

Recruiters often need to identify high-quality AI and Machine Learning talent from thousands of candidate profiles.

The challenge is to:

* Analyze candidate profiles
* Identify candidates with strong AI/ML backgrounds
* Rank candidates according to relevance
* Generate a final recommendation list

---

## Approach

The solution uses a rule-based scoring system.

Each candidate receives a score based on multiple factors:

### 1. Experience Score

Candidates with 5–9 years of experience receive the highest score because they align well with typical hiring requirements for mid-level and senior AI roles.

### 2. Job Title Score

Relevant titles receive positive scores:

* AI Engineer
* ML Engineer
* Machine Learning Engineer
* Applied ML Engineer
* Data Scientist
* Applied Scientist
* Backend Engineer

Non-relevant titles receive penalties.

### 3. AI Skill Score

Candidates are rewarded for AI-related skills such as:

* NLP
* Machine Learning
* Deep Learning
* Fine-tuning LLMs
* LoRA
* Milvus
* Pinecone
* Weaviate
* Qdrant
* FAISS
* TensorFlow
* PyTorch

### 4. Retrieval & Ranking Bonus

Additional weight is given to candidates with skills related to:

* Information Retrieval
* Learning to Rank
* Recommendation Systems
* Vector Search
* Sentence Transformers
* BM25

### 5. Career History Analysis

Candidate work descriptions are scanned for relevant AI keywords including:

* Retrieval
* Ranking
* Embeddings
* Search
* RAG
* LLM
* Fine-tuning
* Vector Databases

### 6. Recruiter Signals

The following engagement metrics are incorporated:

* Recruiter Response Rate
* Interview Completion Rate
* Saved by Recruiters
* Search Appearance

### 7. Availability Factors

Additional bonuses are provided for:

* Open to Work status
* Short notice periods
* High GitHub activity
* Willingness to relocate

---

## Ranking Pipeline

1. Load candidate data from `candidates.json`
2. Parse candidate profiles
3. Calculate candidate scores
4. Sort candidates by score
5. Apply tie-breaking using candidate ID
6. Generate Top 100 ranked candidates
7. Export results to `submission.csv`

---

## Output

The solution generates:

`submission.csv`

Columns:

* candidate_id
* rank
* score
* reasoning

---

## Validation

The generated submission was validated using the provided validation script and successfully passed all checks.

Result:

Submission is valid.

---

## Technologies Used

* Python
* JSON
* CSV
* Rule-Based Ranking System

---

## Future Improvements

Future versions could incorporate:

* Learning-to-Rank models
* Candidate embeddings
* Semantic profile matching
* LLM-based profile understanding
* Explainable AI ranking mechanisms

---

## Repository Structure

├── rank.py
├── candidates.json
├── submission.csv
└── README.md

---

## Author

Karthik Sonaveni

Data & AI Challenge 2026
