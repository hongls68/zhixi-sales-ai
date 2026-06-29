"""
智析销售AI - AI服务 v2.0
"""
import json
import re
import httpx
from config import AI_PROVIDER, API_BASE_URL, API_KEY, API_MODEL, OLLAMA_BASE_URL, OLLAMA_MODEL
from prompts.sales import build_prompt


async def analyze_with_ai(content, user_context=None, style="professional", depth="standard", language="zh"):
    prompt = build_prompt(content, style=style, depth=depth, language=language)
    if AI_PROVIDER == "api":
        result = await call_api(prompt)
    elif AI_PROVIDER == "ollama":
        result = await call_ollama(prompt)
    else:
        raise ValueError(f"Unknown AI provider: {AI_PROVIDER}")
    return result


async def call_api(prompt):
    if not API_KEY:
        print("API Key未配置，使用Mock数据")
        return get_mock_response()
    try:
        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(
                f"{API_BASE_URL}/chat/completions",
                headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"},
                json={
                    "model": API_MODEL,
                    "messages": [
                        {"role": "system", "content": "你是一位资深的销售分析专家，请严格按照JSON格式输出分析结果。只输出JSON，不要有任何其他文字。"},
                        {"role": "user", "content": prompt}
                    ],
                    "temperature": 0.7,
                    "max_tokens": 4000
                }
            )
            if response.status_code != 200:
                print(f"API返回错误: {response.status_code}")
                return get_mock_response()
            data = response.json()
            ai_response = data["choices"][0]["message"]["content"]
            print(f"AI响应长度: {len(ai_response)} 字符")
            return parse_ai_response(ai_response)
    except Exception as e:
        print(f"API调用失败: {e}")
        return get_mock_response()


async def call_ollama(prompt):
    try:
        async with httpx.AsyncClient(timeout=180.0) as client:
            response = await client.post(
                f"{OLLAMA_BASE_URL}/api/generate",
                json={"model": OLLAMA_MODEL, "prompt": prompt, "stream": False, "format": "json"}
            )
            response.raise_for_status()
            data = response.json()
            return parse_ai_response(data.get("response", ""))
    except Exception as e:
        print(f"Ollama调用失败: {e}")
        return get_mock_response()


def parse_ai_response(text):
    json_match = re.search(r'\{[\s\S]*\}', text)
    if json_match:
        try:
            result = json.loads(json_match.group())
            return normalize_result(result)
        except json.JSONDecodeError as e:
            print(f"JSON解析失败: {e}")
    print("AI响应解析失败，返回默认值")
    return get_mock_response()


def normalize_result(result):
    intent = result.get("intent", "medium")
    if intent not in ["high", "medium", "low"]:
        intent = "medium"
    intent_score = result.get("intent_score", 50)
    if not isinstance(intent_score, (int, float)):
        intent_score = 50
    intent_score = max(0, min(100, int(intent_score)))
    return {
        "intent": intent,
        "intent_score": intent_score,
        "key_needs": ensure_list(result.get("key_needs", [])),
        "pain_points": ensure_list(result.get("pain_points", [])),
        "emotion_trend": str(result.get("emotion_trend", "客户情绪稳定")),
        "action_suggestions": ensure_list(result.get("action_suggestions", [])),
        "risks": ensure_list(result.get("risks", [])),
        "keywords": ensure_list(result.get("keywords", []))
    }


def ensure_list(value):
    if isinstance(value, list):
        return [str(item) for item in value if item]
    if isinstance(value, str):
        return [value] if value else []
    return []


def get_mock_response():
    return {
        "intent": "medium",
        "intent_score": 65,
        "key_needs": ["客户对产品功能感兴趣", "关注性价比和投资回报", "需要了解售后服务支持"],
        "pain_points": ["预算有限，需要控制成本", "担心理实施周期影响业务", "对数据安全性有顾虑"],
        "emotion_trend": "客户从最初的观望态度，随着产品介绍逐渐表现出兴趣，在讨论价格时略有犹豫，最后表示需要内部讨论后决定。",
        "action_suggestions": ["3天内发送详细的产品方案和报价", "准备针对性的案例展示", "安排产品演示或试用", "7天后跟进客户决策进展"],
        "risks": ["客户可能在对比其他竞品方案", "内部决策流程可能较长"],
        "keywords": ["产品功能", "价格", "性价比", "售后服务", "实施方案"]
    }


def get_ai_config_options():
    from prompts.sales import get_style_options, get_depth_options, get_language_options
    return {
        "styles": get_style_options(),
        "depths": get_depth_options(),
        "languages": get_language_options()
    }
