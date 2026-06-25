/**
 * 智析销售AI - 工具函数 v1.1
 * 更新：Toast优化、确认弹窗、数字动画、防抖
 */
(function() {
  window.utils = {
    // ============ 日期格式化 ============
    formatDate: function(dateStr, format) {
      format = format || 'YYYY-MM-DD HH:mm';
      var d = new Date(dateStr);
      var Y = d.getFullYear(), M = String(d.getMonth()+1).padStart(2,'0'), D = String(d.getDate()).padStart(2,'0');
      var h = String(d.getHours()).padStart(2,'0'), m = String(d.getMinutes()).padStart(2,'0');
      return format.replace('YYYY',Y).replace('MM',M).replace('DD',D).replace('HH',h).replace('mm',m);
    },

    timeAgo: function(dateStr) {
      var diff = Date.now() - new Date(dateStr).getTime();
      var min = Math.floor(diff/60000), hr = Math.floor(diff/3600000), day = Math.floor(diff/86400000);
      if (min < 1) return '刚刚';
      if (min < 60) return min + '分钟前';
      if (hr < 24) return hr + '小时前';
      return day + '天前';
    },

    // ============ Toast提示（优化版） ============
    showToast: function(message, type, duration) {
      type = type || 'info';
      duration = duration || 3000;

      // 确保容器存在
      var container = document.getElementById('toast-container');
      if (!container) {
        container = document.createElement('div');
        container.id = 'toast-container';
        container.style.cssText = 'position:fixed;top:80px;right:20px;z-index:10000;display:flex;flex-direction:column;gap:10px;';
        document.body.appendChild(container);
      }

      // 图标映射
      var icons = { success: '✓', error: '✕', warning: '⚠', info: 'ℹ' };
      var colors = { success: '#10B981', error: '#EF4444', warning: '#F59E0B', info: '#3B82F6' };

      // 创建Toast
      var toast = document.createElement('div');
      toast.style.cssText = 'background:#fff;border-radius:8px;padding:12px 20px;box-shadow:0 4px 12px rgba(0,0,0,0.15);display:flex;align-items:center;gap:10px;min-width:280px;max-width:400px;animation:slideInRight 0.3s ease;border-left:4px solid ' + colors[type] + ';cursor:pointer;';

      toast.innerHTML = '<span style="font-weight:700;font-size:18px;color:' + colors[type] + '">' + (icons[type]||'ℹ') + '</span><span style="flex:1;font-size:14px;color:#374151">' + message + '</span><span style="color:#9CA3AF;font-size:12px">✕</span>';

      // 点击关闭
      toast.onclick = function() {
        toast.style.animation = 'slideOutRight 0.3s ease';
        setTimeout(function() { toast.remove(); }, 300);
      };

      container.appendChild(toast);

      // 自动消失
      setTimeout(function() {
        if (toast.parentNode) {
          toast.style.animation = 'slideOutRight 0.3s ease';
          setTimeout(function() { if (toast.parentNode) toast.remove(); }, 300);
        }
      }, duration);
    },

    // ============ 确认弹窗 ============
    showConfirm: function(title, message) {
      return new Promise(function(resolve) {
        // 创建遮罩
        var overlay = document.createElement('div');
        overlay.style.cssText = 'position:fixed;top:0;left:0;right:0;bottom:0;background:rgba(0,0,0,0.5);display:flex;align-items:center;justify-content:center;z-index:10000;animation:fadeIn 0.2s ease;';

        // 创建弹窗
        var modal = document.createElement('div');
        modal.style.cssText = 'background:#fff;border-radius:12px;padding:24px;max-width:400px;width:90%;animation:scaleIn 0.2s ease;';

        modal.innerHTML = '<h3 style="font-size:18px;font-weight:600;color:#1F2937;margin-bottom:8px">' + title + '</h3><p style="font-size:14px;color:#6B7280;margin-bottom:24px;line-height:1.6">' + message + '</p><div style="display:flex;justify-content:flex-end;gap:12px"><button id="confirm-cancel" style="padding:8px 20px;border:1px solid #E5E7EB;border-radius:8px;background:#fff;cursor:pointer;font-size:14px;color:#374151">取消</button><button id="confirm-ok" style="padding:8px 20px;border:none;border-radius:8px;background:#3B82F6;color:#fff;cursor:pointer;font-size:14px">确定</button></div>';

        overlay.appendChild(modal);
        document.body.appendChild(overlay);

        // 绑定事件
        modal.querySelector('#confirm-cancel').onclick = function() {
          overlay.style.animation = 'fadeOut 0.2s ease';
          setTimeout(function() { overlay.remove(); }, 200);
          resolve(false);
        };

        modal.querySelector('#confirm-ok').onclick = function() {
          overlay.style.animation = 'fadeOut 0.2s ease';
          setTimeout(function() { overlay.remove(); }, 200);
          resolve(true);
        };

        overlay.onclick = function(e) {
          if (e.target === overlay) {
            overlay.style.animation = 'fadeOut 0.2s ease';
            setTimeout(function() { overlay.remove(); }, 200);
            resolve(false);
          }
        };
      });
    },

    // ============ 数字滚动动画 ============
    animateNumber: function(element, target, duration) {
      duration = duration || 1000;
      var start = 0;
      var startTime = null;

      function step(timestamp) {
        if (!startTime) startTime = timestamp;
        var progress = Math.min((timestamp - startTime) / duration, 1);
        // easeOutCubic
        var eased = 1 - Math.pow(1 - progress, 3);
        element.textContent = Math.floor(eased * target);
        if (progress < 1) {
          requestAnimationFrame(step);
        } else {
          element.textContent = target;
        }
      }

      requestAnimationFrame(step);
    },

    // ============ 防抖函数 ============
    debounce: function(fn, delay) {
      var timer = null;
      return function() {
        var context = this, args = arguments;
        clearTimeout(timer);
        timer = setTimeout(function() {
          fn.apply(context, args);
        }, delay || 300);
      };
    },

    // ============ 显示Loading状态 ============
    showLoading: function(element) {
      if (!element) return;
      element.disabled = true;
      element.dataset.originalText = element.textContent;
      var spinner = document.createElement('span');
      spinner.className = 'btn-spinner';
      spinner.style.cssText = 'display:inline-block;width:16px;height:16px;border:2px solid rgba(255,255,255,0.3);border-top-color:#fff;border-radius:50%;animation:spin 0.8s linear infinite;margin-right:8px;';
      element.textContent = '';
      element.appendChild(spinner);
      element.appendChild(document.createTextNode('加载中...'));
    },

    hideLoading: function(element) {
      if (!element) return;
      element.disabled = false;
      element.textContent = element.dataset.originalText || '提交';
    },

    // ============ 类型和颜色映射 ============
    getAnalysisTypeName: function(type) {
      var m = { sales_call:'销售通话', meeting:'会议记录', interview:'访谈调研', training:'培训课程' };
      return m[type] || type;
    },

    getScoreColor: function(score) {
      if (score >= 90) return 'var(--success)';
      if (score >= 70) return 'var(--primary-500)';
      if (score >= 60) return 'var(--warning)';
      return 'var(--error)';
    },

    getScoreColorHex: function(score) {
      if (score >= 90) return '#10B981';
      if (score >= 70) return '#3B82F6';
      if (score >= 60) return '#F59E0B';
      return '#EF4444';
    },

    // ============ 生成空状态HTML ============
    getEmptyStateHTML: function(icon, title, desc, btnText, btnHref) {
      var html = '<div style="text-align:center;padding:60px 20px;"><div style="font-size:64px;margin-bottom:16px">' + icon + '</div><div style="font-size:18px;font-weight:600;color:#1F2937;margin-bottom:8px">' + title + '</div><div style="font-size:14px;color:#6B7280;margin-bottom:24px">' + desc + '</div>';
      if (btnText) {
        html += '<a href="' + (btnHref || '#') + '" style="display:inline-block;padding:10px 24px;background:#3B82F6;color:#fff;border-radius:8px;text-decoration:none;font-size:14px">' + btnText + '</a>';
      }
      html += '</div>';
      return html;
    },

    // ============ 生成骨架屏HTML ============
    getSkeletonHTML: function(count) {
      count = count || 3;
      var html = '';
      for (var i = 0; i < count; i++) {
        html += '<div style="padding:16px;border:1px solid #E5E7EB;border-radius:8px;margin-bottom:12px;"><div class="skeleton" style="height:20px;width:60%;margin-bottom:12px"></div><div class="skeleton" style="height:14px;width:40%"></div></div>';
      }
      return html;
    }
  };
})();
