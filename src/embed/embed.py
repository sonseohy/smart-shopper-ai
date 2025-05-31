import os
import csv
from dotenv import load_dotenv

from pinecone import Pinecone, ServerlessSpec
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document

from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore


def main():
    load_dotenv()
    pinecone_api_key = os.environ.get("PINECONE_API_KEY")
    openai_api_key = os.environ.get("OPENAI_API_KEY")

    pc = Pinecone(api_key=pinecone_api_key)
    index_name = "daily-goods-prices"
    dimension = 3072

    if index_name not in pc.list_indexes().names():
        pc.create_index(
            name=index_name,
            dimension=dimension,
            metric='cosine',
            spec=ServerlessSpec(cloud='aws', region='us-east-1')
        )
        print(f"새로운 Pinecone 인덱스 생성: {index_name}")
    else:
        print(f"이미 존재하는 인덱스: {index_name}")

    csv_file_path = "data.csv"
    docs = []
    with open(csv_file_path, "r", encoding="euc-kr") as f:
        reader = csv.DictReader(f, delimiter=",")
        for row in reader:
            content = (
                f"상품명: {row.get('상품명', '')}\n"
                f"조사일: {row.get('조사일', '')}\n"
                f"판매가격: {row.get('판매가격', '')}\n"
                f"판매업소: {row.get('판매업소', '')}\n"
                f"제조사: {row.get('제조사', '')}\n"
                f"세일여부: {row.get('세일여부', '')}\n"
                f"원플러스원: {row.get('원플러스원', '')}\n"
            )
            meta = {
                "상품명": row.get('상품명', ''),
                "조사일": row.get('조사일', ''),
                "판매가격": row.get('판매가격', ''),
                "판매업소": row.get('판매업소', ''),
                "제조사": row.get('제조사', ''),
                "세일여부": row.get('세일여부', ''),
                "원플러스원": row.get('원플러스원', ''),
            }
            docs.append(Document(page_content=content, metadata=meta))

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    split_docs = text_splitter.split_documents(docs)

    embedding_openai = OpenAIEmbeddings(
        openai_api_key=openai_api_key,
        model="text-embedding-3-large"
    )

    PineconeVectorStore.from_documents(
        split_docs,
        embedding_openai,
        index_name=index_name
    )
    print("업로드 완료")


if __name__ == "__main__":
    main()
