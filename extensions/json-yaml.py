import json
import yaml
import urllib
import appex
import clipboard

uri = clipboard.get()
if appex.get_url():
    uri = appex.get_url()

webf = urllib.urlopen(uri)
txt = webf.read()

y = yaml.dump(yaml.load(json.dumps(json.loads(txt))), default_flow_style=False)

clipboard.set(y)
