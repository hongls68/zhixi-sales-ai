import json, re, httpx
from config import AI_PROVIDER, API_BASE_URL, API_KEY, API_MODEL, OLLAMA_BASE_URL, OLLAMA_MODEL
from prompts.sales import build_prompt

async def analyze_with_ai(content, user_context=None, style="professional", depth="standard", language="zh"):
    prompt = build_prompt(content, style=style, depth=depth, language=language)
    if AI_PROVIDER == "api":
        result = await call_api(prompt)
    elif AI_PROVIDER == "ollama":
        result = await call_ollama(prompt)
    else:
        result = None
    return result if result else get_mock_response(content)

async def call_api(prompt):
    if not API_KEY:
        return None
    try:
        async with httpx.AsyncClient(timeout=120.0) as client:
            r = await client.post(
                f"{API_BASE_URL}/chat/completions",
                headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"},
                json={"model": API_MODEL, "messages": [{"role": "system", "content": "你是销售分析专家。只输出JSON，不要有任何其他文字。"}, {"role": "user", "content": prompt}], "temperature": 0.7, "max_tokens": 4000}
            )
            if r.status_code != 200:
                return None
            text = r.json()["choices"][0]["message"]["content"]
            return parse_ai_response("{" + text.split("{", 1)[1]) if "{" in text else None
    except:
        return None

def parse_ai_response(text):
    """解析AI返回的JSON响应，支持新旧两种格式"""
    text = re.sub(r'```json\s*', '', text)
    text = re.sub(r'```\s*', '', text)
    m = re.search(r'\{[\s\S]*\}', text)
    if not m:
        return None
    try:
        d = json.loads(m.group())

        # 兼容旧格式和新格式
        lead_score = d.get("lead_score") or d.get("intent_score") or d.get("score") or 50
        if not isinstance(lead_score, (int, float)):
            lead_score = 50
        lead_score = max(0, min(100, int(lead_score)))

        # 成交概率
        closing_prob = d.get("closing_probability") or d.get("closing_prob") or (lead_score - 5)
        if not isinstance(closing_prob, (int, float)):
            closing_prob = lead_score - 5
        closing_prob = max(0, min(100, int(closing_prob)))

        # 意向度标签
        raw = d.get("intent") or d.get("sentiment") or ""
        intent = raw if raw in ["high","medium","low"] else ("high" if lead_score>=70 else "medium" if lead_score>=40 else "low")

        # 客户画像
        profile = d.get("customer_profile") or {}
        if isinstance(profile, dict):
            customer_types = profile.get("types") or []
            customer_chars = profile.get("characteristics") or []
        else:
            customer_types = []
            customer_chars = []

        # 关键需求（处理新格式的 {text, importance} 和旧格式的简单列表）
        raw_needs = d.get("key_needs") or []
        key_needs = []
        for item in raw_needs:
            if isinstance(item, dict):
                key_needs.append({"text": str(item.get("text", "")), "importance": item.get("importance", 3)})
            else:
                key_needs.append({"text": str(item), "importance": 3})

        # 客户痛点（处理新格式的 {issue, explanation} 和旧格式的简单列表）
        raw_pains = d.get("pain_points") or []
        pain_points = []
        for item in raw_pains:
            if isinstance(item, dict):
                pain_points.append({"issue": str(item.get("issue", "")), "explanation": str(item.get("explanation", ""))})
            else:
                pain_points.append({"issue": str(item), "explanation": ""})

        # 情绪时间线
        raw_timeline = d.get("emotion_timeline") or d.get("emotion_trend") or []
        if isinstance(raw_timeline, str):
            # 旧格式：字符串，直接使用
            emotion_timeline = [{"stage": "整体", "emoji": "😊", "mood": raw_timeline, "description": raw_timeline}]
        else:
            emotion_timeline = raw_timeline if isinstance(raw_timeline, list) else []

        # 销售表现
        raw_perf = d.get("sales_performance") or {}
        if isinstance(raw_perf, dict):
            sales_perf = {
       