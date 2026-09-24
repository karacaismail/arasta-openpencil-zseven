import urllib.request,json,tarfile,io,re,xml.etree.ElementTree as ET
from pathlib import Path
root=Path('/work/repo'); out=root/'web/assets';out.mkdir(parents=True,exist_ok=True)
def fetch(u):return urllib.request.urlopen(u,timeout=45).read()
def pkg(name):
 meta=json.loads(fetch('https://registry.npmjs.org/'+name+'/latest'));return meta,tarfile.open(fileobj=io.BytesIO(fetch(meta['dist']['tarball'])),mode='r:gz')
meta,tar=pkg('@phosphor-icons/core')
names='house squares-four magnifying-glass shopping-cart user bell arrow-right arrow-left caret-down caret-right x plus minus check check-circle shield-check seal-check sparkle factory truck package leaf t-shirt gear lightbulb drop coffee chair cube handbag wrench globe map-pin timer lightning chat-circle file-text clipboard-text chart-bar credit-card bank key envelope eye eye-slash upload download funnel list heart star arrows-left-right command question sign-out warning info dots-three lock qr-code device-mobile monitor television buildings briefcase hand-coins receipt flag calendar clock paper-plane translate link-copy image paperclip check-square circle toggle-left toggle-right copy trash arrow-up-right presentation-chart store tag percent sliders-horizontal book-open broadcast wifi-slash cloud-arrow-up fingerprint recycle headset users certificate puzzle tree camera'.split()
icons={}
for name in names:
 for style in ['regular','duotone']:
  m=next((m for m in tar.getmembers() if m.name.endswith('/'+style+'/'+name+('-duotone' if style=='duotone' else '')+'.svg')),None)
  if not m:continue
  s=ET.fromstring(tar.extractfile(m).read()); paths=[]
  for p in s.iter():
   if p.tag.endswith('path'):paths.append({'d':p.attrib['d'],'opacity':float(p.attrib.get('opacity',1))})
  icons[name+'/'+style]=paths
for m in tar.getmembers():
 if m.name.endswith('/LICENSE'): (out/'Phosphor-LICENSE.txt').write_bytes(tar.extractfile(m).read());break
(root/'measurements/asset-sources.json').write_text(json.dumps({'phosphor':{'version':meta['version'],'url':meta['dist']['tarball']}},indent=2))
(out/'icons.json').write_text(json.dumps(icons,separators=(',',':')))
print('icons',len(icons))
for package,label in [('@fontsource/roboto','Roboto'),('@fontsource/roboto-mono','RobotoMono')]:
 meta,tar=pkg(package)
 for weight in [400,500,600,700]:
  for subset in ['latin','latin-ext']:
   tail=f'/{package.split("/")[-1]}-{subset}-{weight}-normal.woff2'
   m=next((m for m in tar.getmembers() if m.name.endswith(tail)),None)
   if m:(out/f'{label}-{subset}-{weight}.woff2').write_bytes(tar.extractfile(m).read())
 for m in tar.getmembers():
  if m.name.endswith('/LICENSE'):(out/f'{label}-LICENSE.txt').write_bytes(tar.extractfile(m).read());break
print('assets complete')
