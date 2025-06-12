![Panda.io Banner](image/PandaAPIBanner.png)

<h1 align="center">PandaAPI <span style="font-size:1.2em;">🌿🐼</span></h1>

<p align="center">
  <a href="https://fastapi.tiangolo.com/">
  <img src="https://img.shields.io/static/v1?label=FastAPI&message=%3E=0.95.0&color=green&logo=FastAPI" alt="FastAPI">
  </a>
  <a href="https://www.python.org/">
  <img src="https://img.shields.io/static/v1?label=Python&message=%3E=3.9%20|%203.13&color=blue&logo=python" alt="Python">
  </a>
</p>


<p align="center">
  <b>FastAPI 기반 AI 통합 API 서비스</b><br>
  <span style="color:#56B16F">OpenAI · DeepSeek 다양한 AI 기능 지원</span>
</p>

## ✨ 프로젝트 소개 (About The Project)

PandaAPI는 복잡한 클라우드 기반 AI 서비스를 하나의 API로 통합하여, 누구나 손쉽게 사용할 수 있도록 만들어진 서비스입니다. 특히 **학생이나 아마추어 개발자들이 여러 AI를 재미있고 간편하게 테스트하며 자신만의 프로젝트를 만들어 볼 수 있는 개발 환경을 제공하는 것**을 목표로 합니다.

각기 다른 인증 방식과 엔드포인트를 신경 쓸 필요 없이, PandaAPI가 발급하는 단일 API Key와 표준화된 요청 형식으로 다양한 최신 AI 모델을 손쉽게 사용할 수 있습니다.




## 🚀 주요 기능

- 🤝 **OpenAI 및 DeepSeek 모델 연동**
- 🔑 **API Key 발급 및 인증**
- 🔀 **모델별 엔드포인트 분리**
- 🔄 **스트리밍 방식 AI 응답 지원**

<br>

## 📁 폴더 구조
```bash
PandaAPI/
├── pandaio
│   ├── __init__.py
│   ├── __pycache__
│   ├── api_key_manager.py # 키 발급 관련 부분
│   ├── auth.py # API Key 인증 모듈
│   ├── config.py # env 파일과 변수를 맵핑하는 파일
│   ├── main.py # FastAPI 엔트리포인트
│   ├── models.py # 키 값과 관련된 DB 스키마 존재
│   └── routes/api_router.py # 실제 AI API 입출력을 정규화하는 부분
├─ .env # 환경변수 템플릿
├─ requirements.txt # Python 의존성 목록
├─ README.md
```

<br>

## 🖥️ 실행 환경 & 요구사항

- **OS:** Ubuntu 22.04+, MacOS Ventura+ (Windows도 지원)
- **Python:** 3.9 이상 (권장: 3.11)
- **필수 패키지:** fastapi, uvicorn, httpx, python-dotenv, sqlalchemy, databases


## ✅ 지원하는 서비스 (Supported Services)

> [!NOTE]
> 현재 PandaAPI는 **Azure**를 통해 배포된 AI 모델의 엔드포인트를 사용하는 것을 기준으로 제작되었습니다.

### 현재 지원
* **Azure OpenAI Service**
* **Azure DeepSeek Service**

### 향후 지원 예정
* Amazon Web Services (AWS) Bedrock
* 기타 클라우드 기반 AI 서비스

---

<br>

## ⚡️ 설치 & 실행 방법 (빠른 시작)

### 1. 저장소 클론 & 진입

```bash
git clone https://github.com/pandag02/PandaAPI.git
cd PandaAPI
```



### 2. 환경 설정

**프로젝트 루트에 `.env` 파일을 생성하고 아래 내용을 추가하세요:**

