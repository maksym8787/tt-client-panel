SETTINGS_JS = r'''async function loadSettings(){try{var r=await api('/settings');S.settings=r.settings||r||{}}catch(e){toast(e.message,true)}R()}

async function svcAct(a,btn){await withLoading(btn,async function(){try{await api('/service/'+a,{method:'POST'});toast(a+' ok');setTimeout(loadStatus,2000)}catch(e){toast(e.message,true)}})}
async function saveSettings(data){try{var r=await api('/settings',{method:'PUT',body:JSON.stringify(data)});S.settings=r.settings||data;toast(t('saved'));R()}catch(e){toast(e.message,true)}}
async function chgAdmin(pw,btn){await withLoading(btn,async function(){try{await api('/change-password',{method:'POST',body:JSON.stringify({password:pw})});toast(t('saved'));S.modal=null;S.auth=false;R()}catch(e){toast(e.message,true)}})}

function renderSettings(){
  var cfg=S.settings;
  var dnsArr=Array.isArray(cfg.dns_upstreams)?cfg.dns_upstreams:[];
  var exclArr=Array.isArray(cfg.exclusions)?cfg.exclusions:[];
  var hci,afe,aft,vpm,kse,dnsi,exci,mtui,actt,fot;
  return h('div',null,
    h('div',{className:'card'},
      h('div',{className:'card-t'},t('settings')),
      h('div',{className:'grid grid2'},
        h('div',{className:'fg'},
          fl(t('health_interval'),'health'),
          hci=h('input',{className:'input input-m',type:'number',min:'10',max:'300',value:String(cfg.health_check_interval||30)})),
        h('div',{className:'fg'},
          fl(t('auto_failover'),'failover'),
          h('div',{style:{display:'flex',alignItems:'center',gap:'10px'}},
            afe=h('label',{className:'toggle'},h('input',{type:'checkbox',checked:cfg.auto_failover!==false}),h('span',{className:'slider'})),
            h('span',{style:{fontSize:'11px',color:'var(--tx3)'}},t('threshold')+':'),
            aft=h('input',{className:'input input-m',type:'number',min:'1',max:'10',value:String(cfg.failover_threshold||3),style:{width:'60px'}}),
            h('span',{style:{fontSize:'10px',color:'var(--tx3)'}},t('failures'))))),
      h('div',{className:'grid grid2'},
        h('div',{className:'fg'},
          fl(t('vpn_mode'),'vpn_mode'),
          vpm=h('select',{className:'input'},
            h('option',{value:'general',selected:(cfg.vpn_mode||'general')==='general'},t('general')),
            h('option',{value:'selective',selected:cfg.vpn_mode==='selective'},t('selective')))),
        h('div',{className:'fg'},
          fl(t('killswitch'),'killswitch'),
          h('div',{style:{display:'flex',alignItems:'center',gap:'10px'}},
            kse=h('label',{className:'toggle'},h('input',{type:'checkbox',checked:cfg.killswitch_enabled!==false}),h('span',{className:'slider'}))))),
      h('div',{className:'grid grid2'},
        h('div',{className:'fg'},
          fl(t('activate_timeout'),'activate_timeout'),
          actt=h('input',{className:'input input-m',type:'number',min:'3',max:'30',value:String(cfg.activate_timeout||10)})),
        h('div',{className:'fg'},
          fl(t('failover_timeout'),'failover_timeout'),
          fot=h('input',{className:'input input-m',type:'number',min:'3',max:'15',value:String(cfg.failover_timeout||5)}))),
      h('div',{className:'grid grid2'},
        h('div',{className:'fg'},
          fl(t('dns'),'dns'),
          dnsi=h('input',{className:'input input-m',value:dnsArr.join(', '),placeholder:'8.8.8.8, 1.1.1.1'})),
        h('div',{className:'fg'},
          fl(t('mtu'),'mtu'),
          mtui=h('input',{className:'input input-m',type:'number',min:'1200',max:'9000',value:String(cfg.mtu_size||1280)}))),
      h('div',{className:'fg'},
        fl(t('exclusions_label'),'exclusions'),
        exci=h('textarea',{className:'input input-m',value:exclArr.join('\n'),placeholder:'example.com\n10.0.0.0/8',style:{minHeight:'80px'}})),
      h('button',{className:'btn btn-p',onClick:function(){
        var dnsVal=dnsi.value.trim()?dnsi.value.split(',').map(function(s){return s.trim()}).filter(Boolean):[];
        var exclVal=exci.value.trim()?exci.value.split('\n').map(function(s){return s.trim()}).filter(Boolean):[];
        saveSettings({
          health_check_interval:parseInt(hci.value)||30,
          auto_failover:afe.querySelector('input').checked,
          failover_threshold:parseInt(aft.value)||3,
          vpn_mode:vpm.value,
          killswitch_enabled:kse.querySelector('input').checked,
          dns_upstreams:dnsVal,
          mtu_size:parseInt(mtui.value)||1280,
          activate_timeout:parseInt(actt.value)||10,
          failover_timeout:parseInt(fot.value)||5,
          exclusions:exclVal
        })}},t('save'))),
    null);
}
'''
