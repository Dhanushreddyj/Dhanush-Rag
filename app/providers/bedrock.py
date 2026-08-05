"""
Bedrock LLM and embedding providers for Amazon Bedrock.

This module provides:
- BedrockLLMProvider — chat completions via Bedrock runtime
- BedrockEmbeddingProvider — embeddings via Bedrock runtime

Usage (development):
    export BEDROCK_MODEL_ID="anthropic.anthropus-v1-0"
    export BEDROCK_EMBEDDING_MODEL_ID="amazon.bedrock-inference-provisioned-us-east-1:ai21.0.3.0"
    python -c "from app.providers.bedrock import BedrockLLMProvider; ..."

Usage (production):
    Configure via environment variables or pass credentials explicitly.
"""

import json
import asyncio
from typing import List, Dict, Any, Optional
from botocore.runtime import RuntimeClient


class BedrockLLMProvider:
    """Amazon Bedrock LLM provider."""

    def __init__(
        self,
        region_name: str = "us-east-1",
        model_id: str = "",
        credentials: Any = None,
    ):
        self.region_name = region_name
        self.model_id = model_id
        self.credentials = credentials or {}

        if not self.model_id:
            raise ValueError("model_id is required for BedrockLLMProvider")

        self.client = RuntimeClient(
            region_name=region_name,
            **self.credentials,
        )

    def _build_messages(self, system_prompt: Optional[str], messages: List[Dict[str, str]]) -> List[Dict]:
        """Build the message list with optional system prompt."""
        if system_prompt:
            return [{"role": "system", "content": system_prompt}] + messages
        return messages

    def generate_answer(
        self,
        query: str,
        context_docs: List[Dict[str, Any]],
        system_prompt: Optional[str] = None,
        temperature: float = 0.2,
        max_tokens: int = 1024,
    ) -> Dict[str, Any]:
        """Generate an answer using Bedrock."""
        messages = self._build_messages(
            system_prompt=system_prompt,
            messages=[{"role": "user", "content": query}],
        )

        response = self.client.invoke_model(
            modelId=self.model_id,
            regionName=self.region_name,
            body=json.dumps({
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens,
            }),
        )

        content = json.loads(response["body"].read().decode())
        answer = content.get("content", [{}])[0].get("text", "")

        return {
            "answer": answer.strip(),
            "model_used": self.model_id,
        }

    def generate_stream(
        self,
        query: str,
        context_docs: List[Dict[str, Any]],
        system_prompt: Optional[str] = None,
        temperature: float = 0.2,
        max_tokens: int = 1024,
    ):
        """Streaming generator — yields chunks as they arrive."""
        messages = self._build_messages(
            system_prompt=system_prompt,
            messages=[{"role": "user", "content": query}],
        )

        response = self.client.invoke_model_with_streaming_response(
            modelId=self.model_id,
            regionName=self.region_name,
            body=json.dumps({
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens,
            }),
        )

        for event in response["stream"]:
            if "chunk" in event:
                chunk = json.loads(event["chunk"].get("bytes", b"{}").decode())
                delta = chunk.get("delta", {}).get("content_block_delta", {}).get("text", "")
                if delta:
                    yield delta


class BedrockEmbeddingProvider:
    """Amazon Bedrock embedding provider."""

    def __init__(
        self,
        region_name: str = "us-east-1",
        model_id: str = "",
        credentials: Any = None,
    ):
        self.region_name = region_name
        self.model_id = model_id
        self.credentials = credentials or {}

        if not self.model_id:
            raise ValueError("model_id is required for BedrockEmbeddingProvider")

        self.client = RuntimeClient(
            region_name=region_name,
            **self.credentials,
        )

    def embed_query(self, text: str) -> List[float]:
        """Generate embeddings for a single query."""
        response = self.client.invoke_model(
            modelId=self.model_id,
            regionName=self.region_name,
            body=json.dumps({"input": [{"data": text}]}),
        )

        content = json.loads(response["body"].read().decode())
        embeddings = [item.get("vector", []) for item in content.get("output", {}).get("texts", [])]
        return embeddings[0] if len(embeddings) == 1 else []

    async def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for multiple documents (async)."""
        tasks = [self.embed_query(text) for text in texts]
        results = await asyncio.gather(*tasks)
        return list(results)


__all__ = ["BedrockLLMProvider", "BedrockEmbeddingProvider"]
