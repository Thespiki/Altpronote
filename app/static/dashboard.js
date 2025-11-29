document.addEventListener('DOMContentLoaded', function(){
  setupThemeSwitcher();
  loadUserInfo();
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

async function loadUserInfo(){
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
  var info = document.getElementById('userInfo');
  if(info){
    info.innerHTML = '<p>Welcome, <strong>' + user.username + '</strong>!</p>' +
      '<p>Role: <strong>' + user.role + '</strong></p>' +
      '<p>ID: <code>' + user.id + '</code></p>';
  }
}
