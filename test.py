import json

def generate_email(event_data, user_data=None):
    subject = event_data["email"]["subject"]
    message = event_data["email"]["message"]
    if user_data:
        for key, value in user_data.items():
            message = message.replace("{" + key + "}", str(value))
    return subject, message

with open("./config/subjects.json", "r", encoding='utf-8') as f:
    data = json.load(f)

for notification in data["messages"]:
    if notification["event_name"] == "update_service":
        subject, message = generate_email(notification)
        print(subject)
        print(message)