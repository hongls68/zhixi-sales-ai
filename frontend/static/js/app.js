/**
 * 智析销售AI - 主应用逻辑 v1.0
 * 页面切换、数据加载、功能集成
 */

// ============ 全局变量 ============
var currentPage = 'dashboard';
var isAdmin = false;

// ============ 页面切换 ============
function showPage(pageName, navElement) {
    // 隐藏所有页面
    document.querySelectorAll('.page').forEach(function(page) {
        page.classList.remove('active');
        page.classList.remove('fade-in');
    });

    // 显示目标页面
    var targetPage = document.getElementById('page-' + pageName);
    if (targetPage) {
        targetPage.classList.add('active');
        targetPage.classList.add('fade-in');
        currentPage = pageName;
    }

    // 更新菜单高亮
    document.querySelectorAll('.nav-item').forEach(function(item) {
        item.classList.remove('active');
    });
    if (navElement) {
        navElement.classList.add('active');
    }

    // 更新页面标题
    var titles = {
        'dashboard': '工作台',
        'history': '分析记录',
        'team': '团队协作',
        'admin': '管理后台',
        'profile': '个人中心'
    };
    document.getElementById('pageTitle').textContent = titles[pageName] || '工作台';

    // 更新URL hash
    window.location.hash = pageName;

    // 加载页面数据
    loadPageData(pageName);
}

// ============ 加载页面数据 ============
function loadPageData(pageName) {
    switch(pageName) {
        case 'dashboard':
            loadDashboard();
            break;
        case 'history':
            loadHistory();
            break;
        case 'team':
            loadTeam();
            break;
        case 'admin':
            loadAdminData();
            break;
        case 'profile':
            loadProfile();
            break;
    }
}

// ============ 初始化 ============
function initApp() {
    // 检查登录状态
    if (!window.auth || !window.auth.isLoggedIn()) {
        window.location.href = 'login.html';
        return;
    }

    // 获取用户信息
    var user = window.auth.getUserInfo();
    var name = user.nickname || user.phone || user.username || '用户';

    // 更新侧边栏用户信息
    document.getElementById('sidebarAvatar').textContent = name.charAt(0);
    document.getElementById('sidebarName').textContent = name;

    // 检查管理员权限
    isAdmin = (user.phone === 'admin' || user.username === 'admin' || user.role === 'admin');
    if (isAdmin && user.role !== 'admin') {
        user.role = 'admin';
        window.auth.setAuth(localStorage.getItem('zhixi_token'), user);
    }

    document.getElementById('sidebarRole').textContent = isAdmin ? '管理员' : '免费版';

    // 显示管理员菜单
    if (isAdmin) {
        var adminNav = document.getElementById('adminNav');
        if (adminNav) {
            adminNav.classList.add('show');
        }
    }

    // 根据URL hash显示对应页面
    var hash = window.location.hash.slice(1) || 'dashboard';
    var navItem = document.querySelector('[data-page="' + hash + '"]');
    if (navItem && (hash !== 'admin' || isAdmin)) {
        showPage(hash, navItem);
    } else {
        showPage('dashboard', document.querySelector('[data-page="dashboard"]'));
    }
}

