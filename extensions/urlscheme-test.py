# coding: utf-8

# pythonista://./extensions/urlscheme-test?action=run&args=&

# Used for testing quicklinks, homescreen shortcuts

# javascript:(function()%7Bif(document.location.href.indexOf('http')===0)document.location.href='pythonista://./extensions/test?action=run&args='+document.location.href;%7D)();


import console, sys
console.alert('Argv: %s' % (str(sys.argv)))
