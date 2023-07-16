import uuid
from pathlib import Path
from typing import Optional, Tuple

import fastapi
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from modal import Dict, Image, Mount, NetworkFileSystem, Stub, asgi_app

from .common import stub

from .inference import OpenLlamaModel


assets_path = Path(__file__).parent / "client"

stub.chat_histories = Dict.new()


@stub.function(
    mounts=[Mount.from_local_dir(assets_path, remote_path="/assets")]
)
@asgi_app()
def transformer():
    app = fastapi.FastAPI()

    @app.post("/chat")
    def chat(body: dict = fastapi.Body(...)):
        message = body["message"]
        chat_id = body.get("id")
        message_id, response = generate_response(message, chat_id)
        return JSONResponse({"id": message_id, "response": response})

    app.mount("/", StaticFiles(directory="/assets", html=True))
    return app


@stub.function()
def generate_response(
    message: str, chat_id: Optional[str] = None
) -> Tuple[Optional[str], str]:
    # Hackathon 🤷
    pod = "Lex Fridman Podcast"
    model = OpenLlamaModel.remote(pod)
    response = model.generate(
        input_prompt=message,
        do_sample=True,
        temperature=0.3,
        top_p=0.85,
        top_k=40,
        num_beams=1,
        max_new_tokens=6000,
        repetition_penalty=1.2,
    )
    return chat_id, response


@stub.local_entrypoint()
def test_response(message: str):
    pod = "Lex Fridman Podcast"
    model = OpenLlamaModel.remote(pod)
    _, response = generate_response(model, message)
    print(response)