from firebase_admin import messaging

def send_to_3days(registration_token):
    # This registration token comes from the client FCM SDKs.
    registration_token = registration_token

    # See documentation on defining a message payload.
    message = messaging.Message(
    notification=messaging.Notification(
        title='3일간 플로깅을 진행하지 않았어요!',
        body='앱에 접속해서 함께 플로깅해요',
    ),
    token=registration_token,
    )

    try:
        response = messaging.send(message)
        # Response is a message ID string.
        print('Successfully sent message:', response)
    except Exception as e:
        print('예외가 발생했습니다.', e)

def send_to_7days(registration_token):
    # This registration token comes from the client FCM SDKs.
    registration_token = registration_token

    # See documentation on defining a message payload.
    message = messaging.Message(
    notification=messaging.Notification(
        title='일주일간 플로깅을 진행하지 않았어요!',
        body='앱에 접속해서 함께 플로깅해요',
    ),
    token=registration_token,
    )

    try:
        response = messaging.send(message)
        # Response is a message ID string.
        print('Successfully sent message:', response)
    except Exception as e:
        print('예외가 발생했습니다.', e)

def send_to_challenge(registration_token):
    # This registration token comes from the client FCM SDKs.
    registration_token = registration_token

    # See documentation on defining a message payload.
    message = messaging.Message(
    notification=messaging.Notification(
        title='챌린지 행성이 갱신되었습니다.',
        body='앱에 접속해서 확인해주세요!',
    ),
    token=registration_token,
    )

    try:
        response = messaging.send(message)
        # Response is a message ID string.
        print('Successfully sent message:', response)
    except Exception as e:
        print('예외가 발생했습니다.', e)
