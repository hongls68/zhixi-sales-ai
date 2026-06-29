"""
智析销售AI - 提示词管理 v2.0
"""

STYLES = {
    "professional": {"name": "正式商务", "prefix": "你是一位资深的销售分析专家，拥有10年大客户销售和管理经验。请用正式、专业的商务语言进行分析。"},
    "concise": {"name": "简洁直接", "prefix": "你是一位高效的销售分析助手。请用简洁、直接的语言，重点突出，避免冗余。"},
    "friendly": {"name": "亲和友好", "prefix": "你是一位经验丰富的销售顾问。请用亲和、易懂的语言，像朋友一样给出建议。"}
}

DEPTHS = {
    "simple": {"name": "快速分析", "instruction": "请进行快速分析，提供核心要点即可，每个维度2-3条。"},
    "standard": {"name": "标准分析", "instruction": "请进行全面分析，每个维度3-5条，包含具体细节。"},
    "detailed": {"name": "深度分析", "instruction": "请进行深度分析，每个维度5-8条，包含具体细节和可执行建议。"}
}

LANGUAGES = {
    "zh": {"name": "中文", "instruction": "请用中文输出所有分析内容。"},
    "en": {"name": "English", "instruction": "Please output all analysis content in English."},
    "mixed": {"name": "中英混合", "instruction": "请用中文输出分析内容，专业术语保留英文。"}
}

BASE_PROMPT = """{style_prefix}

## 分析任务
请分析以下销售对话/沟通记录，从多个维度提供专业洞察。
{depth_instruction}
{language_instruction}

## 分析维度

### 1. 客户意向度评估
- **高意向**：明确表达购买意愿，讨论具体细节（价格、时间、数量）
- **中意向**：表示感兴趣，但有顾虑或需要考虑
- **低意向**：只是了解，没有明确购买意向

### 2. 关键需求提取
- 客户明确提到的需求
- 客户暗示但未明说的需求

### 3. 客户痛点
- 客户当前面临的问题和困扰
- 阻碍成交的因素

### 4. 情绪变化分析
- 对话开始时客户的态度
- 讨论过程中的情绪变化
- 结束时的最终态度

### 5. 行动建议
- 短期跟进（1-3天）
- 中期策略（1-2周）

### 6. 风险预警
- 可能导致丢单的风险点

### 7. 关键词提取
- 提取3-8个对话中的关键词

## 输出格式
请严格按以下JSON格式输出，不要添加任何其他内容：

```json
{{
  "intent": "high",
  "intent_score": 85,
  "key_needs": ["需求1", "需求2"],
  "pain_points": ["痛点1", "痛点2"],
  "emotion_trend": "情绪变化描述",
  "action_suggestions": ["建议1", "建议2"],
  "risks": ["风险1"],
  "keywords": ["关键词1", "关键词2"]
}}
```

## 待分析的对话内容

{content}
"""


def build_prompt(content, style="professional", depth="standard", language="zh"):
    style_config = STYLES.get(style, STYLES["professional"])
    depth_config = DEPTHS.get(depth, DEPTHS["standard"])
    lang_config = LANGUAGES.get(language, LANGUAGES["zh"])
    prompt = BASE_PROMPT.format(
        style_prefix=style_config["prefix"],
        depth_instruction=depth_config["instruction"],
        language_instruction=lang_config["instruction"],
        content=content
    )
    return prompt


def get_style_options():
    return [{"value": k, "name": v["name"]} for k, v in STYLES.items()]

def get_depth_options():
    return [{"value": k, "name": v["name"]} for k, v in DEPTHS.items()]

def get_language_options():
    return [{"value": k, "name": v["name"]} for k, v in LANGUAGES.items()]
