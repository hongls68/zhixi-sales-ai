/**
 * 智析销售AI - API封装 v2.0
 * 支持 Mock 和真实 API 两种模式
 */
(function() {
  // 配置：API地址
  var API_BASE = 'http://localhost:8000/api';
  var USE_API = false; // 设为 true 使用后端API，false 使用 Mock

  // 获取Token
  function getToken() {
    return localStorage.getItem('zhixi_token');
  }

  // 通用请求
  function request(url, options) {
    var token = getToken();
    var headers = {
      'Content-Type': 'application/json'
    };
    if (token) {
      headers['Authorization'] = 'Bearer ' + token;
    }

    var config = {
      headers: headers,
      ...options
    };

    return fetch(API_BASE + url, config)
      .then(function(response) {
        if (response.status === 401) {
          localStorage.removeItem('zhixi_token');
          localStorage.removeItem('zhixi_user');
          window.location.href = 'login.html';
          throw new Error('未登录');
        }
        if (!response.ok) {
          return response.json().then(function(err) {
            throw new Error(err.detail || '请求失败');
          });
        }
        return response.json();
      });
  }

  // Mock数据
  var mockData = {
    getAnalysisList: function() {
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

    getAnalysisDetail: function(id) {
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

    getTeamMembers: function() {
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

  // API接口
  window.api = {
    // 认证
    sendCode: function(phone) {
      if (USE_API) {
        return request('/auth/send-code', {
          method: 'POST',
          body: JSON.stringify({ phone: phone })
        });
      }
      return new Promise(function(resolve) {
        setTimeout(function() { resolve({ message: '验证码已发送' }); }, 500);
      });
    },

    login: function(phone, code) {
      if (USE_API) {
        return request('/auth/login', {
          method: 'POST',
          body: JSON.stringify({ phone: phone, code: code })
        });
      }
      return new Promise(function(resolve, reject) {
        setTimeout(function() {
          if (code === '123456') {
            resolve({
              token: 'mock_token_' + Date.now(),
              user: { id: 1, phone: phone, nickname: '用户' + phone.slice(-4) }
            });
          } else {
            reject({ message: '验证码错误' });
          }
        }, 800);
      });
    },

    register: function(phone, code, password) {
      if (USE_API) {
        return request('/auth/register', {
          method: 'POST',
          body: JSON.stringify({ phone: phone, code: code, password: password })
        });
      }
      return new Promise(function(resolve, reject) {
        setTimeout(function() {
          if (code === '123456' && password.length >= 6) {
            resolve({
              token: 'mock_token_' + Date.now(),
              user: { id: 1, phone: phone, nickname: '用户' + phone.slice(-4) }
            });
          } else {
            reject({ message: '验证码错误或密码太短' });
          }
        }, 800);
      });
    },

    // 分析
    getAnalysisList: function(params) {
      if (USE_API) {
        var query = new URLSearchParams(params || {}).toString();
        return request('/analysis/list?' + query);
      }
      return mockData.getAnalysisList();
    },

    getAnalysisDetail: function(id) {
      if (USE_API) {
        return request('/analysis/' + id);
      }
      return mockData.getAnalysisDetail(id);
    },

    createAnalysis: function(content, title, type) {
      if (USE_API) {
        return request('/analysis/create', {
          method: 'POST',
          body: JSON.stringify({ content: content, title: title, type: type })
        });
      }
      // Mock
      return new Promise(function(resolve) {
        setTimeout(function() {
          resolve({
            id: Date.now(),
            title: title || '新分析',
            content: content,
            type: type || 'sales_call',
            status: 'completed',
            analysis: {
              intent_score: 78,
              sentiment: 'positive',
              key_points: ['客户对产品感兴趣', '价格是主要考虑'],
              risks: ['可能对比竞品'],
              suggestions: ['及时跟进', '发送方案'],
              keywords: ['价格', '方案']
            }
          });
        }, 1500);
      });
    },

    deleteAnalysis: function(id) {
      if (USE_API) {
        return request('/analysis/' + id, { method: 'DELETE' });
      }
      return new Promise(function(resolve) {
        setTimeout(function() { resolve({ message: '删除成功' }); }, 300);
      });
    },

    // 用户
    getUserInfo: function() {
      if (USE_API) {
        return request('/user/me');
      }
      return new Promise(function(resolve) {
        var user = JSON.parse(localStorage.getItem('zhixi_user') || '{}');
        resolve(user);
      });
    },

    updateUser: function(data) {
      if (USE_API) {
        return request('/user/update', {
          method: 'PUT',
          body: JSON.stringify(data)
        });
      }
      return new Promise(function(resolve) {
        var user = JSON.parse(localStorage.getItem('zhixi_user') || '{}');
        Object.assign(user, data);
        localStorage.setItem('zhixi_user', JSON.stringify(user));
        resolve(user);
      });
    },

    getUserStats: function() {
      if (USE_API) {
        return request('/user/stats');
      }
      return new Promise(function(resolve) {
        resolve({
          total_analyses: 156,
          month_analyses: 23,
          avg_score: 82,
          trend: [
            { date: '06-18', count: 3 },
            { date: '06-19', count: 5 },
            { date: '06-20', count: 2 },
            { date: '06-21', count: 4 },
            { date: '06-22', count: 6 },
            { date: '06-23', count: 3 },
            { date: '06-24', count: 4 }
          ]
        });
      });
    },

    // 团队
    getTeamMembers: function() {
      if (USE_API) {
        return request('/team/members');
      }
      return mockData.getTeamMembers();
    }
  };
})();
