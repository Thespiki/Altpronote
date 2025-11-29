document.addEventListener('DOMContentLoaded', function(){
  // Theme switching
  document.querySelectorAll('.swatch').forEach(function(btn){
    btn.addEventListener('click', function(){
      var theme = btn.getAttribute('data-theme');
      document.body.className = theme;
      // persist
      try{ localStorage.setItem('alt-theme', theme); }catch(e){}
    });
  });

  // restore theme
  try{
    var t = localStorage.getItem('alt-theme');
    if(t) document.body.className = t;
  }catch(e){}

  // Helper to post JSON and show result
  async function postJSON(url, data){
    const res = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
    const json = await res.json().catch(()=>({error: 'invalid response'}));
    return {status: res.status, body: json};
  }

  // Register form
  var reg = document.getElementById('registerForm');
  if(reg){
    reg.addEventListener('submit', async function(e){
      e.preventDefault();
      var fd = new FormData(reg);
      var data = {};
      fd.forEach((v,k)=>{ data[k]=v; });
      var res = await postJSON('/register', data);
      var out = document.getElementById('registerResult');
      if(res.status===201) out.textContent = '✔ ' + (res.body.message || 'Compte créé');
      else out.textContent = '✖ ' + (res.body.error || JSON.stringify(res.body));
    });
  }

  // Login form
  var log = document.getElementById('loginForm');
  if(log){
    log.addEventListener('submit', async function(e){
      e.preventDefault();
      var fd = new FormData(log);
      var data = {};
      fd.forEach((v,k)=>{ data[k]=v; });
      var res = await postJSON('/login', data);
      var out = document.getElementById('loginResult');
      if(res.status===200) out.textContent = '✔ ' + (res.body.message || 'Connecté');
      else out.textContent = '✖ ' + (res.body.error || JSON.stringify(res.body));
    });
  }
});