// ============ 工作台 ============
function loadDashboard() {
    // 数字动画
    if (window.utils) {
        window.utils.animateNumber(document.getElementById('totalAnalyses'), 156, 1000);
        window.utils.animateNumber(document.getElementById('monthAnalyses'), 23, 800);
        window.utils.animateNumber(document.getElementById('avgScore'), 82, 900);
    }

    // 趋势图
    var trendCtx = document.getElementById('trendChart');
    if (trendCtx && typeof Chart !== 'undefined') {
        // 检查是否已有图表，避免重复创建
        if (!trendCtx._chartInstance) {
            trendCtx._chartInstance = new Chart(trendCtx.getContext('2d'), {
                type: 'line',
                data: {
                    labels: ['06-18', '06-19', '06-20', '06-21', '06-22', '06-23', '06-24'],
                    datasets: [{
                        label: '分析次数',
                        data: [3, 5, 2, 4, 6, 3, 4],
                        borderColor: '#3B82F6',
                        backgroundColor: 'rgba(59, 130, 246, 0.1)',
                        tension: 0.4,
                        fill: true
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: { legend: { display: false } },
                    scales: {
                        y: { beginAtZero: true, grid: { color: 'rgba(0,0,0,0.05)' } },
                        x: { grid: { display: false } }
                    }
                }
            });
        }
    }

    // 加载最近分析
    loadRecent();
}

function loadRecent() {
    var listEl = document.getElementById('recentList');
    if (!listEl) return;

    listEl.innerHTML = '<div style="text-align:center;padding:20px;color:var(--text-secondary)">加载中...</div>';

    if (window.api) {
        window.api.getAnalysisList().then(function(data) {
            if (!data.list || data.list.length === 0) {
                listEl.innerHTML = '<div style="text-align:center;padding:40px"><div style="font-size:48px;margin-bottom:16px">📭</div><div style="font-size:16px;font-weight:600;margin-bottom:8px">暂无分析记录</div><div style="font-size:14px;color:var(--text-secondary)">点击上方「粘贴文本分析」开始</div></div>';
                return;
            }

            var html = '<div class="history-list">';
            data.list.slice(0, 5).forEach(function(item) {
                var icon = item.type === 'sales_call' ? '📞' : (item.type === 'meeting' ? '🤝' : '📝');
                var badge = item.status === 'completed' ? '<span class="history-badge badge-completed">已完成</span>' : '<span class="history-badge badge-processing">分析中</span>';
                var score = item.score ? '<div class="history-score" style="color:' + (window.utils ? window.utils.getScoreColorHex(item.score) : '#3B82F6') + '">' + item.score + '</div>' : '';

                html += '<div class="history-item" onclick="viewAnalysis(' + item.id + ')">';
                html += '<div class="history-icon">' + icon + '</div>';
                html += '<div class="history-info"><div class="history-title">' + (item.title || '分析记录') + '</div>';
                html += '<div class="history-meta"><span>' + (window.utils ? window.utils.getAnalysisTypeName(item.type) : item.type) + '</span></div></div>';
                html += score + badge + '</div>';
            });
            html += '</div>';
            listEl.innerHTML = html;
        }).catch(function() {
            listEl.innerHTML = '<div style="text-align:center;padding:20px;color:var(--error)">加载失败，请重试</div>';
        });
    }
}

// ============ 分析记录页 ============
function loadHistory() {
    var listEl = document.getElementById('historyList');
    if (!listEl) return;

    listEl.innerHTML = '<div style="text-align:center;padding:20px;color:var(--text-secondary)">加载中...</div>';

    if (window.api) {
        window.api.getAnalysisList().then(function(data) {
            document.getElementById('historyCount').textContent = '共 ' + data.list.length + ' 条';

            if (data.list.length === 0) {
                listEl.innerHTML = '<div style="text-align:center;padding:40px"><div style="font-size:48px;margin-bottom:16px">📭</div><div style="font-size:16px;font-weight:600">暂无分析记录</div></div>';
                return;
            }

            var html = '<div class="history-list">';
            data.list.forEach(function(item) {
                var icon = item.type === 'sales_call' ? '📞' : (item.type === 'meeting' ? '🤝' : '📝');
                var badge = item.status === 'completed' ? '<span class="history-badge badge-completed">已完成</span>' : '<span class="history-badge badge-processing">分析中</span>';
                var score = item.score ? '<div class="history-score" style="color:' + (window.utils ? window.utils.getScoreColorHex(item.score) : '#3B82F6') + '">' + item.score + '</div>' : '';

                html += '<div class="history-item" onclick="viewAnalysis(' + item.id + ')">';
                html += '<div class="history-icon">' + icon + '</div>';
                html += '<div class="history-info"><div class="history-title">' + (item.title || '分析记录') + '</div>';
                html += '<div class="history-meta"><span>' + (window.utils ? window.utils.getAnalysisTypeName(item.type) : item.type) + '</span>';
                html += '<span>' + (window.utils ? window.utils.timeAgo(item.created_at) : '') + '</span></div></div>';
                html += score + badge + '</div>';
            });
            html += '</div>';
            listEl.innerHTML = html;
        }).catch(function() {
            listEl.innerHTML = '<div style="text-align:center;padding:20px;color:var(--error)">加载失败</div>';
        });
    }
}

// ============ 团队页 ============
function loadTeam() {
    var listEl = document.getElementById('teamList');
    if (!listEl) return;

    listEl.innerHTML = '<div style="text-align:center;padding:20px;color:var(--text-secondary)">加载中...</div>';

    if (window.api) {
        window.api.getTeamMembers().then(function(data) {
            var html = '<div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:16px">';
            data.members.forEach(function(member) {
                html += '<div style="padding:20px;border:1px solid var(--border-color);border-radius:var(--radius-lg);text-align:center">';
                html += '<div style="width:48px;height:48px;border-radius:50%;background:var(--primary-100);display:flex;align-items:center;justify-content:center;margin:0 auto 12px;font-size:20px;font-weight:600;color:var(--primary-600)">' + member.name.charAt(0) + '</div>';
                html += '<div style="font-weight:600;margin-bottom:4px">' + member.name + '</div>';
                html += '<div style="font-size:var(--text-sm);color:var(--text-secondary)">' + (member.role === 'admin' ? '管理员' : '成员') + '</div>';
                html += '</div>';
            });
            html += '</div>';
            listEl.innerHTML = html;
        }).catch(function() {
            listEl.innerHTML = '<div style="text-align:center;padding:20px;color:var(--error)">加载失败</div>';
        });
    }
}

// ============ 管理后台 ============
function loadAdminData() {
    if (!isAdmin) return;

    // 加载统计数据
    if (window.api) {
        window.api.getAdminStats().then(function(data) {
            if (window.utils) {
                window.utils.animateNumber(document.getElementById('adminDAU'), data.dau, 800);
                window.utils.animateNumber(document.getElementById('adminTotalUsers'), data.total_users, 800);
                window.utils.animateNumber(document.getElementById('adminTotalAnalyses'), data.total_analyses, 800);
            }
        });
    }

    loadAdminUsers();
}

function loadAdminUsers() {
    var listEl = document.getElementById('adminUserList');
    if (!listEl) return;

    listEl.innerHTML = '<div style="text-align:center;padding:20px;color:var(--text-secondary)">加载中...</div>';

    if (window.api) {
        window.api.getAdminUsers(1, '').then(function(data) {
            document.getElementById('adminUserCount').textContent = '共 ' + data.total + ' 人';

            var html = '<div style="display:flex;flex-direction:column;gap:12px">';
            data.list.forEach(function(user) {
                html += '<div style="display:flex;align-items:center;justify-content:space-between;padding:16px;border:1px solid var(--border-color);border-radius:var(--radius-md)">';
                html += '<div style="display:flex;align-items:center;gap:12px">';
                html += '<div style="width:40px;height:40px;border-radius:50%;background:var(--primary-100);display:flex;align-items:center;justify-content:center;font-weight:600;color:var(--primary-600)">' + (user.nickname || user.phone).charAt(0) + '</div>';
                html += '<div><div style="font-weight:600">' + (user.nickname || '用户') + '</div>';
                html += '<div style="font-size:var(--text-sm);color:var(--text-secondary)">' + user.phone + '</div></div></div>';
                html += '<div style="display:flex;align-items:center;gap:8px">';
                html += '<span style="padding:4px 8px;border-radius:12px;font-size:var(--text-xs);background:' + (user.role === 'admin' ? 'var(--primary-100)' : 'var(--gray-100)') + ';color:' + (user.role === 'admin' ? 'var(--primary-600)' : 'var(--text-secondary)') + '">' + (user.role === 'admin' ? '管理员' : '用户') + '</span>';
                html += '</div></div>';
            });
            html += '</div>';
            listEl.innerHTML = html;
        }).catch(function() {
            listEl.innerHTML = '<div style="text-align:center;padding:20px;color:var(--error)">加载失败</div>';
        });
    }
}

// ============ 个人中心 ============
function loadProfile() {
    var user = window.auth.getUserInfo();
    document.getElementById('profilePhone').value = user.phone || '';
    document.getElementById('profileNickname').value = user.nickname || '';
    document.getElementById('profileCompany').value = user.company || '';

    // 统计数据
    if (window.utils) {
        window.utils.animateNumber(document.getElementById('profileTotalAnalyses'), 156, 800);
        window.utils.animateNumber(document.getElementById('profileMonthAnalyses'), 23, 600);
        window.utils.animateNumber(document.getElementById('profileAvgScore'), 82, 700);
    }
}

function saveProfile() {
    var nickname = document.getElementById('profileNickname').value;
    var company = document.getElementById('profileCompany').value;

    if (window.api) {
        window.api.updateUser({ nickname: nickname, company: company }).then(function() {
            if (window.utils) window.utils.showToast('保存成功', 'success');
            // 更新侧边栏显示
            document.getElementById('sidebarName').textContent = nickname || '用户';
        }).catch(function() {
            if (window.utils) window.utils.showToast('保存失败', 'error');
        });
    }
}

// ============ 分析详情 ============
function viewAnalysis(id) {
    // 跳转到分析详情页（可以是新页面或弹窗）
    window.open('analysis.html?id=' + id, '_blank');
}

// ============ 文本分析 ============
function showTextInput() {
    document.getElementById('textModal').classList.add('active');
}

function closeTextModal() {
    document.getElementById('textModal').classList.remove('active');
}

function analyzeText() {
    var text = document.getElementById('textInput').value.trim();
    if (!text) {
        if (window.utils) window.utils.showToast('请输入对话内容', 'warning');
        return;
    }
    closeTextModal();
    if (window.utils) window.utils.showToast('正在分析...', 'info');

    if (window.api) {
        window.api.createAnalysis(text, '销售对话分析', 'sales_call').then(function(result) {
            if (window.utils) window.utils.showToast('分析完成', 'success');
            window.open('analysis.html?id=' + result.id, '_blank');
            loadRecent(); // 刷新列表
        }).catch(function(err) {
            var errorMsg = '分析失败';
            if (typeof err === 'string') errorMsg = err;
            else if (err && err.message) errorMsg = err.message;
            else if (err && err.detail) errorMsg = err.detail;
            if (window.utils) window.utils.showToast(errorMsg, 'error');
        });
    }
}

// ============ 退出登录 ============
function handleLogout() {
    if (confirm('确定要退出登录吗？')) {
        if (window.auth) window.auth.logout();
    }
}

// ============ URL hash 监听 ============
window.addEventListener('hashchange', function() {
    var hash = window.location.hash.slice(1) || 'dashboard';
    var navItem = document.querySelector('[data-page="' + hash + '"]');
    if (navItem && (hash !== 'admin' || isAdmin)) {
        showPage(hash, navItem);
    }
});

// ============ 页面加载完成后初始化 ============
document.addEventListener('DOMContentLoaded', function() {
    initApp();
});
