from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from collections import defaultdict

API_KEY = "ak_0cplurm6gxeovhk8q32qavz3"
EMAIL = "23f3000717@ds.study.iitm.ac.in"

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # or the exam domain
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Event(BaseModel):
    user: str
    amount: float
    ts: int

class RequestBody(BaseModel):
    events: list[Event]


@app.post("/analytics")
def analytics(
    body: RequestBody,
    x_api_key: str = Header(None)
):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

    total_events = len(body.events)
    unique_users = len({e.user for e in body.events})
    revenue = sum(e.amount for e in body.events if e.amount > 0)

    totals = defaultdict(float)
    for e in body.events:
        if e.amount > 0:
            totals[e.user] += e.amount

    top_user = max(totals.items(), key=lambda x: x[1])[0] if totals else ""

    return {
        "email": EMAIL,
        "total_events": total_events,
        "unique_users": unique_users,
        "revenue": revenue,
        "top_user": top_user,
    }