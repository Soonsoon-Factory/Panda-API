[Read this document in Korean (한국어로 보기) 🇰🇷](README.ko.md)

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
  <b>AI integrated API service based on FastAPI</b><br>
  <span style="color:#56B16F">OpenAI · DeepSeek Supports various AI functions</span>
</p>

## ✨ About The Project

PandaAPI is a service that integrates complex cloud-based AI services into a single API so that anyone can use them easily. In particular, it aims to **provide a development environment where students and amateur developers can test various AIs in a fun and easy way and create their own projects**.

Without having to worry about different authentication methods and endpoints, you can easily use various latest AI models with a single API Key issued by PandaAPI and a standardized request format.




## 🚀 Key Features

- 🤝 **Linking OpenAI and DeepSeek models**
- 🔑 **API Key Issuance and Authentication**
- 🔀 **Separate endpoints by model**
- 🔄 **Support for streaming AI response**

<br>

## 📁 Folder structure
```bash
PandaAPI/
├── pandaio
│   ├── __init__.py
│   ├── __pycache__
│   ├── api_key_manager.py     # Handles API key issuance
│   ├── auth.py                # API Key authentication module
│   ├── config.py              # Maps variables from the .env file
│   ├── main.py                # FastAPI entry point
│   ├── models.py              # Contains the DB schema for API keys
│   └── routes/api_router.py   # Normalizes I/O for the actual AI API calls
├─ .env                        # Environment variable template
├─ requirements.txt            # Python dependency list
├─ README.md
```

<br>

## 🖥️ Run Environment & Requirements

- **OS:** Ubuntu 22.04+, MacOS Ventura+ (Windows also supported)
- **Python:** 3.9 or higher (recommended: 3.11)
- **Required packages:** fastapi, uvicorn, httpx, python-dotenv, sqlalchemy, databases


## ✅ Supported Services

> [!NOTE]
> Currently, PandaAPI is built around using endpoints for AI models deployed via **Azure**.

### Currently supported
* **Azure OpenAI Service**
* **Azure DeepSeek Service**

### Future support planned
* Amazon Web Services (AWS) Bedrock
* Other cloud-based AI services

---

<br>

## ⚡️ How to install & run (Quick Start)

### 1. Clone & Enter Repository

```bash
git clone https://github.com/pandag02/PandaAPI.git
cd PandaAPI
```



### 2. Environment Setup

**Create a `.env` file in the project root and add the following content:**

```env
# 🔑 Base keys for AI services
OPENAI_API_KEY=<YOUR_OPENAI_API_KEY>
DEEPSEEK_API_KEY=<YOUR_DEEPSEEK_API_KEY>

# 💬 Endpoints for GPT models
GPT4O_ENDPOINT=https://your-openai-endpoint.azure.com/openai/deployments/gpt-4o/chat/completions

GPT4O_MINI_ENDPOINT=https://your-openai-endpoint.azure.com/openai/deployments/gpt-4o-mini/chat/completions

GPT41_ENDPOINT=https://your-openai-endpoint.azure.com/openai/deployments/gpt-4.1/chat/completions

# 🐳 Endpoints for DeepSeek models
DEEPSEEK_R1_ENDPOINT=https://your-deepseek-endpoint.azure.com/openai/deployments/DeepSeek-R1/chat/completions

DEEPSEEK_V3_ENDPOINT=https://your-deepseek-endpoint.azure.com/openai/deployments/DeepSeek-V3/chat/completions
````
> [!TIP]  
> Since only the deployments part of the URL changes, you can reduce the number of entries in `.env` by modifying the code to construct the URL dynamically.

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Local Server
If you check the code in `pandaio/main.py`, you will see separate configurations for local testing and deployment. If you intend to deploy to a server, comment out the local test section and use the deployment section.
```python
# For local testing with uvicorn main:app --reload
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)

# For deployment
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run("pandaio.main:app", host="0.0.0.0", port=8000, reload=True)
```


Command to run for local testing:

> [!IMPORTANT]
> Do not close the terminal where the local server is running. Keep it open and use a new terminal to send requests and check responses.

```bash
uvicorn pandaio.main:app --host 0.0.0.0 --port 8000 --reload
```

### 4. Generate an API Key

While the server is running, use the following command to generate an API key:

```bash
curl -X POST http://127.0.0.1:8000/auth/generate-api-key/ \
     -H "Content-Type: application/json" \
     -d '{"expiration_days": 7}'
```

<br>

## 💡 **API Usage Example**


<summary><b>Calling the OpenAI Model</b></summary>

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
<summary><b>Calling the DeepSeek Model</b></summary>

> [!IMPORTANT]
> With DeepSeek, if the `max_tokens` value is too low, the response might contain inference details instead of the AI's answer. If the response seems strange, try increasing the `max_tokens` value in your request (minimum 400 recommended).(최소 400)

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

<summary><h3><b>Return response</b></summary>


```bash
{
    "model": "gpt-4o",
    "response": "Quantum computing is a type of computation that uses quantum mechanics."
    "total_tokens": "121" 
}
```

---

## ✍️ Author

This project was created as part of a study in the Academy Mentoring Program at **[SOONSOO FACTORY](https://soonsoons.com)**.

* **Name:** 이소연 (Lee Soyeon)
* **Affiliation:** Department of Computer Science and Engineering, Dongguk University
* **Email:** <panda_g02@naver.com>



<p align="center">
  <sub>
    PandaAPI · Powered by FastAPI <br/>
    Support: panda_g02@naver.com
  </sub>
</p>
