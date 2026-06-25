/**
 * 智析销售AI - API封装 v1.0
 */
(function() {
  window.api = {
    mockGetAnalysisList: function() {
      return new Promise(function(resolve) {
        setTimeout(function() {
          resolve({
            list: [
              { id: 1, title: '客户A沟通记录分析', type: 'sales_call', status: 'completed', created_at: '2026-06-24T10:30:00', summary: '客户对产品表示浓厚兴趣', score: 85 },
              { id: 2, title: '团队周会纪要', type: 'meeting', status: 'completed', created_at: '2026-06-23T14:00:00', summary: '讨论了Q3销售目标', score: 92 },
              { id: 3, title: '客户需求调研', type: 'interview', status: 'processing', created_at: '2026-06-22T09:00:00', summary: '正在分析中...', score: null }
            ],
            total: 3
          });
        }, 500);
      });
    },
    mockGetAnalysisDetail: function(id) {
      return new Promise(function(resolve) {
        setTimeout(function() {
          resolve({
            id: parseInt(id), title: '客户A沟通记录分析', type: 'sales_call', status: 'completed',
            created_at: '2026-06-24T10:30:00',
            content: '客户：你们这个产品的主要优势是什么？\n\n销售：我们主要有三个优势：第一，AI分析准确率高达98%；第二，支持多种语言和方言；第三，价格比竞品低30%。\n\n客户：价格方面有没有优惠？\n\n销售：如果您今天签约，我们可以提供15%的折扣，并且赠送3个月的高级会员。\n\n客户：我需要和团队商量一下。\n\n销售：没问题，我明天下午给您发一份详细的合作方案，您看可以吗？\n\n客户：好的，明天下午3点吧。',
            analysis: {
              sentiment: 'positive', intent_score: 78,
              key_points: ['客户对产品功能表示认可', '价格是主要考虑因素', '需要内部决策流程', '有明确的后续跟进时间'],
              risks: ['客户可能还在对比其他竞品', '决策周期可能较长'],
              suggestions: ['明天准时发送方案', '突出性价比优势', '准备竞品对比资料', '设置3天后跟进提醒'],
              keywords: ['价格', '优惠', '团队商量', '方案', '产品优势', '折扣']
            }
          });
        }, 600);
      });
    },
    mockGetTeamMembers: function() {
      return new Promise(function(resolve) {
        setTimeout(function() {
          resolve({
            members: [
              { id: 1, name: '张三', role: 'admin', phone: '13800138001' },
              { id: 2, name: '李四', role: 'member', phone: '13800138002' },
              { id: 3, name: '王五', role: 'member', phone: '13800138003' }
            ]
          });
        }, 400);
      });
    }
  };
})();
