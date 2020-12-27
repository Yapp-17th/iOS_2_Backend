from firebase_admin import messaging

def send_to_push(registration_token,title,body):
    # This registration token comes from the client FCM SDKs.
    registration_token = registration_token

    # See documentation on defining a message payload.
    message = messaging.Message(
    notification=messaging.Notification(
        title= title,
        body= body,
    ),
    token=registration_token,
    )

    try:
        response = messaging.send(message)
        # Response is a message ID string.
        print('Successfully sent message:', response)
    except Exception as e:
        print('예외가 발생했습니다.', e)

