from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
import httpx
import traceback

from pandaio.auth import verify_api_key  # 절대 경로로 변경
from pandaio.config import (
    OPENAI_API_KEY, 
    DEEPSEEK_API_KEY, 
    GPT4O_ENDPOINT, 
    GPT4O_MINI_ENDPOINT, 
    GPTO3_MINI_ENDPOINT, 
    GPT41_ENDPOINT, 
    DEEPSEEK_R1_ENDPOINT, 
    DEEPSEEK_V3_ENDPOINT
)

router = APIRouter()
# 기본적으로 있는 모델 설정
class AIRequest(BaseModel):
    model: str
    prompt: str
    max_tokens: int = 150
    system_prompt: str

# OpenAI 요청 처리 함수
async def process_openai_request(url: str, payload: dict, api_key: str):
    headers = {
        "Content-Type": "application/json",
        "api-key": api_key
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload, headers=headers)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as http_exc:
        raise HTTPException(status_code=http_exc.response.status_code, detail=http_exc.response.text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

# DeepSeek 요청 처리 함수
async def process_deepseek_request(url: str, payload: dict, api_key: str, model_name: str):
    headers = {
        "Content-Type": "application/json",
        "api-key": api_key,
        "x-ms-model-mesh-model-name": model_name
    }

    try:
        async with httpx.AsyncClient(timeout=300.0) as client:  
            response = await client.post(url, json=payload, headers=headers)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as http_exc:
        print("DeepSeek HTTP error:", http_exc.response.text)
        raise HTTPException(status_code=http_exc.response.status_code, detail=http_exc.response.text)
    except Exception as e:
        print("DeepSeek Exception:", traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"DeepSeek Error: {str(e)}")



# 메인 요청 처리 함수
@router.post("/process/")
async def process_request(request: AIRequest, api_key: str = Depends(verify_api_key)):

    # 모델별 엔드포인트 정의
    model_endpoints = {
        "gpt-4o": GPT4O_ENDPOINT,
        "gpt-4o-mini": GPT4O_MINI_ENDPOINT,
        "gpt-4.1": GPT41_ENDPOINT,
        "deepseek-r1": DEEPSEEK_R1_ENDPOINT,
        "deepseek-v3": DEEPSEEK_V3_ENDPOINT
    }

    # 모델별 API Key 매핑
    api_key_mapping = {
        "gpt-4o": OPENAI_API_KEY,
        "gpt-4o-mini": OPENAI_API_KEY,
        "gpt-4.1": OPENAI_API_KEY,
        "deepseek-r1": DEEPSEEK_API_KEY,
        "deepseek-v3": DEEPSEEK_API_KEY
    }

    # 모델이 지원되지 않는 경우 404 에러 반환
    if request.model not in model_endpoints:
        raise HTTPException(status_code=404, detail="Model not supported")

    # 모델에 맞는 API Key 및 엔드포인트 추출
    external_api_key = api_key_mapping[request.model]
    endpoint_url = model_endpoints[request.model]

    # 공통 페이로드
    payload = {
        "messages": [
            {"role": "system", "content": request.system_prompt},
            {"role": "user", "content": request.prompt}
        ],
        "max_tokens": request.max_tokens,
        "temperature": 0.7
    }

    # OpenAI 모델 처리
    if request.model.startswith("gpt"):
        response = await process_openai_request(
            url=endpoint_url,
            payload=payload,
            api_key=external_api_key
        )

        try:
            content = response["choices"][0]["message"]["content"]
            total_tokens = response.get("usage", {}).get("total_tokens", None)
        except (KeyError, IndexError):
            raise HTTPException(status_code=500, detail="Unexpected OpenAI response format")

    # DeepSeek 모델 처리(R1, V3의 경우 각각 200, 300 이상을 주어야 진짜 답변을 받을 수 있다.)
    elif request.model.startswith("deepseek"):
        model_name = "DeepSeek-R1" if request.model == "deepseek-r1" else "DeepSeek-V3"
        response = await process_deepseek_request(
            url=endpoint_url,
            payload=payload,
            api_key=external_api_key,
            model_name=model_name
        )

        try:
            message = response["choices"][0]["message"]
            # 토큰이 많으면 정상 내용을 적으면 추론 과정을 나오게 한다. 
            content = message.get("content") or message.get("reasoning_content")
            if not content or not content.strip():
                # message 를 내용에 안넣으면 왜 컨탠츠가 없다고 애러가 날까요? 
                raise ValueError("No content or reasoning_content in DeepSeek response" + message)

            total_tokens = response.get("usage", {}).get("total_tokens", None)

        except Exception as e:
            import traceback
            print("Response parsing error:\n", traceback.format_exc())
            raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

    return {
        "model": request.model,
        "response": content,
        "total_tokens": total_tokens
    }
