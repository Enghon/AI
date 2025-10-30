from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import StreamingResponse, HTMLResponse
from langchain_community.chat_models import ChatOllama
from langchain_core.messages import HumanMessage
import asyncio
import re

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# 初始化 Ollama 模型
chat_model = ChatOllama(
    model="deepseek-r1:latest",
    base_url="http://127.0.0.1:11434",
    temperature=0.7,
    verbose=False
)

def clean_chunk(text: str) -> str:
    """只清理 <think> 标签，保留公式"""
    return re.sub(r'</?think>', '', text, flags=re.IGNORECASE)

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/api/chat")
async def chat_stream(request: Request):
    data = await request.json()
    user_message = data.get("message", "")

    async def generate():
        messages = [HumanMessage(content=user_message)]
        try:
            async for chunk in chat_model.astream(messages):
                cleaned = clean_chunk(chunk.content)
                yield f"data: {cleaned}\n\n"
                await asyncio.sleep(0.01)
        except Exception as e:
            yield f"data: [ERROR] {str(e)}\n\n"
        yield "data: [DONE]\n\n"

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={"X-Accel-Buffering": "no"}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8083)
