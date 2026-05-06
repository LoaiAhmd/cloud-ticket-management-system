from fastapi import FastAPI
from pydantic import BaseModel
import httpx

app = FastAPI()

TICKET_SERVICE_URL = "http://ticket-service:8000"

@app.get("/")
def home():
    return {"message": "Welcome to the Support Service!"}

class AssignTicket(BaseModel):
    ticket_id: int
    agent_name: str

class ResponseTicket(BaseModel):
    ticket_id: int
    agent_name: str
    message: str

responses = []

@app.post("/assign")
def assign_ticket(assign: AssignTicket):
    return { 
        "ticket_id": assign.ticket_id,
        "agent_name": assign.agent_name,
        "status": "assigned"
    }

@app.post("/respond")
def respond_ticket(response: ResponseTicket):
    new_response = {
        "ticket_id": response.ticket_id,
        "agent_name": response.agent_name,
        "message": response.message,
        "status": "responded"
    }
    responses.append(new_response)
    return new_response

@app.get("/responses")
def get_responses():
    return responses

@app.get("/tickets")
def get_tickets():
    response = httpx.get(f"{TICKET_SERVICE_URL}/tickets")
    return response.json()