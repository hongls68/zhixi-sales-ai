/**
 * 听脑AI - 首页按钮登录状态处理脚本
 * 在首页加载后，将所有「免费使用」和「立即使用」按钮改为检查登录状态
 */

// 动态导入 auth 模块
const script = document.createElement('script');
script.type = 'module';
script.textContent = `
    import { isLoggedIn } from './static/js/auth.js';

    // 所有需要修改的按钮选择器
    const buttonSelectors = [
        'a[href="/home"]',                          // 首页顶部「免费使用」
        'a[href="https://itingnao.com/home"]',       // 其他所有「免费使用」和「立即使用」
    ];

    // 修改按钮行为
    function setupButtons() {
        buttonSelectors.forEach(selector => {
            const buttons = document.querySelectorAll(selector);
            buttons.forEach(btn => {
                // 阻止默认跳转
                btn.addEventListener('click', (e) => {
                    e.preventDefault();

                    if (isLoggedIn()) {
                        // 已登录，跳转到 /home
                        window.location.href = '/home';
                    } else {
                        // 未登录，跳转到 /login
                        window.location.href = '/login';
                    }
                });

                // 如果已登录，更新按钮文字
                if (isLoggedIn()) {
                    if (btn.classList.contains('hero-btn')) {
                        btn.textContent = '进入工作台';
                    } else if (btn.classList.contains('nav-btn') || btn.classList.contains('mobile-btn')) {
                        btn.textContent = '进入工作台';
                    } else {
                        // 保持原样或改为「进入工作台」
                        // btn.textContent = '进入工作台';
                    }
                }
            });
        });
    }

    // 页面加载完成后执行
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', setupButtons);
    } else {
        setupButtons();
    }
`;

document.head.appendChild(script);
