from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

notifications = []

class Notification(BaseModel):
    ticket_id: int
    ticket_status: str
    message:str

@app.get("/")
def home():
    return {"message": "Notification Service is running"}

@app.post("/notify")
def send_notification(notification: Notification):
    new_notification = {
        "ticket_id": notification.ticket_id,
        "ticket_status": notification.ticket_status,
        "message": notification.message
    }
    notifications.append(new_notification)
    return new_notification

@app.get("/notifications")
def get_notifications():
    return notifications