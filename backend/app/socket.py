import socketio

# Create the Socket.IO server
sio = socketio.AsyncServer(
    async_mode="asgi",
    cors_allowed_origins="*"
)

# Connection events
@sio.event
async def connect(sid, environ):
    print(f"Client connected: {sid}")

@sio.event
async def disconnect(sid):
    print(f"Client disconnected: {sid}")

@sio.event
async def join_room(sid, data):
    """Client joins their personal room using their user_id."""
    user_id = data.get("user_id")
    if user_id:
        await sio.enter_room(sid, user_id)
        print(f"Client {sid} joined room {user_id}")

# Notification emitter — call this from anywhere in the app
async def send_notification(user_id: str, type: str, message: str):
    await sio.emit(
        "notification",
        {
            "type": type,
            "message": message,
        },
        room=user_id,
    )