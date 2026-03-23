INIT_JS = r'''var _refreshTimer=null;
function startRefresh(){clearInterval(_refreshTimer);_refreshTimer=setInterval(function(){if(S.auth&&(S.tab==='servers'||S.tab==='monitor')){loadStatus().then(function(){var prev=S._prevOnBackup;S._prevOnBackup=S.status&&S.status.on_backup;if(S.status&&S.status.on_backup&&!prev){loadAll()}else{R()}});if(S.tab==='monitor')loadNetHistory().then(function(){drawNetChart()})}},10000)}

document.addEventListener('keydown',function(e){if(e.key==='Escape'&&S.modal){S.modal=null;R()}});
applyTheme();checkAuth().then(function(){if(S.auth)loadAll()});startRefresh();'''
