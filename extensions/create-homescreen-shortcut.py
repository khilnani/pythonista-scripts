# coding: utf-8
import clipboard, base64, console

rawhtml = '''
<html manifest="shotcut.manifest">
<head>
  <title>⌘ %s</title>
  <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no" />
  <meta name="apple-mobile-web-app-capable" content="yes">

  <link rel="apple-touch-icon-precomposed" href="http://omz-software.com/pythonista/shortcut/Icon57.png">
  <link rel="apple-touch-icon-precomposed" sizes="72x72" href="http://omz-software.com/pythonista/shortcut/Icon72.png">
  <link rel="apple-touch-icon-precomposed" sizes="114x114" href="http://omz-software.com/pythonista/shortcut/Icon114.png">
  <link rel="apple-touch-icon-precomposed" sizes="114x114" href="http://omz-software.com/pythonista/shortcut/Icon144.png">
</head>
<body>
  <script type="text/javascript">
  if (window.navigator.standalone) {
    var scriptName = '%s'
    var args = '%s'
    window.location.href = "pythonista://" + scriptName + "?action=run&args=" + args;
    setTimeout(function(){ window.close(); }, 3000);
  } else {
    alert('To save as a shortcut, please use the "Share" menu and select the "Add to Home Screen" option.');
  }
  </script>
</body>
</html>
'''

title = console.input_alert('Title')
script = console.input_alert('Script')
args = console.input_alert('Args')
html = rawhtml % (title,script,args)

encoded = base64.encodestring(html)
encoded = 'data:text/html;base64,' + encoded
# print encoded
clipboard.set(encoded)
console.alert('Encoded html copied to clipboard. Launch Safari, paste as URL and hit Enter/Go.', button1='OK', hide_cancel_button=True)
