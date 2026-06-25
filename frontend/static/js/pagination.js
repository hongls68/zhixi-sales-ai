/**
 * 智析销售AI - 分页组件 v1.2
 * 通用分页，支持上一页/下一页/页码跳转
 */
(function() {
  window.pagination = {
    // 配置
    defaults: {
      currentPage: 1,
      pageSize: 20,
      total: 0,
      containerId: 'pagination',
      onPageChange: null
    },

    // 初始化
    init: function(options) {
      var config = {};
      for (var k in this.defaults) config[k] = this.defaults[k];
      for (var k in options) config[k] = options[k];

      var container = document.getElementById(config.containerId);
      if (!container) return;

      // 存储配置
      container.dataset.currentPage = config.currentPage;
      container.dataset.pageSize = config.pageSize;
      container.dataset.total = config.total;
      container.dataset.callback = options.onPageChange ? 'true' : 'false';

      // 存储回调
      if (options.onPageChange) {
        window['paginationCallback_' + config.containerId] = options.onPageChange;
      }

      this.render(config.containerId);
    },

    // 渲染分页UI
    render: function(containerId) {
      var container = document.getElementById(containerId);
      if (!container) return;

      var currentPage = parseInt(container.dataset.currentPage) || 1;
      var pageSize = parseInt(container.dataset.pageSize) || 20;
      var total = parseInt(container.dataset.total) || 0;
      var totalPages = Math.ceil(total / pageSize) || 1;

      if (total <= pageSize) {
        container.innerHTML = '';
        return;
      }

      var html = '<div style="display:flex;align-items:center;justify-content:center;gap:8px;padding:16px 0;">';

      // 上一页
      html += '<button onclick="pagination.goToPage(\'' + containerId + '\', ' + (currentPage - 1) + ')" ' + (currentPage <= 1 ? 'disabled' : '') + ' style="padding:8px 12px;border:1px solid #E5E7EB;border-radius:6px;background:#fff;cursor:pointer;font-size:13px;color:' + (currentPage <= 1 ? '#D1D5DB' : '#374151') + ';">上一页</button>';

      // 页码
      var startPage = Math.max(1, currentPage - 2);
      var endPage = Math.min(totalPages, currentPage + 2);

      if (startPage > 1) {
        html += '<button onclick="pagination.goToPage(\'' + containerId + '\', 1)" style="padding:8px 12px;border:1px solid #E5E7EB;border-radius:6px;background:#fff;cursor:pointer;font-size:13px;">1</button>';
        if (startPage > 2) html += '<span style="color:#9CA3AF;">...</span>';
      }

      for (var i = startPage; i <= endPage; i++) {
        var isActive = i === currentPage;
        html += '<button onclick="pagination.goToPage(\'' + containerId + '\', ' + i + ')" style="padding:8px 12px;border:1px solid ' + (isActive ? '#3B82F6' : '#E5E7EB') + ';border-radius:6px;background:' + (isActive ? '#3B82F6' : '#fff') + ';cursor:pointer;font-size:13px;color:' + (isActive ? '#fff' : '#374151') + ';">' + i + '</button>';
      }

      if (endPage < totalPages) {
        if (endPage < totalPages - 1) html += '<span style="color:#9CA3AF;">...</span>';
        html += '<button onclick="pagination.goToPage(\'' + containerId + '\', ' + totalPages + ')" style="padding:8px 12px;border:1px solid #E5E7EB;border-radius:6px;background:#fff;cursor:pointer;font-size:13px;">' + totalPages + '</button>';
      }

      // 下一页
      html += '<button onclick="pagination.goToPage(\'' + containerId + '\', ' + (currentPage + 1) + ')" ' + (currentPage >= totalPages ? 'disabled' : '') + ' style="padding:8px 12px;border:1px solid #E5E7EB;border-radius:6px;background:#fff;cursor:pointer;font-size:13px;color:' + (currentPage >= totalPages ? '#D1D5DB' : '#374151') + ';">下一页</button>';

      // 显示信息
      html += '<span style="margin-left:16px;font-size:13px;color:#6B7280;">共 ' + total + ' 条</span>';

      html += '</div>';

      container.innerHTML = html;
    },

    // 跳转到指定页
    goToPage: function(containerId, page) {
      var container = document.getElementById(containerId);
      if (!container) return;

      var pageSize = parseInt(container.dataset.pageSize) || 20;
      var total = parseInt(container.dataset.total) || 0;
      var totalPages = Math.ceil(total / pageSize) || 1;

      if (page < 1) page = 1;
      if (page > totalPages) page = totalPages;

      container.dataset.currentPage = page;
      this.render(containerId);

      // 调用回调
      var callback = window['paginationCallback_' + containerId];
      if (typeof callback === 'function') {
        callback(page, pageSize);
      }
    },

    // 更新总数
    updateTotal: function(containerId, total) {
      var container = document.getElementById(containerId);
      if (!container) return;
      container.dataset.total = total;
      container.dataset.currentPage = 1;
      this.render(containerId);
    },

    // 获取当前页
    getCurrentPage: function(containerId) {
      var container = document.getElementById(containerId);
      if (!container) return 1;
      return parseInt(container.dataset.currentPage) || 1;
    }
  };
})();
