from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

tickets = []

class TicketClass(BaseModel):
    title: str
    description: str

@app.get("/") # get->read data
def home():
    return {"message": "Tickets Service is running"}

@app.post("/tickets") # post->create data
def create_ticket(ticket: TicketClass):
    new_ticket = {
        "id": len(tickets) + 1,
        "title": ticket.title,
        "description": ticket.description,
        "status": "open"
    }  
    tickets.append(new_ticket)
    return new_ticket

@app.get("/tickets/{ticket_id}") # get->read data
def get_ticket_by_id(ticket_id: int):
    for t in tickets:
        if t["id"] == ticket_id:
            return t
    return {"error": "Ticket not found"}

@app.get("/tickets")
def get_all_tickets():
    return tickets
