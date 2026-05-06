from fastapi import FastAPI
import httpx

TICKET_SERVICE_URL = "http://ticket-service:8000"
SUPPORT_SERVICE_URL = "http://support-service:8001"

app = FastAPI()

@app.get("/reports")
def get_reports():
    tickets = httpx.get(f"{TICKET_SERVICE_URL}/tickets").json()
    responses = httpx.get(f"{SUPPORT_SERVICE_URL}/responses").json()

    return{
        "total_tickets": len(tickets),
        "open": len([t for t in tickets if t["status"] == "open"]),
        "resolved": len([t for t in tickets if t["status"] == "resolved"]),
        "in_progress": len([t for t in tickets if t["status"] == "in-progress"]),
        "total_responses": len(responses)
    }