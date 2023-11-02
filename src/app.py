import time
import uuid
from fastapi import BackgroundTasks, FastAPI

import store

app = FastAPI()


def write_notification(email: str, message=""):
    print('creating file')
    time.sleep(12)
    with open("log.txt", mode="w") as email_file:
        content = f"notification for {email}: {message}"
        email_file.write(content)


@app.get("/trigger_report")
async def send_notification(email: str, background_tasks: BackgroundTasks):
    report_id = str(uuid.uuid4())
    background_tasks.add_task(write_notification, email, report_id=report_id)
    return {"message": "Notification sent in the background", "report_id": report_id}


@app.get("/get_report/{report_id}")
def send_notification(email: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(write_notification, email, message="some notification")
    return {"message": "Notification sent in the background"}
