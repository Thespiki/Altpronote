document.addEventListener('DOMContentLoaded', function(){
  setupThemeSwitcher();
  loadProfile();
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

async function loadProfile(){
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
  var info = document.getElementById('profileInfo');
  if(info){
    var html = '<div class="profile-field"><label>Username</label><value>' + user.username + '</value></div>';
    html += '<div class="profile-field"><label>ID</label><value><code>' + user.id + '</code></value></div>';
    html += '<div class="profile-field"><label>Role</label><value>' + user.role + '</value></div>';
    if(user.age) html += '<div class="profile-field"><label>Age</label><value>' + user.age + '</value></div>';
    if(user.email) html += '<div class="profile-field"><label>Email</label><value>' + user.email + '</value></div>';
    if(user.phone) html += '<div class="profile-field"><label>Phone</label><value>' + user.phone + '</value></div>';
    if(user.address) html += '<div class="profile-field"><label>Address</label><value>' + user.address + '</value></div>';
    html += '<div class="profile-field"><label>Created</label><value>' + new Date(user.created_at).toLocaleDateString() + '</value></div>';
    info.innerHTML = html;
  }
}
