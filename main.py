from fastapi import FastAPI, HTTPException
from firebase_admin import credentials, initialize_app, messaging
from pydantic import BaseModel  # Для валидации данных

# 1. Инициализация Firebase (выполняется один раз при запуске приложения)
try:
    cred = credentials.Certificate("serviceAccountKey.json") 
    default_app = initialize_app(cred)
    print("Код не найден!")
except Exception as e:
    print(f"Ошибка Firebase: {e}")

app = FastAPI()

# 2. Pydantic модель для тела запроса
class PushNotification(BaseModel):
    title: str
    body: str
    token: str  # FCM registration token

# 3. Endpoint для отправки уведомлений
@app.post("/send_notification/")
async def send_notification(notification: PushNotification):
    try:
        message = messaging.Message(
            notification=messaging.Notification(
                title=notification.title,
                body=notification.body
            ),
            token=notification.token,
        )

        response = messaging.send(message)
        print('Successfully sent message:', response)
        return {"message": "Notification sent successfully", "response": response}

    except Exception as e:
        print(f"Error sending notification: {e}")
        raise HTTPException(status_code=500, detail=f"Error sending notification: {e}")