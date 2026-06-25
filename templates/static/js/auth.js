/**
 * 听脑AI - 登录状态管理工具
 * 提供统一的认证状态管理函数
 */

const TOKEN_KEY = 'tingnao_token';
const USER_KEY = 'tingnao_user';

/**
 * 保存登录信息
 * @param {string} token - JWT token
 * @param {object} user - 用户信息对象
 */
export const setAuth = (token, user) => {
  localStorage.setItem(TOKEN_KEY, token);
  localStorage.setItem(USER_KEY, JSON.stringify(user));
};

/**
 * 获取登录信息
 * @returns {{ token: string|null, user: object }}
 */
export const getAuth = () => {
  const token = localStorage.getItem(TOKEN_KEY);
  const user = JSON.parse(localStorage.getItem(USER_KEY) || '{}');
  return { token, user };
};

/**
 * 检查是否已登录
 * @returns {boolean}
 */
export const isLoggedIn = () => {
  return !!localStorage.getItem(TOKEN_KEY);
};

/**
 * 退出登录
 */
export const logout = () => {
  localStorage.removeItem(TOKEN_KEY);
  localStorage.removeItem(USER_KEY);
  window.location.href = '/';
};

/**
 * 获取用户信息
 * @returns {object}
 */
export const getUserInfo = () => {
  return JSON.parse(localStorage.getItem(USER_KEY) || '{}');
};

/**
 * 处理「立即使用」按钮点击
 * 根据登录状态决定跳转目标
 */
export const handleUseNow = () => {
  if (isLoggedIn()) {
    window.location.href = '/home';
  } else {
    window.location.href = '/login';
  }
};

/**
 * Mock 登录 API
 * @param {string} phone - 手机号
 * @param {string} code - 验证码
 * @returns {Promise}
 */
export const mockLogin = (phone, code) => {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      if (phone.length === 11 && code === '123456') {
        resolve({
          token: 'mock_token_' + Date.now(),
          user: {
            phone,
            nickname: '用户' + phone.slice(-4),
            avatar: null
          }
        });
      } else {
        reject({ message: '验证码错误' });
      }
    }, 1000);
  });
};

/**
 * Mock 发送验证码 API
 * @param {string} phone - 手机号
 * @returns {Promise}
 */
export const mockSendCode = (phone) => {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      if (phone.length === 11 && phone.startsWith('1')) {
        resolve({ message: '验证码已发送' });
      } else {
        reject({ message: '手机号格式不正确' });
      }
    }, 500);
  });
};
