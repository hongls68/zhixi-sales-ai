/**
 * 智析销售AI - 认证工具 v1.0
 * 全局变量方式，兼容直接打开HTML
 */
(function() {
  const TOKEN_KEY = 'zhixi_token';
  const USER_KEY = 'zhixi_user';

  window.auth = {
    setAuth: function(token, user) {
      localStorage.setItem(TOKEN_KEY, token);
      localStorage.setItem(USER_KEY, JSON.stringify(user));
    },
    getAuth: function() {
      var token = localStorage.getItem(TOKEN_KEY);
      var user = JSON.parse(localStorage.getItem(USER_KEY) || '{}');
      return { token: token, user: user };
    },
    isLoggedIn: function() {
      return !!localStorage.getItem(TOKEN_KEY);
    },
    logout: function() {
      localStorage.removeItem(TOKEN_KEY);
      localStorage.removeItem(USER_KEY);
      window.location.href = 'login.html';
    },
    getUserInfo: function() {
      return JSON.parse(localStorage.getItem(USER_KEY) || '{}');
    },
    updateUserInfo: function(updates) {
      var user = this.getUserInfo();
      for (var k in updates) user[k] = updates[k];
      localStorage.setItem(USER_KEY, JSON.stringify(user));
      return user;
    },
    mockLogin: function(phone, code) {
      return new Promise(function(resolve, reject) {
        setTimeout(function() {
          if (phone.length === 11 && code === '123456') {
            resolve({
              token: 'mock_token_' + Date.now(),
              user: { id: 1, phone: phone, nickname: '用户' + phone.slice(-4), avatar: null, role: 'user', company: '' }
            });
          } else if (phone.length !== 11) {
            reject({ message: '请输入正确的11位手机号' });
          } else {
            reject({ message: '验证码错误' });
          }
        }, 800);
      });
    },
    mockSendCode: function(phone) {
      return new Promise(function(resolve, reject) {
        setTimeout(function() {
          if (phone.length === 11 && phone[0] === '1') {
            resolve({ message: '验证码已发送' });
          } else {
            reject({ message: '请输入正确的手机号' });
          }
        }, 500);
      });
    },
    mockRegister: function(phone, code, password) {
      return new Promise(function(resolve, reject) {
        setTimeout(function() {
          if (phone.length === 11 && code === '123456' && password.length >= 6) {
            resolve({
              token: 'mock_token_' + Date.now(),
              user: { id: 1, phone: phone, nickname: '用户' + phone.slice(-4), avatar: null, role: 'user', company: '' }
            });
          } else if (password.length < 6) {
            reject({ message: '密码至少6位' });
          } else {
            reject({ message: '验证码错误' });
          }
        }, 800);
      });
    }
  };
})();
