from fastapi import FastAPI
from pydantic import BaseModel
import httpx

app = FastAPI()

TICKET_SERVICE_URL = "http://ticket-service:8000"
NOTIFICATION_SERVICE_URL = "http://notification-service:8002"

class AssignTicket(BaseModel):
    ticket_id: int
    agent_name: str

class ResponseTicket(BaseModel):
    ticket_id: int
    agent_name: str
    message: str

class ResolveTicket(BaseModel):
    ticket_id: int
    agent_name: str

responses = []
assignments = []
resolved = []

@app.get("/")
def home():
    return {"message": "Support Service is running"}

# assigning a ticket to an agent
# means an agent catches a ticket and starts working on it
# and updating the ticket status to "in-progress"
@app.post("/assign")
def assign_ticket(assign: AssignTicket):
    new_assignment = { 
        "ticket_id": assign.ticket_id,
        "agent_name": assign.agent_name,
        "status": "assigned"
    }
    assignments.append(new_assignment)

    httpx.put(f"{TICKET_SERVICE_URL}/tickets/{assign.ticket_id}", params={"status": "in-progress-assigned"})
    return new_assignment

@app.get("/assignments")
def get_assignments():
    return assignments

# responding to a ticket 
# means an agent has worked on the ticket and is providing a response to the customer
@app.post("/respond")
def respond_ticket(response: ResponseTicket):
    new_response = {
        "ticket_id": response.ticket_id,
        "agent_name": response.agent_name,
        "message": response.message,
        "status": "responded"
    }
    responses.append(new_response)

    httpx.post(f"{NOTIFICATION_SERVICE_URL}/notify",  json= {
        "ticket_id": response.ticket_id,
        "ticket_status": "in-progress-responded",
        "message": f"Agent \"{response.agent_name}\" has responded to your ticket"
    })
    httpx.put(f"{TICKET_SERVICE_URL}/tickets/{response.ticket_id}", params={"status": "in-progress-responded"})
    return new_response

@app.get("/responses")
def get_responses():
    return responses

# resolving a ticket
# means an agent has finished working on the ticket and is marking it as resolved
@app.post("/resolve")
def resolve_ticket(resolve: ResolveTicket):
    new_resolution = {
        "ticket_id": resolve.ticket_id,
        "agent_name": resolve.agent_name,
        "status": "resolved"
    }
    resolved.append(new_resolution)

    httpx.post(f"{NOTIFICATION_SERVICE_URL}/notify",  json= {
        "ticket_id": resolve.ticket_id,
        "ticket_status": "resolved",
        "message": f"Agent \"{resolve.agent_name}\" has resolved your ticket"
    })
    httpx.put(f"{TICKET_SERVICE_URL}/tickets/{resolve.ticket_id}", params={"status": "resolved"})
    return new_resolution

@app.get("/resolved")
def get_resolved():
    return resolved

@app.get("/tickets")
def get_tickets():
    response = httpx.get(f"{TICKET_SERVICE_URL}/tickets")
    return response.json()