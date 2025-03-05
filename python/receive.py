import asyncio
import websockets
import os
import time
from io import BytesIO
from PIL import Image, UnidentifiedImageError

# Define save path
SAVE_DIR = "saved"

# Ensure the directory exists
if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

def is_valid_image(image_bytes):
    """Check if the received bytes form a valid image."""
    try:
        Image.open(BytesIO(image_bytes))
        return True
    except UnidentifiedImageError:
        print("Invalid image received.")
        return False

async def handle_connection(websocket, path):
    """Handles incoming WebSocket connections."""
    while True:
        try:
            message = await websocket.recv()
            print(f"Received data size: {len(message)} bytes")
            
            if len(message) > 5000:  # Ensure it's an image, not noise
                if is_valid_image(message):
                    filename = os.path.join(SAVE_DIR, f"image_{int(time.time())}.jpg")
                    with open(filename, "wb") as f:
                        f.write(message)
                    print(f"Saved image as {filename}")

        except websockets.exceptions.ConnectionClosed:
            print("Client disconnected.")
            break

async def main():
    """Starts the WebSocket server."""
    server = await websockets.serve(functools.partial(handle_connection, path = None), '0.0.0.0', 3001)
    print("Server started on ws://0.0.0.0:3001")
    await server.wait_closed()

asyncio.run(main())
