from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional
import json
import os

app = FastAPI(
    title="SOČ Archiv API",
    description="api pro vyhledávání vítězných prací SOČ na základě dat z archiv.soc.cz",
    docs_url="/api",
    redoc_url="/api/redoc"
)

class Work(BaseModel):
    id: int
    title: str
    author: str
    school: str
    field: str
    year: int
    keywords: List[str]
    content_url: str
    annotation: str

DATA_FILE = "data.json"
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, encoding="utf-8") as f:
        raw_data = json.load(f)
    works_db = [Work(**item) for item in raw_data]
else:
    works_db = []

def matches_query(work: Work, q: Optional[str]) -> bool:
    if not q:
        return True
    q = q.lower()
    return (
        q in work.title.lower() or
        q in work.author.lower() or
        q in work.field.lower() or
        q in work.annotation.lower()
    )

@app.get("/works", response_model=List[Work])
def search_works(
    query: Optional[str] = Query(None, description="Fulltextový dotaz"),
    field: Optional[str] = Query(None, description="Filtrování podle oboru"),
    school: Optional[str] = Query(None, description="Filtrování podle školy"),
    year: Optional[int] = Query(None, description="Filtrování podle roku")
):
    results = []
    for work in works_db:
        if not matches_query(work, query):
            continue
        if field and field.lower() not in work.field.lower():
            continue
        if school and school.lower() not in work.school.lower():
            continue
        if year and work.year != year:
            continue
        results.append(work)
    return results

@app.delete("/admin/works/{work_id}")
def delete_work(work_id: int):
    global works_db
    before = len(works_db)
    works_db = [w for w in works_db if w.id != work_id]
    if len(works_db) == before:
        raise HTTPException(404, "Práce nenalezena")

    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump([w.dict() for w in works_db], f, ensure_ascii=False, indent=2)
    return {"status": "smazáno"}

@app.get("/participants")
def list_participants():
    authors = {}
    for w in works_db:
        if w.author not in authors:
            authors[w.author] = set()
        authors[w.author].add(w.year)
    return [{"author": a, "years": sorted(list(years))} for a, years in authors.items()]

@app.get("/")
def root():
    return {"message": "SOČ Archiv API – data z archiv.soc.cz", "works_count": len(works_db)}