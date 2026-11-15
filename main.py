import os
import httpx
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Truyen AI Backend")

# Lấy API Key từ biến môi trường (sẽ cài đặt trên Render ở bước sau)
AION_API_KEY = os.environ.get("AION_API_KEY")
AION_BASE_URL = "https://api.aionlabs.ai/v1"

class StoryRequest(BaseModel):
    prompt: str

@app.get("/")
def read_root():
    return {"status": "Bộ não đang chạy!", "service": "Truyen AI Backend"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/v1/generate-story")
async def generate_story(request: StoryRequest):
    if not AION_API_KEY:
        raise HTTPException(status_code=500, detail="Chưa cấu hình AION_API_KEY trên server.")
    
    headers = {
        "Authorization": f"Bearer {AION_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "aion-labs/aion-3.5",
        "messages": [
            {"role": "system", "content": "Bạn là một nhà văn sáng tạo, chuyên viết truyện ngắn bằng tiếng Việt với văn phong lôi cuốn."},
            {"role": "user", "content": request.prompt}
        ],
        "temperature": 0.8
    }

    async with httpx.AsyncClient(timeout=60.0) as client:
        try:
            response = await client.post(f"{AION_BASE_URL}/chat/completions", headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()
            story_text = data["choices"][0]["message"]["content"]
            return {"story": story_text}
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail=f"Lỗi từ Aion Labs: {e.response.text}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Lỗi không xác định: {str(e)}")
