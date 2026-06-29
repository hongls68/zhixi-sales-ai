/**
 * 智析销售AI - API封装 v2.0
 * 支持 Mock 和真实 API 两种模式
 */
(function() {
  // 配置：API地址
  var API_BASE = 'http://localhost:8000/api';
  var USE_API = true; // 设为 true 使用后端API，false 使用 Mock

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

    login: function(account, password) {
      if (USE_API) {
        return request('/auth/login', {
          method: 'POST',
          body: JSON.stringify({ account: account, password: password })
        });
      }
      // Mock模式
      return new Promise(function(resolve, reject) {
        setTimeout(function() {
          if (password.length >= 6) {
            resolve({
              token: 'mock_token_' + Date.now(),
              user: {
                id: 1,
                phone: account,
                username: account,
                nickname: account === 'admin' ? '管理员' : '用户' + account.slice(-4),
                role: account === 'admin' ? 'admin' : 'user'
              }
            });
          } else {
            reject({ message: '密码错误' });
          }
        }, 800);
      });
    },

    register: function(phone, code, password, username, email) {
      if (USE_API) {
        return request('/auth/register', {
          method: 'POST',
          body: JSON.stringify({
            phone: phone,
            code: code,
            password: password,
            username: username || null,
            email: email || null
          })
        });
      }
      return new Promise(function(resolve, reject) {
        setTimeout(function() {
          if (code === '123456' && password.length >= 6) {
            resolve({
              token: 'mock_token_' + Date.now(),
              user: {
                id: 1,
                phone: phone,
                username: username,
                email: email,
                nickname: '用户' + phone.slice(-4)
              }
            });
          } else {
            reject({ message: '验证码错误或密码太短' });
          }
        }, 800);
      });
    },

    // 分析配置
    getAnalysisConfig: function() {
      if (USE_API) {
        return request('/analysis/config');
      }
      return new Promise(function(resolve) {
        resolve({
          styles: [
            {value: 'professional', name: '正式商务'},
            {value: 'concise', name: '简洁直接'},
            {value: 'friendly', name: '亲和友好'}
          ],
          depths: [
            {value: 'simple', name: '快速分析'},
            {value: 'standard', name: '标准分析'},
            {value: 'detailed', name: '深度分析'}
          ],
          languages: [
            {value: 'zh', name: '中文'},
            {value: 'en', name: 'English'},
            {value: 'mixed', name: '中英混合'}
          ]
        });
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

    createAnalysis: function(content, title, type, style, depth, language) {
      if (USE_API) {
        return request('/analysis/create', {
          method: 'POST',
          body: JSON.stringify({
            content: content,
            title: title,
            type: type,
            style: style || 'professional',
            depth: depth || 'standard',
            language: language || 'zh'
          })
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
    },

    // 管理员接口
    getAdminStats: function() {
      if (USE_API) {
        return request('/admin/stats');
      }
      // Mock数据
      return new Promise(function(resolve) {
        resolve({
          dau: 12,
          wau: 45,
          total_users: 156,
          today_users: 5,
          total_analyses: 423,
          today_analyses: 18,
          user_trend: [
            { date: '06-18', count: 3 }, { date: '06-19', count: 5 },
            { date: '06-20', count: 2 }, { date: '06-21', count: 4 },
            { date: '06-22', count: 6 }, { date: '06-23', count: 3 },
            { date: '06-24', count: 5 }
          ],
          analysis_trend: [
            { date: '06-18', count: 8 }, { date: '06-19', count: 12 },
            { date: '06-20', count: 6 }, { date: '06-21', count: 15 },
            { date: '06-22', count: 20 }, { date: '06-23', count: 10 },
            { date: '06-24', count: 18 }
          ]
        });
      });
    },

    getAdminUsers: function(page, keyword) {
      if (USE_API) {
        var query = new URLSearchParams({ page: page, keyword: keyword || '' }).toString();
        return request('/admin/users?' + query);
      }
      return new Promise(function(resolve) {
        resolve({
          list: [
            { id: 1, phone: 'admin', nickname: '管理员', role: 'admin', is_active: true, created_at: '2026-06-20T10:00:00' },
            { id: 2, phone: '13800138000', nickname: '用户8000', role: 'user', is_active: true, created_at: '2026-06-21T14:00:00' },
            { id: 3, phone: '13900139000', nickname: '用户9000', role: 'user', is_active: true, created_at: '2026-06-22T09:00:00' }
          ],
          total: 3,
          page: 1,
          page_size: 20
        });
      });
    },

    updateAdminUser: function(userId, data) {
      if (USE_API) {
        return request('/admin/users/' + userId, {
          method: 'PUT',
          body: JSON.stringify(data)
        });
      }
      return new Promise(function(resolve) { resolve({ id: userId, ...data }); });
    },

    toggleAdminUserActive: function(userId) {
      if (USE_API) {
        return request('/admin/users/' + userId + '/toggle-active', { method: 'PUT' });
      }
      return new Promise(function(resolve) { resolve({ id: userId, is_active: true }); });
    },

    deleteAdminUser: function(userId) {
      if (USE_API) {
        return request('/admin/users/' + userId, { method: 'DELETE' });
      }
      return new Promise(function(resolve) { resolve({ message: '删除成功' }); });
    },

    getAdminAnalyses: function(page, keyword) {
      if (USE_API) {
        var query = new URLSearchParams({ page: page, keyword: keyword || '' }).toString();
        return request('/admin/analyses?' + query);
      }
      return new Promise(function(resolve) {
        resolve({
          list: [
            { id: 1, title: '客户A沟通记录', user_phone: '13800138000', analysis: { intent_score: 78 }, created_at: '2026-06-24T10:30:00' },
            { id: 2, title: '团队周会纪要', user_phone: '13900139000', analysis: { intent_score: 92 }, created_at: '2026-06-23T14:00:00' }
          ],
          total: 2,
          page: 1,
          page_size: 20
        });
      });
    },

    deleteAdminAnalysis: function(analysisId) {
      if (USE_API) {
        return request('/admin/analyses/' + analysisId, { method: 'DELETE' });
      }
      return new Promise(function(resolve) { resolve({ message: '删除成功' }); });
    },

    getOperationLogs: function(page, action) {
      if (USE_API) {
        var query = new URLSearchParams({ page: page, action: action || '' }).toString();
        return request('/admin/operation-logs?' + query);
      }
      return new Promise(function(resolve) {
        resolve({
          list: [
            { id: 1, admin_name: '管理员', action: 'delete_user', target_type: 'user', target_id: 5, detail: '删除用户 13800138000', ip_address: '127.0.0.1', created_at: '2026-06-25T10:00:00' },
            { id: 2, admin_name: '管理员', action: 'update_user', target_type: 'user', target_id: 3, detail: '更新用户 13900139000: 角色: user → admin', ip_address: '127.0.0.1', created_at: '2026-06-25T09:30:00' },
            { id: 3, admin_name: '管理员', action: 'disable_user', target_type: 'user', target_id: 7, detail: '禁用用户 15000150000', ip_address: '127.0.0.1', created_at: '2026-06-24T16:00:00' }
          ],
          total: 3,
          page: 1,
          page_size: 20
        });
      });
    }
  };
})();
