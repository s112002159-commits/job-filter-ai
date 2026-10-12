import os
from fastapi import FastAPI, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="基於生成式 AI 優秀職缺篩選器 API")

# 模擬專題資料庫來源 (Canonical Job Schema)
MOCK_JOBS = [
    {
        "id": "job_001",
        "title": "Python 後端架構工程師",
        "company_name": "智網科技股份有限公司",
        "location": {"city": "台南市", "district": "永康區"},
        "salary": {"min": 45000, "max": 65000, "type": "月薪"},
        "working_hours": {"text": "09:00 - 18:00", "shift": False, "overtime_desc": "極少加班"},
        "insurance": {"labor": True, "health": True, "evidence": "原文提及：『全額保障勞健保與提撥6%勞退』"},
        "benefits": ["年終獎金2個月", "彈性上下班", "定期健檢"],
        "confidence": "A"
    },
    {
        "id": "job_002",
        "title": "AI 應用開發軟體工程師",
        "company_name": "創研人工智慧技術有限公司",
        "location": {"city": "台南市", "district": "科學園區"},
        "salary": {"min": 50000, "max": 75000, "type": "月薪"},
        "working_hours": {"text": "08:30 - 17:30", "shift": False, "overtime_desc": "專案高峰期配合加班"},
        "insurance": {"labor": True, "health": True, "evidence": "原文提及：『享勞保、健保及團體保險』"},
        "benefits": ["免費零食飲料", "績效分紅"],
        "confidence": "A"
    }
]

# API 路由：搜尋與過濾職缺[cite: 2, 3]
@app.get("/api/jobs")
def get_jobs(q: Optional[str] = None, city: Optional[str] = None, min_salary: int = 0):
    results = MOCK_JOBS
    if q:
        results = [j for j in results if q.lower() in j["title"].lower() or q.lower() in j["company_name"].lower()]
    if city and city != "全部":
        results = [j for j in results if j["location"]["city"] == city]
    if min_salary > 0:
        results = [j for j in results if j["salary"]["min"] >= min_salary]
    return {"status": "success", "data": results}

# 託管前端靜態 HTML
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def serve_frontend():
    return FileResponse("static/index.html")