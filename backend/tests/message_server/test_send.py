import pytest
import websockets
import json
from src.schemas import SendGroupMessage, SendUserMessage


pytestmark = pytest.mark.asyncio

ws: websockets.WebSocketClientProtocol


@pytest.fixture
async def ws():
    websocket = await websockets.client.Connect(
        "ws://localhost:6789",
        origin="localhost",
        extra_headers={"authorization": "user@example.com:string"},
    )
    yield websocket
    await websocket.close()


async def test_send_group(ws: websockets.WebSocketClientProtocol):
    message = SendGroupMessage(
        message="group", channel_uuid="2a1d80c3-7d5d-11eb-9220-fc4596ed0d8e"
    )
    await ws.send(
        json.dumps(["send-group-message", {"message": message.dict()}]).encode()
    )
    assert json.loads(await ws.recv()) == {"code": 200, "message": True}
    message = SendGroupMessage(
        message="group", channel_uuid="2a1d80c3-7d5d-11eb-9220-fc4596ed0d8f"
    )
    await ws.send(
        json.dumps(["send-group-message", {"message": message.dict()}]).encode()
    )
    assert json.loads(await ws.recv()) == {"code": 404, "message": "channel not found"}


async def test_send_personal(ws: websockets.WebSocketClientProtocol):
    message = SendUserMessage(message="personal", name="test-user", hash="89118")
    await ws.send(
        json.dumps(["send-user-message", {"message": message.dict()}]).encode()
    )
    assert json.loads(await ws.recv()) == {"code": 200, "message": True}
    message = SendUserMessage(message="personal", name="test-user", hash="89119")
    await ws.send(
        json.dumps(["send-user-message", {"message": message.dict()}]).encode()
    )
    assert json.loads(await ws.recv()) == {"code": 404, "message": "user not found"}


async def test_receive(ws: websockets.WebSocketClientProtocol):
    await ws.send(json.dumps(["subscribe-for-messages", {}]).encode())
    messages = [await ws.recv() for _ in range(2)]
    assert "personal".encode() in messages
    assert "group".encode() in messages
