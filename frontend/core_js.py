CORE_JS = r'''var A='/api';
var S={auth:false,setup:false,loading:true,tab:'servers',
  servers:[],activeServerId:'',status:null,failoverLog:[],settings:{},
  toast:null,modal:null,netHistory:[],netPeriod:1,lang:localStorage.getItem('tt_lang')||'en',
  theme:localStorage.getItem('tt_theme')||'system',addMode:'deeplink',flPage:0};

function t(k){return(T[S.lang]||T.en)[k]||T.en[k]||k}
function setLang(l){S.lang=l;localStorage.setItem('tt_lang',l);if(!S.auth){_patchLoginText()}else{R()}}
function setTheme(th){S.theme=th;localStorage.setItem('tt_theme',th);applyTheme();if(!S.auth){_patchLoginText()}else{R()}}
function _patchLoginText(){var e=document.querySelector('.ls');if(e)e.textContent=S.setup?t('create_admin_pw'):t('enter_admin_pw');var b=document.querySelector('.lc .btn-p');if(b)b.textContent=S.setup?t('create_password'):t('sign_in');var i=document.querySelector('.lc input[type=password]');if(i)i.placeholder=t('password');document.querySelectorAll('.lg button').forEach(function(b,i){b.className=(i===0?S.lang==='en':S.lang==='ru')?'on':''});document.querySelectorAll('.tg button').forEach(function(b,i){b.className=([S.theme==='dark',S.theme==='light',S.theme==='system'][i])?'on':''})}
function applyTheme(){document.documentElement.setAttribute('data-theme',S.theme)}

async function api(p,o){o=o||{};var r=await fetch(A+p,{headers:{'Content-Type':'application/json'},credentials:'same-origin',...o});var d=await r.json();if(!r.ok)throw new Error(d.detail||r.statusText);return d}
function toast(m,e){S.toast={m:m,e:!!e};R();setTimeout(function(){S.toast=null;R()},3500)}
function fmtUptime(sec){if(!sec)return '\u2014';var d=Math.floor(sec/86400),h=Math.floor((sec%86400)/3600),m=Math.floor((sec%3600)/60);if(d>0)return d+'d '+h+'h '+m+'m';if(h>0)return h+'h '+m+'m';return m+'m'}
function withLoading(btn,fn){if(!btn)return fn();var orig=btn.textContent;btn.disabled=true;btn.textContent='...';return Promise.resolve(fn()).finally(function(){if(btn.parentNode){btn.disabled=false;btn.textContent=orig}})}
var _tipEl=null;
function tip(key){var text=t('tip_'+key);if(!text||text===('tip_'+key))return null;return h('span',{style:{cursor:'pointer',fontSize:'11px',color:'var(--ac)',marginLeft:'4px',display:'inline-flex',alignItems:'center',justifyContent:'center',width:'16px',height:'16px',borderRadius:'50%',border:'1px solid var(--ac)',flexShrink:'0',position:'relative',userSelect:'none'},onClick:function(e){e.stopPropagation();if(_tipEl&&_tipEl.parentNode){_tipEl.parentNode.removeChild(_tipEl);_tipEl=null;return}if(_tipEl&&_tipEl.parentNode)_tipEl.parentNode.removeChild(_tipEl);var pop=document.createElement('div');pop.style.cssText='position:fixed;z-index:9999;background:var(--sf);border:1px solid var(--bd);border-radius:8px;padding:10px 14px;font-size:12px;color:var(--tx);max-width:300px;box-shadow:0 4px 20px rgba(0,0,0,.3);line-height:1.5';pop.textContent=text;var rect=e.currentTarget.getBoundingClientRect();pop.style.top=(rect.bottom+6)+'px';pop.style.left=Math.max(8,Math.min(rect.left,window.innerWidth-310))+'px';document.body.appendChild(pop);_tipEl=pop;setTimeout(function(){document.addEventListener('click',function rm(){if(_tipEl){_tipEl.parentNode.removeChild(_tipEl);_tipEl=null}document.removeEventListener('click',rm)})},10)}},'\u2139')}
function fl(label,tipKey){return h('label',{className:'fl',style:{display:'flex',alignItems:'center'}},label,tipKey?tip(tipKey):null)}

function h(t,a){var e=document.createElement(t);var dv=null;if(a){var ks=Object.keys(a);for(var i=0;i<ks.length;i++){var k=ks[i],v=a[k];if(k==='style'&&typeof v==='object')Object.assign(e.style,v);else if(k.substr(0,2)==='on')e.addEventListener(k.slice(2).toLowerCase(),v);else if(k==='className')e.className=v;else if(k==='value'){dv=v}else if(k==='checked'||k==='selected'||k==='disabled'){if(v!==false&&v!=null)e[k]=v}else e.setAttribute(k,v)}}for(var i=2;i<arguments.length;i++){var x=arguments[i];if(Array.isArray(x)){for(var j=0;j<x.length;j++)an(e,x[j])}else an(e,x)}if(dv!==null)e.value=dv;return e}
function an(e,x){if(x==null||x===false||x===undefined)return;if(typeof x==='number')x=String(x);if(typeof x==='string')e.appendChild(document.createTextNode(x));else if(x.nodeType)e.appendChild(x);else if(Array.isArray(x)){for(var i=0;i<x.length;i++)an(e,x[i])}}

async function checkAuth(){try{var r=await api('/auth-status');S.auth=r.authenticated;S.setup=r.setup_required}catch(e){S.auth=false}S.loading=false;R()}
async function doLogin(pw){try{await api('/login',{method:'POST',body:JSON.stringify({password:pw})});S.auth=true;loadAll()}catch(e){toast(e.message,true)}R()}
async function doSetup(pw){try{await api('/setup',{method:'POST',body:JSON.stringify({password:pw})});S.setup=false;await doLogin(pw)}catch(e){toast(e.message,true)}}
async function doLogout(){await api('/logout',{method:'POST'});S.auth=false;R()}

var _rTimer=null;
function R(){if(_rTimer)return;_rTimer=requestAnimationFrame(function(){_rTimer=null;_doRender()})}
function _doRender(){
  var root=document.getElementById('root');
  try{
    var frag=document.createDocumentFragment();
    if(S.toast)frag.appendChild(h('div',{className:'toast '+(S.toast.e?'toast-err':'toast-ok')},S.toast.m));
    if(S.modal)frag.appendChild(renderModal());
    if(S.loading){frag.appendChild(h('div',{className:'loading-box',style:{minHeight:'60vh'}},h('div',{className:'spinner spinner-lg'}),t('loading')));root.replaceChildren(frag);return}
    if(!S.auth){frag.appendChild(renderLogin());root.replaceChildren(frag);return}
    frag.appendChild(renderApp());
    root.replaceChildren(frag);
    if(S.tab==='monitor')setTimeout(drawNetChart,50);
  }catch(err){console.error('R() error:',err)}
}

function langThemeBar(){
  return h('div',{style:{display:'flex',justifyContent:'center',marginTop:'16px',gap:'8px'}},
    h('div',{className:'lg'},
      h('button',{className:S.lang==='en'?'on':'',onClick:function(){setLang('en')}},'EN'),
      h('button',{className:S.lang==='ru'?'on':'',onClick:function(){setLang('ru')}},'\u0420\u0423')),
    h('div',{className:'tg'},
      h('button',{className:S.theme==='dark'?'on':'',onClick:function(){setTheme('dark')}},'\u263E'),
      h('button',{className:S.theme==='light'?'on':'',onClick:function(){setTheme('light')}},'\u2600'),
      h('button',{className:S.theme==='system'?'on':'',onClick:function(){setTheme('system')}},'\u2699')))
}

function renderLogin(){
  var pw;var isS=S.setup;
  var card=h('div',{className:'lw'},h('div',{className:'lc'},
    h('div',{style:{textAlign:'center',marginBottom:'20px'}},h('img',{src:'/static/logo-full.png',className:'logo-img',style:{maxHeight:'56px',maxWidth:'260px',width:'auto',height:'auto',margin:'0 auto 12px'}})),
    h('div',{className:'lt'},isS?t('initial_setup'):''),
    h('div',{className:'ls'},isS?t('create_admin_pw'):t('enter_admin_pw')),
    h('div',{className:'fg'},pw=h('input',{className:'input',type:'password',placeholder:t('password'),style:{textAlign:'center'}})),
    h('button',{className:'btn btn-p',style:{width:'100%',justifyContent:'center',padding:'12px',fontSize:'13px',borderRadius:'10px'},onClick:function(){isS?doSetup(pw.value):doLogin(pw.value)}},isS?t('create_password'):t('sign_in')),
    langThemeBar()));
  setTimeout(function(){if(pw){pw.addEventListener('keydown',function(e){if(e.key==='Enter'){e.preventDefault();(isS?doSetup:doLogin)(pw.value)}});pw.focus()}},50);
  return card;
}

function renderApp(){
  var tabs=[{id:'servers',label:t('servers')},{id:'monitor',label:t('monitor')},{id:'settings',label:t('settings')}];
  return h('div',{className:'app fade-in'},
    h('div',{className:'hdr'},
      h('div',{className:'logo'},
        h('img',{src:'/static/logo-full.png',className:'logo-img',style:{height:'34px',width:'auto'}}),
        h('div',{className:'logo-s',style:{marginLeft:'8px'}},'Client')),
      h('div',{className:'bg'},
        h('div',{className:'lg'},
          h('button',{className:S.lang==='en'?'on':'',onClick:function(){setLang('en')}},'EN'),
          h('button',{className:S.lang==='ru'?'on':'',onClick:function(){setLang('ru')}},'\u0420\u0423')),
        h('div',{className:'tg'},
          h('button',{className:S.theme==='dark'?'on':'',onClick:function(){setTheme('dark')}},'\u263E'),
          h('button',{className:S.theme==='light'?'on':'',onClick:function(){setTheme('light')}},'\u2600'),
          h('button',{className:S.theme==='system'?'on':'',onClick:function(){setTheme('system')}},'\u2699')),
        h('button',{className:'btn btn-xs btn-ghost',onClick:function(){S.modal={t:'chgadmin'};R()}},t('password_btn')),
        h('button',{className:'btn btn-xs btn-ghost',onClick:doLogout},t('logout')))),
    h('div',{className:'tabs'},tabs.map(function(tb){return h('button',{className:'tab'+(S.tab===tb.id?' on':''),
      onClick:function(){S.tab=tb.id;if(tb.id==='servers')loadAll();if(tb.id==='monitor'){loadStatus();loadFailoverLog();loadNetHistory().then(function(){drawNetChart()})}if(tb.id==='settings')loadSettings();R()}},tb.label)})),
    h('div',{className:'tab-content'},S.tab==='servers'?renderServers():S.tab==='monitor'?renderMonitor():renderSettings()));
}

function renderModal(){
  var m=S.modal;if(!m)return h('div');
  var close=function(){S.modal=null;R()};
  var content;
  if(m.t==='confirm'){
    content=h('div',{className:'md'},
      h('div',{className:'md-t'},m.title||t('confirm')),
      h('div',{style:{fontSize:'13px',color:'var(--tx2)',marginBottom:'16px'}},m.msg||''),
      h('div',{className:'bg'},
        h('button',{className:'btn btn-d',onClick:function(e){if(m.onOk)m.onOk(e.currentTarget)}},t('confirm')),
        h('button',{className:'btn',onClick:close},t('cancel'))));
  }else if(m.t==='edit'){
    var ni,hi,ai,ui,pi,proti,snii,ipv6i,dpii;var s=m.s;
    content=h('div',{className:'md',style:{maxWidth:'540px'}},
      h('div',{className:'md-t'},t('edit')+': '+s.name),
      h('div',{className:'grid grid2',style:{gap:'10px'}},
        h('div',{className:'fg'},fl(t('name'),'srv_name'),ni=h('input',{className:'input',value:s.name||''})),
        h('div',{className:'fg'},fl(t('hostname'),'srv_hostname'),hi=h('input',{className:'input input-m',value:s.hostname||''}))),
      h('div',{className:'fg'},fl(t('address'),'srv_address'),ai=h('input',{className:'input input-m',value:(s.addresses||[]).join(', '),placeholder:'host:443, host2:443'})),
      h('div',{className:'grid grid2',style:{gap:'10px'}},
        h('div',{className:'fg'},fl(t('username'),'srv_username'),ui=h('input',{className:'input',value:s.username||''})),
        h('div',{className:'fg'},fl(t('password'),'srv_password'),pi=h('input',{className:'input',type:'password',value:s.password||''}))),
      h('div',{className:'grid grid2',style:{gap:'10px'}},
        h('div',{className:'fg'},fl(t('protocol'),'srv_protocol'),proti=h('select',{className:'input'},h('option',{value:'http2',selected:s.upstream_protocol==='http2'},'HTTP/2'),h('option',{value:'http3',selected:s.upstream_protocol==='http3'},'HTTP/3'))),
        h('div',{className:'fg'},fl('SNI','srv_sni'),snii=h('input',{className:'input input-m',value:s.custom_sni||'',placeholder:t('hostname')}))),
      h('div',{style:{display:'flex',gap:'16px',marginBottom:'14px'}},
        h('label',{style:{display:'flex',alignItems:'center',gap:'6px',fontSize:'12px',cursor:'pointer'}},ipv6i=h('input',{type:'checkbox',checked:s.has_ipv6!==false}),'IPv6'),
        h('label',{style:{display:'flex',alignItems:'center',gap:'6px',fontSize:'12px',cursor:'pointer'}},dpii=h('input',{type:'checkbox',checked:!!s.anti_dpi}),'Anti-DPI')),
      h('div',{className:'bg'},
        h('button',{className:'btn btn-p',onClick:function(){var addrs=ai.value.trim()?ai.value.split(',').map(function(x){return x.trim()}).filter(Boolean):[hi.value+':443'];editServer(s.id,{name:ni.value,hostname:hi.value,addresses:addrs,username:ui.value,password:pi.value,upstream_protocol:proti.value,custom_sni:snii.value,has_ipv6:ipv6i.checked,anti_dpi:dpii.checked})}},t('save')),
        h('button',{className:'btn',onClick:close},t('cancel'))));
  }else if(m.t==='chgadmin'){
    var ap;
    content=h('div',{className:'md'},
      h('div',{className:'md-t'},t('change_password')),
      h('div',{className:'fg'},h('label',{className:'fl'},t('new_password')),ap=h('input',{className:'input',type:'password',placeholder:t('new_password')})),
      h('div',{className:'bg'},
        h('button',{className:'btn btn-p',onClick:function(e){if(ap.value.length<6){toast('Min 6 chars',true);return}chgAdmin(ap.value,e.currentTarget)}},t('save')),
        h('button',{className:'btn',onClick:close},t('cancel'))));
    setTimeout(function(){if(ap)ap.focus()},50);
  }
  return h('div',{className:'mo',onClick:function(e){if(e.target.className&&e.target.className.indexOf('mo')!==-1)close()}},content||h('div'));
}
'''
