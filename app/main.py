from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
# from fastapi.staticfiles import StaticFiles  # optional
from pydantic import BaseModel
from pdfminer.high_level import extract_text
import joblib
import os
import uuid
import heapq
import random
from collections import Counter, defaultdict, deque

app = FastAPI(
    title="AI Hiring Platform",
    description="Advanced AI Hiring & Workforce Optimization"
)

# -------------------------------
# OPTIONAL FRONTEND (DISABLED)
# -------------------------------
# app.mount("/static", StaticFiles(directory="static"), name="static")

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
MODELS_DIR = os.path.join(PROJECT_ROOT, "models")
VIEWS_DIR = os.path.join(PROJECT_ROOT, "views")

# -------------------------------
# LOAD MODELS
# -------------------------------
vectorizer = None
classifier_model = None

try:
    vectorizer = joblib.load(os.path.join(MODELS_DIR, "tfidf_vectorizer.joblib"))
    classifier_model = joblib.load(os.path.join(MODELS_DIR, "resume_model.joblib"))
    print("✅ Models loaded successfully!")
except Exception as e:
    print(f"❌ Model loading error: {e}")

# -------------------------------
# INPUT SCHEMAS
# -------------------------------
class ResumeInput(BaseModel):
    text: str

class CandidatesInput(BaseModel):
    candidates: list

class BudgetInput(BaseModel):
    candidates: list
    budget: int

class GraphInput(BaseModel):
    edges: list
    source: str
    sink: str

# -------------------------------
# FRONTEND ROUTE (DISABLED)
# -------------------------------
# @app.get("/")
# def home():
#     return FileResponse(os.path.join(VIEWS_DIR, "index.html"))

# -------------------------------
# RESUME TEXT PREDICTION
# -------------------------------
@app.post("/predict-role")
def predict_role(resume: ResumeInput):

    if not resume.text.strip():
        return {"status": "error", "message": "Empty resume"}

    if vectorizer is None or classifier_model is None:
        return {"status": "error", "message": "Models not loaded"}

    vectorized = vectorizer.transform([resume.text])
    prediction = classifier_model.predict(vectorized)

    return {
        "status": "success",
        "predicted_role": str(prediction[0])
    }

# -------------------------------
# RESUME FILE UPLOAD
# -------------------------------
@app.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...)):

    try:
        temp_file = f"temp_{uuid.uuid4()}.pdf"

        with open(temp_file, "wb") as buffer:
            buffer.write(await file.read())

        text = extract_text(temp_file)
        os.remove(temp_file)

        if not text.strip():
            return {"status": "error", "message": "No readable text"}

        vectorized = vectorizer.transform([text])
        prediction = classifier_model.predict(vectorized)

        return {
            "status": "success",
            "predicted_role": str(prediction[0])
        }

    except Exception as e:
        return {"status": "error", "message": str(e)}

# ============================================================
# 🔥 HUFFMAN CODING (COMPRESSION)
# ============================================================

class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq


def build_huffman_tree(text):
    freq = Counter(text)
    heap = [HuffmanNode(c, f) for c, f in freq.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)

        merged = HuffmanNode(None, left.freq + right.freq)
        merged.left = left
        merged.right = right

        heapq.heappush(heap, merged)

    return heap[0]


def generate_codes(node, prefix="", codebook=None):
    if codebook is None:
        codebook = {}

    if node:
        if node.char:
            codebook[node.char] = prefix
        generate_codes(node.left, prefix + "0", codebook)
        generate_codes(node.right, prefix + "1", codebook)

    return codebook


@app.post("/compress-resume")
def compress_resume(resume: ResumeInput):

    text = resume.text

    tree = build_huffman_tree(text)
    codebook = generate_codes(tree)

    encoded = "".join(codebook[ch] for ch in text)

    return {
        "original_length": len(text),
        "compressed_length": len(encoded),
        "compression_ratio": round(len(encoded) / len(text), 2),
        "encoded_preview": encoded[:200]
    }

# ============================================================
# 🔥 RANDOMIZED HIRING
# ============================================================

@app.post("/randomized-hiring")
def randomized_hiring(data: CandidatesInput):

    candidates = data.candidates.copy()
    random.shuffle(candidates)

    best = None
    hires = []

    for c in candidates:
        if best is None or c["score"] > best["score"]:
            best = c
            hires.append(c)

    return {
        "final_selected": best,
        "hiring_steps": hires,
        "total_checked": len(candidates)
    }

# ============================================================
# 🔥 APPROXIMATION (VERTEX COVER)
# ============================================================

@app.post("/approximate-cover")
def approx_cover(data: GraphInput):

    edges = data.edges.copy()
    cover = set()

    while edges:
        u, v = edges.pop()
        cover.add(u)
        cover.add(v)

        edges = [e for e in edges if u not in e and v not in e]

    return {"approx_vertex_cover": list(cover)}

# ============================================================
# 🔥 0/1 KNAPSACK
# ============================================================

def optimize_hiring_budget(candidates, max_budget):

    n = len(candidates)
    dp = [[0] * (max_budget + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        salary = candidates[i - 1]["expected_salary"]
        score = candidates[i - 1]["score_value"]

        for w in range(1, max_budget + 1):
            if salary <= w:
                dp[i][w] = max(dp[i - 1][w], dp[i - 1][w - salary] + score)
            else:
                dp[i][w] = dp[i - 1][w]

    hired = []
    w = max_budget

    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            hired.append(candidates[i - 1])
            w -= candidates[i - 1]["expected_salary"]

    return {
        "max_score": dp[n][max_budget],
        "total_cost": max_budget - w,
        "hired_candidates": hired
    }


@app.post("/optimize-budget")
def optimize_budget(data: BudgetInput):
    return optimize_hiring_budget(data.candidates, data.budget)

# ============================================================
# 🔥 FORD-FULKERSON
# ============================================================

class HRFlowNetwork:
    def __init__(self):
        self.graph = defaultdict(dict)

    def add_edge(self, u, v, capacity):
        self.graph[u][v] = capacity
        if u not in self.graph[v]:
            self.graph[v][u] = 0

    def bfs(self, source, sink, parent):
        visited = set()
        queue = deque([source])
        visited.add(source)

        while queue:
            u = queue.popleft()
            for v, cap in self.graph[u].items():
                if v not in visited and cap > 0:
                    queue.append(v)
                    visited.add(v)
                    parent[v] = u
                    if v == sink:
                        return True
        return False

    def ford_fulkerson(self, source, sink):
        parent = {}
        max_flow = 0

        while self.bfs(source, sink, parent):
            path_flow = float("Inf")
            s = sink

            while s != source:
                path_flow = min(path_flow, self.graph[parent[s]][s])
                s = parent[s]

            v = sink
            while v != source:
                u = parent[v]
                self.graph[u][v] -= path_flow
                self.graph[v][u] += path_flow
                v = parent[v]

            max_flow += path_flow

        return {"maximum_interviews": max_flow}


@app.post("/maximize-interviews")
def maximize_interviews(data: GraphInput):

    network = HRFlowNetwork()

    for u, v, cap in data.edges:
        network.add_edge(u, v, cap)

    return network.ford_fulkerson(data.source, data.sink)