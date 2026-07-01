"""
智析销售AI - 提示词管理 v3.0
专业级销售分析报告生成
"""

STYLES = {
    "professional": {"name": "正式商务", "prefix": "你是一位资深的销售分析专家，拥有10年大客户销售和管理经验。请用正式、专业的商务语言进行分析。"},
    "concise": {"name": "简洁直接", "prefix": "你是一位高效的销售分析助手。请用简洁、直接的语言，重点突出，避免冗余。"},
    "friendly": {"name": "亲和友好", "prefix": "你是一位经验丰富的销售顾问。请用亲和、易懂的语言，像朋友一样给出建议。"}
}

DEPTHS = {
    "simple": {"name": "快速分析", "instruction": "请进行快速分析，提供核心要点即可，每个维度精简到2-3条。"},
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
请深入分析以下销售对话/沟通记录，从多个维度提供专业洞察。
{depth_instruction}
{language_instruction}

## 重要原则
- 必须基于对话实际内容分析，不要使用通用模板
- 提取对话中提到的具体产品、价格、优惠等信息
- 根据对话内容判断行业类型（服装、软件、房产、汽车等）
- 建议要针对具体情况，不要泛泛而谈
- 如果对话中未涉及某个维度，不要编造相关内容，标记为"未明确"
- 评分要客观，基于对话中的实际表现

## 评分维度说明

### Lead Score (0-100分)
评分依据包括：
- 是否主动提出需求
- 是否询问价格/产品详情
- 是否讨论具体细节
- 是否进行比较（竞品对比）
- 是否议价
- 是否明确意向
- 是否留下联系方式
- 是否主动推进流程

### 成交概率 (0-100%)
基于Lead Score和对话进展综合判断

### 销售表现评分 (每项0-100分)
- 需求挖掘：是否有效挖掘客户真实需求
- 产品介绍：是否清晰介绍产品特点
- 价值塑造：是否成功塑造产品价值
- 异议处理：是否有效处理客户异议
- 报价策略：报价时机和策略是否恰当
- 成交推进：是否积极推进成交
- 专业程度：销售展示的专业性
- 沟通技巧：沟通是否流畅有效

## 输出格式
请严格按以下JSON格式输出，不要添加任何其他内容：

```json
{{
  "lead_score": 95,
  "closing_probability": 90,
  "score_reason": "客户主动预约看房，并完成价格谈判，成交意愿较高。",
  "summary_brief": "客户预算明确，以学区房为核心需求，关注房屋质量及价格，最终成功预约看房，成交意向较高。",
  "summary_detail": "详细总结，2-3段话...",
  "customer_profile": {{
    "types": ["刚需客户", "价格敏感型"],
    "characteristics": ["理性消费", "关注品质", "决策谨慎"]
  }},
  "key_needs": [
    {{"text": "三居室", "importance": 5}},
    {{"text": "学区", "importance": 5}},
    {{"text": "采光", "importance": 3}}
  ],
  "pain_points": [
    {{"issue": "价格", "explanation": "担心超出预算，需要更多优惠"}},
    {{"issue": "质量", "explanation": "担心房屋质量问题，要求提供检测报告"}}
  ],
  "emotion_timeline": [
    {{"stage": "开始", "emoji": "🙂", "mood": "平静", "description": "客户态度平和"}},
    {{"stage": "需求确认", "emoji": "😊", "mood": "感兴趣", "description": "确认了核心需求"}},
    {{"stage": "议价", "emoji": "😐", "mood": "犹豫", "description": "对价格有顾虑"}},
    {{"stage": "决策", "emoji": "😄", "mood": "满意", "description": "达成共识"}}
  ],
  "sales_performance": {{
    "need_digging": 85,
    "product_int