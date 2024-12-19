from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

app = FastAPI()

class Part(BaseModel):
    id: int
    name: str
    model_path: str
    position: dict
    scale: dict

parts = [
    Part(
        id=1,
        name="Placa-Mãe",
        model_path="/static/models/atx_motherboard_sample.glb",
        position={"x": 0, "y": 0, "z": -0.1},
        scale={"x": 1, "y": 1, "z": 1},
    ),
    Part(
        id=2,
        name="Placa de Vídeo",
        model_path="/static/models/gpu_sample.glb",
        position={"x": 0, "y": 0.5, "z": 0},
        scale={"x": 0.5, "y": 0.5, "z": 0.5},
    ),
]

@app.get("/api/parts")
def get_parts():
    return parts

# Servir arquivos estáticos (modelos, imagens, etc.)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Servir o arquivo HTML do frontend
@app.get("/", response_class=HTMLResponse)
def serve_frontend():
    with open("templates/index.html", "r") as file:
        html = file.read()
    return HTMLResponse(content=html)