```env
# 🔑 기본 AI 사용 키
OPENAI_API_KEY=<YOUR_OPENAI_API_KEY>
DEEPSEEK_API_KEY=<YOUR_DEEPSEEK_API_KEY>

# 💬 GPT의 END_POINT들
GPT4O_ENDPOINT=https://your-openai-endpoint.azure.com/openai/deployments/gpt-4o/chat/completions

GPT4O_MINI_ENDPOINT=https://your-openai-endpoint.azure.com/openai/deployments/gpt-4o-mini/chat/completions

GPT41_ENDPOINT=https://your-openai-endpoint.azure.com/openai/deployments/gpt-4.1/chat/completions

# 🐳 DeepSeek의 END_POINT
DEEPSEEK_R1_ENDPOINT=https://your-deepseek-endpoint.azure.com/openai/deployments/DeepSeek-R1/chat/completions

DEEPSEEK_V3_ENDPOINT=https://your-deepseek-endpoint.azure.com/openai/deployments/DeepSeek-V3/chat/completions
````
> [!TIP]  
> deployments 부분만 변경되는 것이기에, 코드에서 수정하면 `.env` 등록을 줄일 수 있습니다. 

### 3. 요구사항 설치

```bash
pip install -r requirements.txt
```

### 4. 로컬 서버 실행
현재 `pandaio/main.py`의 코드를 확인하면 로컬 테스트와 배포가 따로 있는 것을 확인할 수 있습니다. 만일 서버에 배포하려고 하는 경우, 로컬 테스트용을 주석처리하고 배포용 부분을 사용하면 됩니다. 
```python
# 로컬 테스트용 uvicorn main:app --reload
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)

# 배포용
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run("pandaio.main:app", host="0.0.0.0", port=8000, reload=True)
```


로컬 테스트 실행 명령어

> [!IMPORTANT]
> 로컬 서버를 실행한 터미널을 닫지 마세요. 열어둔 상태로 새로운 터미널을 열어서 입력과 출력을 확인하세요.

```bash
uvicorn pandaio.main:app --host 0.0.0.0 --port 8000 --reload
```

### 4. API Key 발급

서버가 실행 중일 때, 아래 명령어로 API Key를 발급받으세요:

```bash
curl -X POST http://127.0.0.1:8000/auth/generate-api-key/ \
     -H "Content-Type: application/json" \
     -d '{"expiration_days": 7}'
```

<br>

## 💡 **API 사용 예시**


<summary><b>OpenAI 모델 호출</b></summary>

```bash
curl -X POST http://127.0.0.1:8000/api/process/ \
     -H "Content-Type: application/json" \
     -H "api-key: <YOUR_API_KEY>" \
     -d '{
           "model": "gpt-4o",
           "system_prompt": "You are helpful AI",
           "prompt": "What is quantum computing?",
           "max_tokens": 150
         }'
```
<br>
<summary><b>DeepSeek 모델 호출</b></summary>

> [!IMPORTANT]
> DeepSeek에서 토큰 값이 부족하면 response에 AI 답변 대신 추론 부분이 나오게 됩니다. 만일 답변이 이상하다면 입력 부분의 max_tokens부분을 늘려주세요.(최소 400)

```bash
curl -X POST http://127.0.0.1:8000/api/process/ \
     -H "Content-Type: application/json" \
     -H "api-key: <YOUR_API_KEY>" \
     -d '{
           "model": "deepseek-r1",
           "system_prompt": "You are helpful AI",
           "prompt": "Tell me about the latest AI trends.",
           "max_tokens": 400
         }'
```

<summary><h3><b>반환 값</b></summary>


```bash
{
    "model": "gpt-4o",
    "response": "Quantum computing is a type of computation that uses quantum mechanics."
    "total_tokens": "121" 
}
```

---

## ✍️ 제작자 (Author)

이 프로젝트는 **[SOONSOO FACTORY](https://soonsoons.com) 의 아카데미 멘토링 프로그램** 의 스터디 일환으로 제작되었습니다.

* **이름:** 이소연 (Lee Soyeon)
* **소속:** 동국대학교 컴퓨터공학부 4학년
* **이메일:** <panda_g02@naver.com>



<p align="center">
  <sub>
    PandaAPI · Powered by FastAPI <br/>
    Support: panda_g02@naver.com
  </sub>
</p>
