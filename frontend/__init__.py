from frontend.styles import STYLES
from frontend.translations import TRANSLATIONS
from frontend.core_js import CORE_JS
from frontend.servers_js import SERVERS_JS
from frontend.monitor_js import MONITOR_JS
from frontend.settings_js import SETTINGS_JS
from frontend.init_js import INIT_JS

FRONTEND_HTML = (
    '<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="UTF-8">\n<meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=5">\n<title>TTClient</title>\n<link rel="icon" type="image/png" sizes="64x64" href="/static/favicon.png?v=2">\n<link href="https://fonts.googleapis.com/css2?family=DM+Sans:opsz,wght@9..40,400;9..40,500;9..40,600;9..40,700&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet" crossorigin="anonymous">\n<script src="/static/chart.umd.min.js" defer></script>\n<style>\n'
    + STYLES +
    '\n</style>\n</head>\n<body>\n<div id="root"></div>\n<script>\n'
    + TRANSLATIONS + '\n' + CORE_JS + '\n' + SERVERS_JS + '\n' + MONITOR_JS + '\n' + SETTINGS_JS + '\n' + INIT_JS +
    '\n</script>\n</body>\n</html>\n'
)
