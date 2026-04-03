SERVERS_JS = r'''async function loadAll(){await Promise.all([loadServers(),loadStatus()]);R()}
async function loadServers(){try{var r=await api('/servers');S.servers=r.servers||[];S.activeServerId=r.active_server_id||''}catch(e){toast(e.message,true)}}
async function loadStatus(){try{S.status=await api('/status')}catch(e){}}
async function addServer(data){try{await api('/servers',{method:'POST',body:JSON.stringify(data)});toast(t('server_added'));await loadAll();R()}catch(e){toast(e.message,true)}}
async function deleteServer(id){S.modal={t:'confirm',title:t('delete'),msg:t('delete_confirm'),onOk:async function(btn){await withLoading(btn,async function(){try{await api('/servers/'+id,{method:'DELETE'});toast(t('server_deleted'));S.modal=null;await loadAll();R()}catch(e){toast(e.message,true)}})}};R()}
async function activateServer(id,btn){await withLoading(btn,async function(){try{var r=await api('/servers/'+id+'/activate',{method:'POST'});toast(r.ok?t('activation_ok'):t('activation_fail'),!r.ok);await loadAll();R()}catch(e){toast(e.message,true)}})}
async function editServer(id,data){try{await api('/servers/'+id,{method:'PUT',body:JSON.stringify(data)});toast(t('saved'));S.modal=null;await loadAll();R()}catch(e){toast(e.message,true)}}
async function reorderServers(order){try{await api('/servers/reorder',{method:'PUT',body:JSON.stringify({order:order})})}catch(e){toast(e.message,true)}}
function renderStatusBar(){
  var st=S.status;var hl=st&&st.health?st.health:{};var ok=hl.connected;var srv=st&&st.active_server;
  return h('div',{className:'status-bar'},
    h('span',{className:'dot '+(ok?'dot-on':'dot-off')}),
    h('span',{style:{fontWeight:600}},ok?t('connected')+(srv?' \u2014 '+srv.name:''):t('disconnected')),
    hl.latency_ms?h('span',{style:{color:'var(--tx3)',fontSize:'12px',fontFamily:'var(--m)',marginLeft:'auto'}},t('latency')+': '+hl.latency_ms+'ms'):'',
    hl.external_ip?h('span',{style:{color:'var(--tx3)',fontSize:'12px',fontFamily:'var(--m)'}},t('external_ip')+': '+hl.external_ip):'');
}

function renderServers(){
  var sorted=S.servers.slice().sort(function(a,b){return(a.priority||0)-(b.priority||0)});
  var onBackup=false;
  if(S.activeServerId&&sorted.length>1&&sorted[0].enabled&&sorted[0].id!==S.activeServerId)onBackup=true;
  return h('div',null,
    renderStatusBar(),
    onBackup?h('div',{style:{background:'var(--orbg)',border:'1px solid rgba(245,158,11,.25)',borderRadius:'var(--r2)',padding:'10px 16px',marginBottom:'10px',fontSize:'12px',color:'var(--or)',display:'flex',alignItems:'center',gap:'8px'}},
      '\u26A0 '+t('on_backup_server'),
      h('button',{className:'btn btn-xs btn-p',onClick:function(){var pid=sorted[0].id;api('/servers/'+pid+'/activate',{method:'POST'}).then(function(r){toast(r.message||t('activation_ok'));loadAll()}).catch(function(e){toast(e.message,true)})}},t('switch_to_primary'))):null,
    sorted.length===0?h('div',{className:'card',style:{textAlign:'center',padding:'40px',color:'var(--tx3)'}},t('no_servers')):sorted.map(function(s,i){
      var isActive=s.id===S.activeServerId;
      return h('div',{className:'sc'+(isActive?' sc-active':'')+(!s.enabled?' sc-dis':'')},
        h('div',{style:{display:'flex',flexDirection:'column',gap:'2px',marginRight:'10px',alignItems:'center'}},
          h('span',{style:{fontSize:'10px',color:'var(--tx3)',fontFamily:'var(--m)'}},''+(i+1)),
          h('button',{className:'btn btn-xs',disabled:i===0,onClick:function(){moveServer(i,-1)}},'\u25B2'),
          h('button',{className:'btn btn-xs',disabled:i===sorted.length-1,onClick:function(){moveServer(i,1)}},'\u25BC')),
        h('div',{className:'sc-info'},
          h('div',{style:{display:'flex',alignItems:'center',gap:'8px'}},
            h('span',{className:'sc-name'},s.name||s.hostname),
            isActive?h('span',{className:'badge b-gn'},t('active')):'',
            s.upstream_protocol?h('span',{className:'badge b-bl'},s.upstream_protocol):''),
          h('div',{className:'sc-host'},s.hostname+(s.addresses&&s.addresses.length?' \u2014 '+(Array.isArray(s.addresses)?s.addresses.join(', '):s.addresses):''))),
        h('div',{className:'sc-acts'},
          !isActive?h('button',{className:'btn btn-sm btn-p',onClick:function(e){activateServer(s.id,e.currentTarget)}},t('activate')):'',
          h('button',{className:'btn btn-sm',onClick:function(){S.modal={t:'edit',s:s};R()}},t('edit')),
          h('button',{className:'btn btn-sm btn-d',onClick:function(){deleteServer(s.id)}},t('delete'))));
    }),
    renderAddServer());
}

function moveServer(idx,dir){
  var sorted=S.servers.slice().sort(function(a,b){return(a.priority||0)-(b.priority||0)});
  var ni=idx+dir;if(ni<0||ni>=sorted.length)return;
  var tmp=sorted[idx];sorted[idx]=sorted[ni];sorted[ni]=tmp;
  sorted.forEach(function(s,i){s.priority=i+1});
  S.servers=sorted;
  R();
  toast(t('activating')+'...');
  reorderServers(sorted.map(function(s){return s.id})).then(function(){
    setTimeout(function(){loadAll()},2000);
  });
}

function renderAddServer(){
  var dl,hn,ad,un,pw,nm,proto,sni,ipv6,dpi;
  return h('div',{className:'card'},
    h('div',{className:'card-t'},t('add_server')),
    h('div',{className:'add-tabs'},
      h('button',{className:'add-tab'+(S.addMode==='deeplink'?' on':''),onClick:function(){S.addMode='deeplink';R()}},t('deeplink')),
      h('button',{className:'add-tab'+(S.addMode==='manual'?' on':''),onClick:function(){S.addMode='manual';R()}},t('manual'))),
    S.addMode==='deeplink'?h('div',null,
      h('div',{className:'fg'},fl('Deeplink','deeplink'),dl=h('input',{className:'input input-m',placeholder:t('paste_deeplink')})),
      h('button',{className:'btn btn-p',onClick:function(){addServer({deeplink:dl.value})}},t('add_server'))
    ):h('div',null,
      h('div',{className:'grid grid2'},
        h('div',{className:'fg'},fl(t('name'),'srv_name'),nm=h('input',{className:'input'})),
        h('div',{className:'fg'},fl(t('hostname'),'srv_hostname'),hn=h('input',{className:'input input-m',placeholder:'vpn.example.com'}))),
      h('div',{className:'fg'},fl(t('address'),'srv_address'),ad=h('input',{className:'input input-m',placeholder:'vpn.example.com:443'})),
      h('div',{className:'grid grid2'},
        h('div',{className:'fg'},fl(t('username'),'srv_username'),un=h('input',{className:'input'})),
        h('div',{className:'fg'},fl(t('password'),'srv_password'),pw=h('input',{className:'input',type:'password'}))),
      h('div',{className:'grid grid2'},
        h('div',{className:'fg'},fl(t('protocol'),'srv_protocol'),proto=h('select',{className:'input'},h('option',{value:'http2'},'HTTP/2'),h('option',{value:'http3'},'HTTP/3'))),
        h('div',{className:'fg'},fl('SNI','srv_sni'),sni=h('input',{className:'input input-m',placeholder:t('hostname')}))),
      h('div',{style:{display:'flex',gap:'16px',marginBottom:'14px'}},
        h('label',{style:{display:'flex',alignItems:'center',gap:'6px',fontSize:'12px',cursor:'pointer'}},ipv6=h('input',{type:'checkbox',checked:true}),'IPv6'),
        h('label',{style:{display:'flex',alignItems:'center',gap:'6px',fontSize:'12px',cursor:'pointer'}},dpi=h('input',{type:'checkbox'}),'Anti-DPI')),
      h('button',{className:'btn btn-p',onClick:function(){addServer({hostname:hn.value,addresses:[ad.value||hn.value+':443'],username:un.value,password:pw.value,name:nm.value||hn.value,upstream_protocol:proto.value,custom_sni:sni.value,has_ipv6:ipv6.checked,anti_dpi:dpi.checked})}},t('add_server'))));
}
'''
