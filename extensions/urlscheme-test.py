# coding: utf-8

# Used for testing quicklinks, homescreen shortcuts
##    javascript:(function()%7Bif(document.location.href.indexOf('http')===0)document.location.href='pythonista://./extensions/test?action=run&argv='+document.location.href;%7D)();
#
import console, sys
console.alert('''
Script: %s
Argv: %s
''' % (__file__, str(sys.argv)))