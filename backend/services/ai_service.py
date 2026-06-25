"""
智析销售AI - AI服务
支持兼容OpenAI的API和本地Ollama
"""
import json
import re
import httpx
from config import (
    AI_PROVIDER,
    API_BASE_URL, API_KEY, API_MODEL,
    OLLAMA_BASE_URL, OLLAMA_MODEL
)
from prompts.sales import build_prompt


async def analyze_with_ai(content: str, user_context: dict = None) -> dict:
    """
    调用AI分析销售对话

    Args:
        content: 对话内容
        user_context: 用户上下文（行业、角色等）

    Returns:
        分析结果字典
    """
    # 构建提示词
    prompt = build_prompt(content, user_context)

    # 根据配置选择AI提供商
    if AI_PROVIDER == "api":
        result = await call_api(prompt)
    elif AI_PROVIDER == "ollama":
        result = await call_ollama(prompt)
    else:
        raise ValueError(f"Unknown AI provider: {AI_PROVIDER}")

    return result


async def call_api(prompt: str) -> dict:
    """调用兼容OpenAI的API"""
    if not API_KEY:
        print("API Key未配置，使用Mock数据")
        return get_mock_response()

    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                f"{API_BASE_URL}/chat/completions",
                headers={
                    "Authorization": f"Bearer {API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": API_MODEL,
                    "messages": [
                        {"role": "system", "content": "你是一位资深的销售分析专家，请严格按照JSON格式输出分析结果。"},
                        {"role": "user", "content": prompt}
                    ],
                    "temperature": 0.7,
                    "max_tokens": 2000
                }
            )
            response.raise_for_status()
            data = response.json()

            # 提取AI回复
            ai_response = data["choices"][0]["message"]["content"]
            print(f"AI原始响应: {ai_response[:200]}...")

            return parse_ai_response(ai_response)
    except Exception as e:
        print(f"API调用失败: {e}")
        return get_mock_response()


async def call_ollama(prompt: str) -> dict:
    """调用本地Ollama"""
    try:
        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(
                f"{OLLAMA_BASE_URL}/api/generate",
                json={
                    "model": OLLAMA_MODEL,
                    "prompt": prompt,
                    "stream": False
                }
            )
            response.raise_for_status()
            data = response.json()

            return parse_ai_response(data.get("response", ""))
    except Exception as e:
        print(f"Ollama调用失败: {e}")
        return get_mock_response()


def parse_ai_response(text: str) -> dict:
    """解析AI返回的JSON"""
    # 尝试提取JSON部分
    json_match = re.search(r'\{[\s\S]*\}', text)
    if json_match:
        try:
            result = json.loads(json_match.group())
            # 确保所有必要字段存在
            return {
                "intent_score": result.get("intent_score", 50),
                "sentiment": result.get("sentiment", "neutral"),
                "key_points": result.get("key_points", []),
                "risks": result.get("risks", []),
                "suggestions": result.get("suggestions", []),
                "keywords": result.get("keywords", [])
            }
        except json.JSONDecodeError:
            print(f"JSON解析失败: {json_match.group()}")

    # 解析失败，尝试从文本中提取关键信息
    print(f"AI响应解析失败，返回默认值: {text[:100]}...")
    return get_mock_response()


def get_mock_response() -> dict:
    """返回Mock数据（当AI不可用时）"""
    return {
        "intent_score": 75,
        "sentiment": "positive",
        "key_points": [
            "客户对产品功能表示认可",
            "价格是主要考虑因素",
            "需要内部决策流程"
        ],
        "risks": [
            "客户可能还在对比其他竞品"
        ],
        "suggestions": [
            "及时发送详细方案",
            "突出性价比优势",
            "准备竞品对比资料"
        ],
        "keywords": ["价格", "方案", "对比"]
    }
