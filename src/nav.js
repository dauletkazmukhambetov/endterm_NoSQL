(function() {
  const sidebar = document.getElementById('sidebar');
  const overlay = document.getElementById('sidebar-overlay');
  const toggle = document.getElementById('menu-toggle');
  if (!sidebar || !overlay || !toggle) return;

  function openSidebar() {
    sidebar.classList.add('open');
    overlay.classList.add('visible');
    document.body.style.overflow = 'hidden';
  }
  function closeSidebar() {
    sidebar.classList.remove('open');
    overlay.classList.remove('visible');
    document.body.style.overflow = '';
  }

  toggle.onclick = () => sidebar.classList.contains('open') ? closeSidebar() : openSidebar();
  overlay.onclick = closeSidebar;

  var path = location.pathname || location.href;
  var page = path.split('/').pop().split('?')[0] || 'index.html';
  if (!page) page = 'index.html';
  document.querySelectorAll('.sidebar-nav a').forEach(function(a) {
    var href = (a.getAttribute('href') || '').split('?')[0];
    if (href === page || (page === 'index.html' && (href === 'index.html' || href === ''))) {
      a.classList.add('active');
    } else {
      a.classList.remove('active');
    }
  });
})();
