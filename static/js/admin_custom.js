/* ==========================================================================
   Heat Wheels — Admin JS Enhancements
   ========================================================================== */

(function () {
  'use strict';

  // Run after DOM is ready
  document.addEventListener('DOMContentLoaded', function () {

    // ---- 1. Smooth fade-in for inline form rows ----
    var inlineRows = document.querySelectorAll('.inline-related');
    inlineRows.forEach(function (row, i) {
      row.style.opacity = '0';
      row.style.transform = 'translateY(10px)';
      row.style.transition = 'opacity 0.35s ease, transform 0.35s ease';
      setTimeout(function () {
        row.style.opacity = '1';
        row.style.transform = 'translateY(0)';
      }, 60 * i);
    });

    // ---- 2. Auto-dismiss success messages after 5s ----
    var messages = document.querySelectorAll('.messagelist li');
    messages.forEach(function (msg) {
      msg.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
      setTimeout(function () {
        msg.style.opacity = '0';
        msg.style.transform = 'translateY(-10px)';
        setTimeout(function () {
          msg.remove();
        }, 500);
      }, 5000);
    });

    // ---- 3. Enhanced file inputs — show filename preview ----
    var fileInputs = document.querySelectorAll('input[type="file"]');
    fileInputs.forEach(function (input) {
      input.addEventListener('change', function () {
        var fileName = this.files[0] ? this.files[0].name : '';
        // Remove any previous preview
        var existing = this.parentNode.querySelector('.c2c-file-preview');
        if (existing) existing.remove();

        if (fileName) {
          var preview = document.createElement('span');
          preview.className = 'c2c-file-preview';
          preview.textContent = '📄 ' + fileName;
          preview.style.cssText =
            'display:inline-block;margin-top:8px;padding:6px 14px;' +
            'background:rgba(249,115,22,0.1);color:#f97316;' +
            'border-radius:8px;font-size:0.82rem;font-weight:500;';
          this.parentNode.appendChild(preview);
        }

        // Image thumbnail preview
        if (this.files[0] && this.files[0].type.startsWith('image/')) {
          var existingThumb = this.parentNode.querySelector('.c2c-thumb-preview');
          if (existingThumb) existingThumb.remove();

          var reader = new FileReader();
          var parent = this.parentNode;
          reader.onload = function (e) {
            var thumb = document.createElement('img');
            thumb.src = e.target.result;
            thumb.className = 'c2c-thumb-preview';
            thumb.style.cssText =
              'display:block;margin-top:12px;max-width:180px;max-height:120px;' +
              'border-radius:10px;border:1px solid #2a2e3d;' +
              'box-shadow:0 4px 12px rgba(0,0,0,0.25);';
            parent.appendChild(thumb);
          };
          reader.readAsDataURL(this.files[0]);
        }
      });
    });

    // ---- 4. Table row click to navigate (changelist) ----
    var resultRows = document.querySelectorAll('#result_list table tbody tr');
    resultRows.forEach(function (row) {
      var link = row.querySelector('th a, td a');
      if (link) {
        row.style.cursor = 'pointer';
        row.addEventListener('click', function (e) {
          // Don't navigate if clicking on a checkbox or a link directly
          if (e.target.tagName === 'INPUT' || e.target.tagName === 'A') return;
          link.click();
        });
      }
    });

    // ---- 5. Collapsible fieldsets ----
    var fieldsets = document.querySelectorAll('fieldset h2');
    fieldsets.forEach(function (h2) {
      var fieldset = h2.closest('fieldset');
      if (!fieldset) return;

      // Add toggle indicator
      var indicator = document.createElement('span');
      indicator.textContent = ' ▾';
      indicator.style.cssText = 'float:right;font-size:0.9rem;transition:transform 0.3s;';
      h2.appendChild(indicator);
      h2.style.cursor = 'pointer';

      var content = [];
      var children = fieldset.children;
      for (var i = 0; i < children.length; i++) {
        if (children[i] !== h2) {
          content.push(children[i]);
        }
      }

      h2.addEventListener('click', function () {
        var isCollapsed = content[0] && content[0].style.display === 'none';
        content.forEach(function (el) {
          el.style.display = isCollapsed ? '' : 'none';
        });
        indicator.style.transform = isCollapsed ? '' : 'rotate(-90deg)';
      });
    });

    // ---- 6. Focus highlight for active form row ----
    var formRows = document.querySelectorAll('.form-row');
    formRows.forEach(function (row) {
      var inputs = row.querySelectorAll('input, select, textarea');
      inputs.forEach(function (input) {
        input.addEventListener('focus', function () {
          row.style.background = 'rgba(249, 115, 22, 0.04)';
          row.style.borderRadius = '8px';
          row.style.transition = 'background 0.2s ease';
        });
        input.addEventListener('blur', function () {
          row.style.background = '';
        });
      });
    });

    // ---- 7. Confirm before delete ----
    var deleteLinks = document.querySelectorAll('.deletelink');
    deleteLinks.forEach(function (link) {
      link.addEventListener('click', function (e) {
        if (!confirm('Are you sure you want to delete this? This action cannot be undone.')) {
          e.preventDefault();
        }
      });
    });

  });
})();
