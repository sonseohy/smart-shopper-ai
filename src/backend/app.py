# 필요한 패키지 설치:
# pip install fastapi uvicorn openai python-dotenv pinecone-client

from fastapi import FastAPI
from pydantic import BaseModel
from openai import AsyncOpenAI
import os
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from pinecone import Pinecone
from pinecone import ServerlessSpec
import time

# .env 파일 로드
load_dotenv()

# OpenAI 초기화
openai = AsyncOpenAI(api_key=os.getenv("GPT_API_KEY"))

# Pinecone 초기화
pc = Pinecone(
    api_key=os.getenv("PINECONE_API_KEY"),
)

spec = ServerlessSpec(cloud="aws", region="us-east-1")

# Pinecone 인덱스 이름 (여러분의 인덱스 이름으로 변경 가능)
index_name = "daily-goods-prices"
# 인덱스 객체 생성

# connect to index
index = pc.Index(index_name)
time.sleep(1)
# view index stats
index.describe_index_stats()


# FastAPI 앱 생성 및 Swagger 메타데이터 추가
app = FastAPI(
    title="AI 채팅 API",
    description="OpenAI 기반의 AI 비서를 통해 채팅 및 정보를 제공하는 API입니다.",
    version="1.0.0",
)

# CORS 설정 (개발용)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 운영 환경에서는 도메인을 제한하는 것이 좋습니다.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 요청 데이터 모델 정의
class MessageRequest(BaseModel):
    message: str


# "/chat" 엔드포인트: 간단한 채팅 기능 제공
@app.post("/chat", summary="AI 비서와 채팅", tags=["채팅"])
async def chat_endpoint(req: MessageRequest):
    """
    AI 비서에게 메시지를 보내고 응답을 받습니다.

    - **message**: 비서에게 보낼 메시지 내용
    """
    response = await openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "너는 인공지능 챗봇으로, 주어진 데이터를 분석해서 소비자가 구매하고 싶은 물품을 검색해서 현재 판매가격과 할인 또는 원플러스원 물품으로 파는곳을 제공해줘. 데이터에 있는 내용으로만 답하고 내용이 없다면, 잘 모르겠다고 답변해"},
            {"role": "user", "content": req.message},
        ],
    )
    assistant_reply = response.choices[0].message.content
    return {"reply": assistant_reply}


# "/assistant" 엔드포인트: 사전 설정된 AI 비서와 상호작용
@app.post("/assistant", summary="Pinecone + OpenAI 기반 비서", tags=["비서"])
async def assistant_endpoint(req: MessageRequest):
    """
    사전 구성된 AI 비서와 상호작용하며 상세한 응답을 제공합니다.

    - **message**: 비서에게 보낼 메시지 내용
    """
    # 1) 사용자 질문을 임베딩
    embed_response = await openai.embeddings.create(
        input=req.message,
        model="text-embedding-3-large"
    )
    query_embedding = embed_response.data[0].embedding

    # 2) Pinecone 인덱스에 쿼리
    #    - top_k: 몇 개의 문서를 가져올지 (적절히 조정)
    #    - include_metadata: True로 설정하면 원본 텍스트(혹은 기타 메타데이터) 확인 가능
    top_k = 5
    pinecone_result = index.query(
        vector=query_embedding,
        top_k=top_k,
        include_metadata=True
    )

    # 3) Pinecone에서 가져온 상위 문서들의 텍스트를 합쳐서 하나의 문자열로 만든다
    contexts = []
    for match in pinecone_result["matches"]:
        # match["metadata"]에 저장해둔 필드명에 맞게 조정 (예: "text", "content" 등)
        context_text = match["metadata"].get("text", "")
        contexts.append(context_text)

    # 가져온 맥락들을 연결 (너무 길면 일정 길이로 자르거나 요약하는 로직 추가 가능)
    context_str = "\n\n".join(contexts)

    # 4) ChatCompletion 생성
    #    - system_prompt를 통해 역할 부여
    #    - user_prompt에 맥락 + 실제 질문을 함께 전달
    system_prompt = (
        "  너는 인공지능 챗봇으로, 주어진 데이터를 분석해서 소비자가 구매하고 싶은 물품을 검색해서 현재 판매가격과 할인 또는 원플러스원 물품으로 파는곳을 제공해줘. 데이터에 있는 내용으로만 답하고 내용이 없다면, 잘 모르겠다고 답변해."
    )
    user_prompt = (
        f"맥락:\n{context_str}\n\n"
        f"질문:\n{req.message}\n\n"
        "위 정보를 기반으로 최대한 자세히 답변해줘."
    )

    # 비동기 ChatCompletion 사용 (AsyncOpenAI)
    response = await openai.chat.completions.create(
        model="gpt-4o-mini",  # 원하는 모델로 변경 가능
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )
    assistant_reply = response.choices[0].message.content

    return {"reply": assistant_reply}


# uvicorn app:app --reload
# 서버 실행
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
