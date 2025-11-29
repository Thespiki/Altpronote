document.addEventListener('DOMContentLoaded', function(){
  setupThemeSwitcher();
  loadPermissionsUI();
});

function setupThemeSwitcher(){
  document.querySelectorAll('.swatch').forEach(function(btn){
    btn.addEventListener('click', function(){
      var theme = btn.getAttribute('data-theme');
      document.body.className = theme;
      try{ localStorage.setItem('alt-theme', theme); }catch(e){}
    });
  });
  try{
    var t = localStorage.getItem('alt-theme');
    if(t) document.body.className = t;
  }catch(e){}
}

function getToken(){
  try{ return localStorage.getItem('alt-token'); }catch(e){ return null; }
}

function logout(){
  try{ localStorage.removeItem('alt-token'); }catch(e){}
  window.location.href = '/';
}

async function loadPermissionsUI(){
  var token = getToken();
  if(!token){
    window.location.href = '/';
    return;
  }

  var res = await fetch('/me', {
    headers: { 'Authorization': 'Bearer ' + token }
  });

  if(!res.ok){
    logout();
    return;
  }

  var data = await res.json();
  var user = data.user;
  var content = document.getElementById('permissionsContent');
  
  if(user.role === 'principal'){
    // Principal sees all users and can manage permissions
    loadPrincipalView(token, content);
  } else {
    // Regular user sees their own permissions
    loadUserPermissionsView(user, content);
  }
}

async function loadUserPermissionsView(user, container){
  container.innerHTML = '<p>Your permissions:</p>';
  
  if(user.permissions && user.permissions.length > 0){
    var html = '<div class="permission-item">';
    user.permissions.forEach(function(p){
      html += '<div class="permission-item">';
      html += '<div><strong>' + p.name + '</strong><br><small>' + (p.description || '') + '</small></div>';
      html += '</div>';
    });
    html += '</div>';
    container.innerHTML = html;
  } else {
    container.innerHTML = '<p>You have no permissions.</p>';
  }
}

async function loadPrincipalView(token, container){
  // Load all users
  var res = await fetch('/permissions/user/self', {
    headers: { 'Authorization': 'Bearer ' + token }
  }).catch(e => ({ ok: false }));

  // For now, show simple principal dashboard
  var html = '<p>As Principal, you can manage permissions for all users.</p>';
  html += '<div class="users-list" id="usersList"></div>';
  container.innerHTML = html;

  // Load users (we need to create an endpoint for this)
  loadAllUsers(token);
}

async function loadAllUsers(token){
  // This would require a new endpoint to get all users
  // For now, show a placeholder
  var list = document.getElementById('usersList');
  if(list){
    list.innerHTML = '<p><em>User management features coming soon...</em></p>';
  }
}
