import json,math,hashlib,copy,sys,re
from pathlib import Path
from mcp_client import call,BASE
ICON=json.loads((BASE/'web/assets/icons.json').read_text())
COLORS={
'bg.canvas':'#F4F6FA','bg.surface':'#FFFFFF','bg.subtle':'#FAFBFC','bg.muted':'#EBEEF3','bg.inverse':'#111623','bg.inverse-2':'#1E2533','bg.brand':'#2446D8','bg.brand-subtle':'#EEF2FF','bg.brand-subtle-2':'#DDE4FF','bg.ai-subtle':'#F3F0FF','bg.success-subtle':'#ECFDF3','bg.warning-subtle':'#FFF6E5','bg.danger-subtle':'#FEF0EF','bg.highlight':'#FDB022',
 'text.primary':'#111623','text.secondary':'#4B5567','text.tertiary':'#647084','text.on-brand':'#FFFFFF','text.brand':'#2446D8','text.link':'#1B36B0','text.ai':'#5B3CD6','text.success':'#067647','text.warning':'#B54708','text.danger':'#B42318','text.inverse':'#FFFFFF','text.inverse-muted':'#C3CAD6',
 'border.subtle':'#DCE1E9','border.default':'#7D879A','border.strong':'#343D4E','border.brand':'#2446D8','border.danger':'#D92D20','action.primary':'#2446D8','action.hover':'#1B36B0','action.pressed':'#16298A','action.danger':'#D92D20','action.disabled-bg':'#EBEEF3','action.disabled-text':'#8D96A8','focus.ring':'#2446D8','focus.ring-on-dark':'#BCC9FF','accent.violet':'#7A5AF8','accent.saffron':'#FDB022','accent.coral':'#D92D20','accent.green':'#12B76A'}
TINTS={'blue':('#EEF2FF','#DDE4FF','#2446D8'),'violet':('#F3F0FF','#E3D9FF','#5B3CD6'),'green':('#ECFDF3','#CDECDC','#067647'),'saffron':('#FFF6E5','#FFE2A1','#934C06'),'coral':('#FEF0EF','#F9D8D4','#B42318'),'slate':('#F4F6FA','#DCE1E9','#343D4E'),'teal':('#EAFBF9','#C0EBE6','#0B6E65')}
for k,v in TINTS.items():
 for j,c in zip(['start','end','ink'],v): COLORS['media.'+k+'.'+j]=c
DARK={**COLORS,'bg.canvas':'#111623','bg.surface':'#1E2533','bg.subtle':'#202938','bg.muted':'#303C4F','bg.brand-subtle':'#242F52','bg.brand-subtle-2':'#344477','bg.ai-subtle':'#30244E','bg.success-subtle':'#153B2D','bg.warning-subtle':'#45341C','bg.danger-subtle':'#482421','text.primary':'#FFFFFF','text.secondary':'#C3CAD6','text.tertiary':'#AAB5C7','text.brand':'#BCC9FF','text.link':'#C5D0FF','text.ai':'#CEBFFF','text.success':'#89E6B1','text.warning':'#FFD18A','text.danger':'#FFB4AE','border.subtle':'#424F63','border.default':'#7D879A','focus.ring':'#BCC9FF'}
FAM={'phone':(16,12,16,36,2,44),'phoneL':(24,12,16,28,3,44),'tablet':(32,16,16,44,3,44),'tabletL':(32,16,16,44,4,44),'desktop':(40,24,16,56,5,44),'wide':(64,32,18,72,6,48),'ultra':(96,40,20,88,8,56),'tv':(96,32,28,80,5,64)}
CLUSTERS=[('mobil-dikey','Mobil · dikey','phone',[(320,480),(360,740),(375,667),(390,844),(430,932)]),('mobil-yatay','Mobil · yatay','phoneL',[(480,320),(667,375),(844,390),(932,430)]),('tablet-dikey','Tablet · dikey','tablet',[(600,960),(768,1024),(1024,1366)]),('tablet-yatay','Tablet · yatay','tabletL',[(960,600),(1024,768),(1366,1024)]),('laptop','Laptop','desktop',[(1280,800),(1440,900),(1728,1117)]),('masaustu','Masaüstü & 5K','desktop',[(1920,1080),(2560,1440)]),('buyuk-ekran','Büyük ekran · 8K','ultra',[(3840,2160)]),('tv','TV · 10-foot','tv',[(1920,1080)])]
PAGES=[('ana-sayfa','Ana Sayfa'),('kategoriler','Kategoriler'),('arama','Arama & Liste'),('urun','Ürün Detayı'),('karsilastirma','Ürün Karşılaştırma'),('tedarikciler','Tedarikçi Arama'),('magaza','Tedarikçi Mağazası'),('flash','Flash Fırsatlar'),('teklif-iste','Teklif İste'),('teklif-karsilastir','Teklif Karşılaştırma'),('sepet','Sepet'),('odeme','Ödeme'),('siparis','Sipariş & Takip'),('mesajlar','Mesajlar'),('panel','Alıcı Paneli'),('giris','Giriş'),('kayit','Kurumsal Kayıt'),('guvence','Ticaret Güvencesi'),('tedarikci-ol','Tedarikçi Olun'),('yardim','Yardım Merkezi'),('hakkimizda','Hakkımızda'),('durumlar','404 & Boş Durumlar')]
PRODUCTS=[
('Organik pamuk penye kumaş','Ege Tekstil','Denizli','₺118 – ₺142,50','500 metre','%92','t-shirt','blue'),('Endüstriyel mikser · 500 L','Anadolu Makina','Konya','₺312.000','1 adet','%88','gear','slate'),('Erken hasat zeytinyağı · 5 L','Ayvalık Zeytincilik','Balıkesir','₺1.090 – ₺1.240','120 teneke','%90','drop','green'),('Porselen karo · 60 × 120','Bilecik Seramik','Bilecik','₺412 – ₺489','300 m²','%86','squares-four','coral'),('Oluklu mukavva koli','Kutuna Ambalaj','İstanbul','₺12,40 – ₺18','2.000 adet','%95','package','saffron'),('LED panel · 36 W','Işıkora Elektrik','Kayseri','₺245 – ₺310','100 adet','%89','lightbulb','blue'),('Masif meşe masa','Ormana Mobilya','Bursa','₺4.800 – ₺6.200','20 adet','%91','chair','saffron'),('PET granül · şeffaf','Poliven Kimya','Kocaeli','₺38 – ₺44','1.000 kg','%93','cube','violet'),('Havalandırmalı fren diski','Anadolu Makina','Konya','₺680 – ₺820','100 adet','%87','gear','slate'),('Saf gül suyu · 1 L','Gülvadi Kozmetik','Isparta','₺84 – ₺110','200 şişe','%94','drop','coral'),('Deri evrak çantası','Dokuva Deri','İzmir','₺1.150 – ₺1.490','50 adet','%90','handbag','saffron'),('Türk kahvesi · 1 kg','Kavruma Gıda','Gaziantep','₺325 – ₺380','100 paket','%96','coffee','coral'),('Afyon mermeri · levha','Taşvera Doğal Taş','Afyon','₺1.240 – ₺1.580','200 m²','%88','squares-four','slate'),('Denizci halatı · 16 mm','Haliva Teknik','Tekirdağ','₺52 – ₺68','500 metre','%92','link-copy','teal')]
SECTORS=[('Tekstil & Giyim','t-shirt','blue'),('Makine & Endüstri','gear','slate'),('Gıda & Tarım','leaf','green'),('Yapı & Seramik','squares-four','coral'),('Ambalaj & Baskı','package','saffron'),('Elektrik & Işık','lightbulb','blue'),('Mobilya & Yaşam','chair','saffron'),('Kimya & Plastik','cube','violet'),('Otomotiv','wrench','slate'),('Kozmetik & Bakım','drop','coral')]
SUPPLIERS=[('Ege Tekstil A.Ş.','Denizli','12 yıl','%94','t-shirt'),('Anadolu Makina','Konya','21 yıl','%88','gear'),('Ayvalık Zeytincilik','Balıkesir','16 yıl','%90','leaf'),('Bilecik Seramik','Bilecik','18 yıl','%91','squares-four'),('Kutuna Ambalaj','İstanbul','9 yıl','%96','package')]
EVENTS=['Ege’nin Pamuk Atölyeleri','Anadolu Makine Haftası','Hasattan Sofraya','Yeni Nesil Ambalaj','Işığın Geleceği','Doğal Taş Buluşması']
MASTERS={}; CURRENT={'fam':'phone','body':16,'target':44,'hero':36,'gap':12,'gutter':16,'cols':2,'width':320,'cw':288}
def solid(c):return [{'type':'solid','color':'$'+c if c in COLORS else c}]
def frame(name,children=None,w='fill_container',h='fit_content',layout='vertical',gap=12,pad=0,bg=None,**kw):
 d={'type':'frame','name':name,'width':w,'height':h,'layout':layout,'gap':gap,'padding':pad,'fill':solid(bg) if bg else [],'children':children or [],**kw};return d
def text(s,size=None,color='text.primary',weight=400,name='p',**kw):
 return {'type':'text','name':name,'content':str(s),'width':'fill_container','textGrowth':'fixed-width','fontFamily':'Roboto','fontSize':size or CURRENT['body'],'fontWeight':weight,'lineHeight':1.5 if not name.startswith('h') else 1.16,'fill':solid(color),**kw}
def row(ch,gap=12,name='row',**kw):return frame(name,ch,layout='horizontal',gap=gap,**{'alignItems':'center',**kw})
def comp(key,node,name=None,**over):
 if key not in MASTERS: MASTERS[key]={**node,'name':key,'reusable':True}
 return {'type':'ref','ref':key,'name':name or node['name'],**over}
def icon(name,size=24,color='text.secondary',style='regular'):
 key=f'Icon/{name}/{style}/{size}/{color}'
 paths=ICON.get(name+'/'+style,ICON.get('cube/regular',[]))
 node=frame('icon:'+name,[{'type':'path','name':'path','d':p['d'],'width':size,'height':size,'fill':solid(color),'opacity':p['opacity']} for p in paths],w=size,h=size,layout='none',gap=0)
 return comp(key,node)
def button(label,to=None,kind='Primary',ic=None,action=None,width='fit_content',state='Default'):
 b=CURRENT['body']; target=CURRENT['target']; color='text.on-brand' if kind in ['Primary','Danger'] else 'text.brand'; bg={'Primary':'action.primary','Secondary':'bg.surface','Tertiary':None,'Danger':'action.danger'}[kind]
 if state=='Hover' and kind=='Primary': bg='action.hover'
 if state=='Pressed' and kind=='Primary':bg='action.pressed'
 if state=='Disabled':bg='action.disabled-bg';color='action.disabled-text'
 ch=([icon(ic,24 if b<24 else 32,color)] if ic else [])+[text(label,b,color,500,name='label')]
 for c in ch:
  if c['type']=='text':c['width']='fit_content';c['textGrowth']='auto'
 node=row(ch,8,'button',w=width,h=target,pad=[8,16],bg=bg,cornerRadius=8,justifyContent='center')
 if kind=='Secondary' or state=='Focus':node['stroke']={'thickness':2 if state=='Focus' else 1,'fill':solid('focus.ring' if state=='Focus' else 'border.default')}
 if to:node['events']={'onTap':[{'push':json.dumps('/'+to)}]}
 key=f'Button/{kind}/{state}/{b}/{label}/{ic or ""}'
 return comp(key,node,name=('link:'+to+':'+label if to else 'action:'+(action or 'toast')+':'+label),width=width)
def badge(label,tone='Brand'):
 bg,ink={'Brand':('bg.brand-subtle','text.brand'),'Success':('bg.success-subtle','text.success'),'Warning':('bg.warning-subtle','text.warning'),'Danger':('bg.danger-subtle','text.danger'),'AI':('bg.ai-subtle','text.ai'),'Neutral':('bg.muted','text.secondary'),'Premium':('bg.inverse','text.inverse')}[tone]
 n=frame('badge',[text(label,CURRENT['body'],ink,500)],w='fit_content',pad=[4,8],bg=bg,cornerRadius=4,gap=0)
 return comp(f'Badge/{tone}/{CURRENT["body"]}/{label}',n)
def field(label,value='',kind='text',state='Default'):
 b=CURRENT['body'];box=frame('field-box',[text(value or label,b,'text.secondary')],h=100 if kind=='textarea' else CURRENT['target']+4,pad=12,bg='bg.surface',cornerRadius=8,stroke={'thickness':2 if state=='Focus' else 1,'fill':solid('border.danger' if state=='Error' else 'border.default')})
 n=frame('field:'+kind+':'+label,[text(label,b,'text.primary',500,name='label'),box],gap=8)
 return comp(f'Field/{label}/{kind}/{state}/{b}/{value}',n,name=f'field:{kind}:{label}')
def section(title,children,eyebrow=None):
 return frame('section',[*( [text(eyebrow,CURRENT['body'],'text.ai',600,name='overline')] if eyebrow else []),text(title,32 if CURRENT['fam'] not in ['phone','phoneL'] else 24,weight=600,name='h2'),*children],gap=CURRENT['gap'])
def card(ch,name='card',bg='bg.surface',pad=20,**kw):return frame(name,ch,gap=12,pad=pad,bg=bg,cornerRadius=12,stroke={'thickness':1,'fill':solid('border.subtle')},**kw)
def grid(items,cols=None,name='grid'):
 n=cols or CURRENT['cols'];cw=CURRENT['cw'];g=CURRENT['gap'];rows=[]
 for i in range(0,len(items),n):
  chunk=items[i:i+n];chunks=[]
  for it in chunk:it['width']='fill_container';chunks.append(it)
  rows.append(row(chunks,g,name='grid-row',alignItems='start'))
 return frame(name,rows,gap=g)
def illustration(ic,tint='blue',height=164):
 size=min(height-24,160)
 node=frame('illustration:'+ic,[icon(ic,size,'media.'+tint+'.ink','duotone')],h=height,layout='horizontal',justifyContent='center',alignItems='center',cornerRadius=8,fill=[{'type':'linear_gradient','angle':135,'stops':[{'offset':0,'color':'$media.'+tint+'.start'},{'offset':1,'color':'$media.'+tint+'.end'}]}])
 return comp(f'Illustration/{ic}/{tint}/{height}',node)
def product(idx,small=False):
 title,supplier,city,price,moq,match,ic,tint=PRODUCTS[idx%len(PRODUCTS)];b=CURRENT['body']
 cols=CURRENT['cols'];cw=(CURRENT['cw']-(cols-1)*CURRENT['gap'])/cols
 narrow=cw<175
 media=illustration(ic,tint,120 if narrow else 170 if CURRENT['fam']!='tv' else 240)
 children=[media,badge('Uyum '+match,'AI'),text(title,b if narrow else b+2,weight=600,name='h3'),text(supplier,b,'text.secondary'),text(price,20 if b<20 else b+4,weight=700),text('Min. '+moq,b,'text.secondary'),button('İncele','urun',kind='Secondary',width='fill_container'),button('Karşılaştır',kind='Tertiary',action='compare',width='fill_container')]
 node=card(children,name='product:'+str(idx),pad=12 if narrow else 16)
 return comp(f'ProductCard/{idx}/{CURRENT["fam"]}/{"narrow" if narrow else "regular"}',node,name='product:'+str(idx))
def supplier(idx):
 n,c,y,m,ic=SUPPLIERS[idx%5]
 node=card([row([icon(ic,40,'text.brand'),text(n,20 if CURRENT['body']<20 else 32,weight=600,name='h3')]),text(c+' · '+y+' · Üretici',color='text.secondary'),badge('Doğrulanmış','Success'),text('≤ 4 sa yanıt  ·  %98,6 zamanında',color='text.secondary'),button('Mağazayı gör','magaza',kind='Secondary',width='fill_container')])
 return comp(f'SupplierCard/{idx}/{CURRENT["fam"]}',node)
def event(idx):
 return card([row([badge('23 sa 14 dk','Warning'),icon('lightning',24,'text.warning')]),text(EVENTS[idx],24 if CURRENT['body']<24 else 36,weight=600,name='h3'),text('%18’e varan toptan indirim',color='text.secondary'),frame('progress:64',[],h=8,bg='bg.muted',cornerRadius=4),text('Kontenjanın %64’ü doldu',color='text.secondary'),button('Fırsatları gör','flash',kind='Secondary',width='fill_container')],bg='bg.warning-subtle')
def search(label='Ürün veya tedarikçi ara',hero=False):
 ch=[field(label,'Denizli’den 5.000 m organik penye' if hero else '',kind='search'),button('Eşleştir' if hero else 'Ara','arama',ic='sparkle' if hero else 'magnifying-glass',width='fill_container' if CURRENT['fam']=='phone' else 'fit_content')]
 return frame('search-form',ch,layout='vertical' if CURRENT['fam']=='phone' else 'horizontal',alignItems='end',gap=12,pad=16 if hero else 0,bg='bg.surface' if hero else None,cornerRadius=12)
def stat(value,label,detail=''):
 return card([text(value,36 if CURRENT['body']<24 else 48,weight=700),text(label,weight=500),text(detail,color='text.secondary')] if detail else [text(value,36 if CURRENT['body']<24 else 48,weight=700),text(label,weight=500)])
def intro(title,desc='',tag=None):
 return frame('intro',[*([badge(tag,'AI')] if tag else []),text(title,CURRENT['hero'],weight=700,name='h1'),*([text(desc,CURRENT['body']+2,'text.secondary')] if desc else [])],gap=16)
def nav():
 fam=CURRENT['fam'];b=CURRENT['body'];g=CURRENT['gutter'];w=CURRENT['width'];n=[]
 brand=text('arasta',28 if fam=='phone' else 32 if b<24 else 44,'text.brand',700,name='brand');brand['width']='fit_content'
 if fam=='phone':
  n=[row([brand,button('Yardım','yardim',kind='Tertiary',ic='question'),button('Sepet','sepet',kind='Tertiary',ic='shopping-cart')],8,justifyContent='space_between'),search()]
  # At 320px a concise logo/action header preserves 44px controls.
  n[0]['children']=[brand,button('Yardım','yardim',kind='Tertiary'),button('Sepet','sepet',kind='Tertiary')]
  n[1]=row([frame('field:search:Ürün ara',[frame('field-box',[text('Ürün veya üretici',16,'text.secondary')],h=48,pad=12,bg='bg.subtle',cornerRadius=8,stroke={'thickness':1,'fill':solid('border.default')})],gap=0),button('Ara','arama',width='fit_content')],8,name='search-form')
 elif fam=='phoneL':return comp('Header/phoneL',frame('header',[search()],pad=[8,24],bg='bg.surface'))
 elif fam=='tablet':n=[row([brand,button('Hesabım','panel',kind='Tertiary'),button('Sepet','sepet',kind='Secondary')],justifyContent='space_between'),search(),row([button('Kategoriler','kategoriler','Tertiary'),button('Üreticiler','tedarikciler','Tertiary'),button('Teklif iste','teklif-iste','Primary')],8)]
 elif fam=='tv':n=[row([brand,button('Keşfet','ana-sayfa','Tertiary'),button('Kategoriler','kategoriler','Tertiary'),button('Fırsatlar','flash','Tertiary'),button('Hesap','giris','Tertiary')],gap=32,justifyContent='space_between')]
 else:
  if fam in ['desktop','wide','ultra']:
   n.append(row([text('Üreticiden işletmenize. Güvenle.',b,'text.secondary'),button('Ticaret güvencesi','guvence','Tertiary'),button('Tedarikçi olun','tedarikci-ol','Tertiary'),button('Yardım','yardim','Tertiary')],gap=16))
  n += [row([brand,search(),button('Hesabım','panel','Tertiary',ic='user'),button('Sepet','sepet','Secondary',ic='shopping-cart')],24,justifyContent='space_between')]
  if fam!='tabletL':n +=[row([button('Tüm kategoriler','kategoriler','Tertiary',ic='squares-four'),button('Doğrulanmış üreticiler','tedarikciler','Tertiary'),button('Flash fırsatlar','flash','Tertiary',ic='lightning'),button('Teklif iste','teklif-iste','Primary'),button('⌘ K',kind='Tertiary',action='command')],24)]
 node=frame('header',n,pad=[12,g],bg='bg.surface',gap=12,stroke={'thickness':{'bottom':1},'fill':solid('border.subtle')})
 return comp('Header/'+fam,node)
def bottom(active='ana-sayfa'):
 ch=[]
 for s,l,ic in [('ana-sayfa','Keşfet','house'),('kategoriler','Kategori','squares-four'),('teklif-iste','Teklifler','clipboard-text'),('panel','Hesap','user')]:
  n=frame('link:'+s+':'+l,[icon(ic,24,'text.brand' if s==active else 'text.secondary'),text(l,16,'text.brand' if s==active else 'text.secondary',500,textAlign='center')],pad=[8,0],gap=4,alignItems='center',h=72)
  ch.append(n)
 return comp('BottomNav/'+active,row(ch,0,'nav:Alt menü',bg='bg.surface',stroke={'thickness':{'top':1},'fill':solid('border.subtle')}))
def rail(active):
 ch=[text('arasta',20,'text.brand',700,textAlign='center')]
 for s,l,ic in [('ana-sayfa','Keşfet','house'),('kategoriler','Kategori','squares-four'),('teklif-iste','Teklif','clipboard-text'),('panel','Hesap','user'),('yardim','Yardım','question')]:ch.append(frame('link:'+s+':'+l,[icon(ic,24,'text.brand'),text(l,16,'text.brand',500,textAlign='center')],gap=4,pad=8,alignItems='center'))
 return comp('Rail/'+active,frame('nav:Yan menü',ch,w=96,h='fill_container',pad=[16,8],bg='bg.surface',gap=8))
def footer():
 return comp('Footer/'+CURRENT['fam'],frame('footer',[row([text('arasta',28,'text.brand',700),button('Yardım','yardim','Tertiary')],justifyContent='space_between'),text('Üretimin gücü, ticaretin güveni.',color='text.secondary'),grid([button('Hakkımızda','hakkimizda','Tertiary'),button('Güvence','guvence','Tertiary'),button('Tedarikçi olun','tedarikci-ol','Tertiary')],1 if CURRENT['fam']=='phone' else 3),text('© 2026 arasta · Örnek B2B deneyimi',color='text.secondary')],pad=24,bg='bg.surface',gap=16))
def page_content(slug):
 f=CURRENT['fam'];narrow=f in ['phone','phoneL'];b=CURRENT['body'];cols=CURRENT['cols'];hero=CURRENT['hero'];gap=CURRENT['gap']
 def blocks(items,n=2):return grid(items,1 if narrow else n)
 def check(label):return frame('check:'+label,[row([icon('check-square',24,'text.brand'),text(label)])],pad=[8,0])
 def table(headers,rows,name='table'):
  if narrow:
   return frame('table-cards',[card([text(str(r[0]),24,weight=600,name='h3'),*[text(h+': '+str(v)) for h,v in zip(headers[1:],r[1:])]]) for r in rows],gap=12)
  return frame('table:'+name,[row([text(h,b,'text.secondary',600,name='th') for h in headers],16,'tr',pad=[16,20],bg='bg.muted'),*[row([text(v,b,weight=600 if j==0 else 400,name='td') for j,v in enumerate(r)],16,'tr',pad=[16,20],bg='bg.surface') for r in rows]],gap=2)
 def timeline(labels):return frame('timeline',[row([badge(str(i+1),'Success' if i<2 else 'Brand'),frame('step',[text(l,weight=600),text(['Tamamlandı','Tamamlandı','İşleniyor','Sıradaki'][min(i,3)],color='text.secondary')],gap=4)]) for i,l in enumerate(labels)],gap=20)
 def form_fields(items,cta,to=None):return card([*[field(*a) for a in items],button(cta,to,width='fill_container',action='submit')],pad=24)
 if slug=='ana-sayfa':
  heroIntro=frame('hero-copy',[badge('48.000 doğrulanmış üretici','Brand'),text('Doğru üretici.\nGüçlü ticaret.',hero,'text.primary',700,name='h1'),text('İhtiyacınızı anlatın. Türkiye’nin üreticileriyle akıllı, güvenceli toptan alım yapın.',b+2,'text.secondary'),search('İhtiyacınızı doğal dille yazın',True),grid([badge('GOTS sertifikalı','AI'),badge('≤ 30 gün teslim','AI')],2),button('Üreticileri keşfet','tedarikciler','Tertiary',ic='arrow-right')],gap=20)
  collage=frame('collage',[card([row([icon('seal-check',32,'text.success'),text('Ege Tekstil',24,weight=600)]),text('Denizli · Doğrulanmış üretici',color='text.secondary'),illustration('t-shirt','blue',160),row([text('%94 uyum',24,'text.ai',700),badge('GOTS','Success')])],pad=24),row([stat('₺24.600','Potansiyel tasarruf'),card([badge('Yeni teklif','Success'),text('₺118 / metre',24,weight=700),text('5.000 m · 21 gün',color='text.secondary')])],16)],gap=16)
  top=frame('hero',[heroIntro] if narrow else [heroIntro,collage],layout='vertical' if narrow else 'horizontal',gap=32,pad=24 if narrow else 40,cornerRadius=12,fill=[{'type':'linear_gradient','angle':135,'stops':[{'offset':0,'color':'$bg.brand-subtle'},{'offset':1,'color':'$bg.ai-subtle'}]}])
  trust=grid([row([icon(ic,24,'text.brand'),text(label,b,'text.secondary',500)]) for ic,label in [('shield-check','Güvenceli ödeme'),('seal-check','Doğrulanmış üretici'),('truck','81 ile teslimat')]],1 if narrow else 3)
  sectors=grid([card([illustration(ic,tint,104),button(l,'kategoriler','Tertiary',width='fill_container')],pad=12) for l,ic,tint in SECTORS[:(6 if narrow else 10)]],2 if narrow else cols)
  return [top,trust,section('İşinizin ihtiyacı, burada.',[sectors],'SEKTÖRLER'),section('Bugünün toptan fırsatları',[blocks([event(0),event(1)])],'FLASH ETKİNLİKLER'),card([badge('AI TEKLİF ASİSTANI','AI'),text('Tek ihtiyacınız, doğru bir cümle.',32,weight=600,name='h2'),text('Miktarı, teslimat süresini ve belgeleri yazın. Talebinizi birlikte hazırlayalım.'),button('Teklif talebi oluştur','teklif-iste',ic='sparkle')],bg='bg.ai-subtle',pad=32),section('Sizin için seçtiklerimiz',[grid([product(i) for i in range(6 if narrow else 10)])],'AKILLI EŞLEŞTİRME'),section('Üretimin arkasındaki uzmanlar',[blocks([supplier(0),supplier(1),supplier(2)],3)],'DOĞRULANMIŞ ÜRETİCİLER'),card([text('Satın alma ekibiniz için.',32,weight=600,name='h2'),text('Onay akışları, harcama limitleri ve sipariş görünürlüğü tek çalışma alanında.'),button('Alıcı panelini incele','panel','Secondary')],bg='bg.brand-subtle',pad=32)]
 if slug=='kategoriler':
  return [intro('Üretimin tüm alanları.','10 sektör. Binlerce uzman üretici.'),search(),grid([card([illustration(ic,tint,124),text(l,24,weight=600,name='h2'),text('Üreticileri, malzemeleri ve yeni fırsatları keşfedin.',color='text.secondary'),button('Ürünleri gör','arama','Secondary',width='fill_container')]) for l,ic,tint in SECTORS],2 if narrow else cols),section('Popüler toptan ürünler',[grid([product(i) for i in range(6)])])]
 if slug=='arama':
  filters=card([text('Filtreler',24,weight=600,name='h2'),field('Minimum sipariş','500','number'),field('Şehir','Denizli','select'),field('Teslimat','30 gün içinde','select'),check('Yalnızca stoktakiler'),check('Doğrulanmış üretici'),check('GOTS sertifikası'),button('Filtreleri uygula',action='filter',width='fill_container')],name='filters',w=240)
  results=frame('results',[row([text('14 uygun ürün',24,weight=600,name='h2'),button('Filtrele',action='filters',kind='Secondary',ic='funnel')]),grid([product(i) for i in range(14)]),row([button('1',action='page1'),button('2',kind='Secondary',action='page2'),button('Sonraki',kind='Secondary',action='page2')])],gap=24)
  return [intro('İhtiyacınıza uygun üretim.','Organik penye için doğrulanmış seçenekler.','AI aramanızı yorumladı'),grid([button(l,kind='Secondary',action='remove-chip') for l in ['Organik pamuk ×','Denizli ×','≤ 30 gün ×']],1 if narrow else 3),results if f in ['phone','phoneL','tablet'] else row([filters,results],24,alignItems='start')]
 if slug=='urun':
  details=frame('product-detail',[badge('Ege Tekstil · Doğrulanmış','Success'),intro('Organik pamuk penye kumaş','180 g/m² · %100 pamuk · GOTS sertifikalı'),row([badge('AI uyum %92','AI'),text('★ 4,8 · 312 değerlendirme',color='text.secondary')]),table(['Miktar','Birim fiyat'],[['500–1.999 m','₺142,50'],['2.000–4.999 m','₺128'],['5.000 m ve üzeri','₺118']],'price-tiers'),text('Renk: Doğal ekru',weight=500),row([button('Ekru',kind='Secondary',action='color'),button('Lacivert',kind='Secondary',action='color')]),row([button('−',kind='Secondary',action='minus'),field('Miktar','500','number'),button('+',kind='Secondary',action='plus')]),text('Ara toplam · ₺71.250',24,weight=700,name='subtotal'),button('Sepete ekle',action='cart',ic='shopping-cart',width='fill_container'),button('Numune talep et','teklif-iste','Secondary',width='fill_container')],gap=20)
  gallery=frame('gallery',[illustration('t-shirt','blue',260 if narrow else 440),grid([illustration('t-shirt','blue',100),illustration('leaf','green',100),illustration('seal-check','slate',100)],3)],gap=12)
  return [blocks([gallery,details]),blocks([card([text('Kapınıza kadar maliyet',28,weight=600,name='h2'),field('Teslimat şehri','İstanbul','select'),field('Miktar (metre)','500','number'),button('Maliyeti hesapla',action='landed',width='fill_container'),text('Ürün + nakliye + KDV birlikte.',color='text.secondary',name='landed-result')]),card([icon('shield-check',40,'text.brand'),text('Ticaret Güvencesi',28,weight=600,name='h2'),text('Ödemeniz, teslimatı onaylayana kadar güvence altında tutulur.'),button('Kapsamı incele','guvence','Tertiary')])]),section('Teknik özellikler',[table(['Özellik','Değer'],[['Bileşim','%100 organik pamuk'],['Gramaj','180 g/m²'],['En','180 cm'],['Üretim yeri','Denizli'],['Teslimat','21 gün']])]),section('Birlikte değerlendirilenler',[grid([product(i) for i in [0,4,8,12]])])]
 if slug=='karsilastirma':
  return [intro('Yan yana, daha net.','Fiyatı, minimum siparişi ve teslimatı birlikte değerlendirin.'),card([badge('AI önerisi','AI'),text('Ege Tekstil toplam maliyette %8 avantajlı.',28,weight=600),text('5.000 m ihtiyacınız ve 30 günlük teslimat beklentiniz esas alındı.')],bg='bg.ai-subtle'),table(['Özellik','Ege Tekstil','Dokuva Tekstil','İlmekon Dokuma'],[['Birim fiyat','₺118','₺126','₺132'],['Minimum sipariş','500 m','1.000 m','250 m'],['Teslimat','21 gün','28 gün','14 gün'],['Sertifika','GOTS','GOTS','OEKO-TEX'],['Güvence','Dahil','Dahil','Dahil']]),button('Seçilen ürün için teklif iste','teklif-iste')]
 if slug=='tedarikciler':
  return [intro('Üretimin doğru adresi.','Uzmanlık, kapasite ve teslimat performansına göre eşleşin.'),search(),card([text('Türkiye üretim ağı',28,weight=600,name='h2'),illustration('map-pin','blue',140),text('Denizli: 1.320 · Konya: 910 · Bursa: 840 · İstanbul: 2.450 üretici',color='text.secondary')],bg='bg.brand-subtle'),grid([supplier(i) for i in range(5)],1 if narrow else 3)]
 if slug=='magaza':
  return [card([badge('Doğrulanmış üretici','Success'),intro('Ege Tekstil A.Ş.','Denizli’den dünyaya, sorumlu üretim.'),button('Üreticiye mesaj gönder','mesajlar',ic='chat-circle')],bg='bg.brand-subtle',pad=32),blocks([stat('12 yıl','Üretim deneyimi'),stat('%98,6','Zamanında teslimat'),stat('≤ 4 sa','Ortalama yanıt')],3),section('Güvenin izini sürün',[timeline(['İşletme belgeleri doğrulandı','SGS yerinde denetim','GOTS belgesi güncellendi'])]),section('Üreticinin koleksiyonu',[grid([product(i) for i in [0,4,10,12]])])]
 if slug=='flash':return [card([badge('SINIRLI SÜRE','Warning'),intro('Fırsatın tam zamanı.','Üreticilerin ayrılmış kontenjanlarından yararlanın.'),row([badge('23 saat','Warning'),badge('14 dakika','Warning')])],bg='bg.inverse',pad=32),grid([event(i) for i in range(6)],1 if narrow else 3),section('Etkinlik ürünleri',[grid([product(i) for i in range(8)])])]
 if slug=='teklif-iste':
  return [intro('İhtiyacınızı yazın.\nTeklifler size gelsin.','AI taslağını düzenleyin; göndermeden önce son söz sizde.','AI RFQ'),card([field('İhtiyacınız','Denizli’den 5.000 metre GOTS sertifikalı organik penye; 30 gün içinde teslim.','textarea'),button('Taslağı AI ile doldur',action='draft',ic='sparkle',width='fill_container'),text('1 / 3 · İhtiyaç ve ürün',weight=600),field('Ürün','Organik pamuk penye'),field('Miktar','5000','number'),field('Teslimat süresi','30 gün','select'),field('Sertifika','GOTS'),badge('AI tarafından dolduruldu · %96 güven','AI'),check('Kayıtlı adresimi kullan'),field('Teknik dosya','','file'),button('Talebi incele','teklif-karsilastir',width='fill_container')])]
 if slug=='teklif-karsilastir':return [intro('Üç teklif. Tek net karar.','RFQ-2026-0241 · 5.000 m organik pamuk penye'),card([badge('AI · En iyi toplam değer','AI'),text('Ege Tekstil ile ₺24.600 tasarruf',28,weight=600),text('Fiyat, teslimat ve belge uyumu birlikte değerlendirildi.')],bg='bg.ai-subtle'),table(['Üretici','Toplam','Teslimat','Uyum'],[['Ege Tekstil · En iyi değer','₺590.000','21 gün','%96'],['Dokuva Tekstil','₺630.000','28 gün','%91'],['İlmekon Dokuma','₺660.000','14 gün','%88']],'quotes'),blocks([button('Excel’e aktar',kind='Secondary',action='export',ic='download'),button('Onaya gönder',action='approve',ic='check-circle')])]
 if slug=='sepet':return [intro('Sepetiniz','2 üretici · 3 ürün · Güvenceli satın alma'),blocks([frame('cart-items',[card([text('Ege Tekstil',24,weight=600,name='h2'),text('Organik pamuk penye kumaş'),illustration('t-shirt','blue',120),field('Miktar (metre)','500','number'),text('₺71.250',24,weight=700),badge('1.500 m daha ekleyin, birim fiyat ₺128 olsun','AI'),frame('progress:25',[],h=8,bg='bg.muted',cornerRadius=4)]),card([text('Kutuna Ambalaj',24,weight=600,name='h2'),text('Oluklu mukavva koli · 2.000 adet'),text('₺24.800',24,weight=700)])]),card([text('Sipariş özeti',28,weight=600,name='h2'),text('Ara toplam · ₺96.050'),text('Nakliye · ₺2.400'),text('KDV · ₺19.690'),text('Toplam · ₺118.140',28,weight=700),button('Güvenle ödemeye geç','odeme',ic='lock',width='fill_container'),text('EFT · Kurumsal kart · 60 gün vade',color='text.secondary')])])]
 if slug=='odeme':
  if f=='tv':return tv_handoff('Ödemeyi telefonunuzda tamamlayın.')
  return [intro('Güvenle tamamlayın.','1 · Adres     2 · Ödeme     3 · Onay'),blocks([card([text('Teslimat adresi',24,weight=600,name='h2'),check('Kayıtlı adres: Merkez depo'),text('Örnek Sanayi Bölgesi · İstanbul',color='text.secondary'),field('Satın alma sipariş no (PO)','PO-2026-084'),field('Vergi kimlik numarası (VKN)','','text'),text('Ödeme yöntemi',24,weight=600,name='h2'),*[frame('radio:payment:'+l,[row([icon('circle'),text(l)])],pad=12,bg='bg.surface',cornerRadius=8,stroke={'thickness':1,'fill':solid('border.default')}) for l in ['Banka havalesi / EFT','Kurumsal kart','60 gün açık hesap']],check('Finans ekibimin onayına gönder')]),card([text('Ödenecek tutar',24,weight=600,name='h2'),text('₺118.140',36,weight=700),text('Ödeme teslimat onayına kadar emanette.'),button('Siparişi oluştur','siparis',width='fill_container'),text('Bu prototip gerçek ödeme almaz.',color='text.secondary')])])]
 if slug=='siparis':return [intro('Siparişiniz alındı.','AR-2026-0841 · Ege Tekstil','İşlem başarılı'),card([icon('check-circle',48,'text.success'),text('Ödemeniz güvende',28,weight=600,name='h2'),text('₺118.140 teslimat onayınıza kadar emanette.')],bg='bg.success-subtle'),blocks([card([text('Siparişin yolculuğu',28,weight=600,name='h2'),timeline(['Sipariş onaylandı','Üretim tamamlandı','Kargoya teslim ediliyor','Teslimat onayı'])]),card([illustration('truck','blue',180),text('Tahmini teslimat · 28 Eylül',24,weight=600,name='h2'),text('Son konum: Denizli lojistik merkezi. Son güncelleme 14:32.',color='text.secondary'),button('e-Fatura indir',kind='Secondary',action='invoice',ic='download')])])]
 if slug=='mesajlar':return [intro('Üreticinizle aynı sayfada.','Tüm teklif ve sipariş konuşmaları bir arada.'),blocks([card([text('Görüşmeler',24,weight=600,name='h2'),*[button(n,'mesajlar','Secondary',width='fill_container') for n,*_ in SUPPLIERS[:3]]]),card([row([text('Ege Tekstil',24,weight=600,name='h2'),badge('Çevrimiçi','Success')]),frame('chat-log',[card([text('Merhaba, organik penye için numune gönderebilir misiniz?')],bg='bg.brand-subtle'),card([text('Elbette. Ekru ve lacivert numuneleri bugün hazırlayabiliriz.'),text('14:32 · Okundu',color='text.secondary')])]),button('TR ⇄ EN çeviri',kind='Tertiary',action='translate',ic='translate'),field('Mesajınız','','textarea'),field('Dosya ekle','','file'),button('Mesajı gönder',action='message',ic='paper-plane',width='fill_container')])])]
 if slug=='panel':return [intro('İşinizin bugünü,\nyarının fırsatları.','Hoş geldiniz, Deniz · Örnek satın alma ekibi'),grid([stat('₺842.600','Bu ay satın alma','Önceki aya göre %12 daha verimli'),stat('24','Aktif sipariş','6 teslimat bu hafta'),stat('3','Onay bekliyor','Toplam ₺148.500'),stat('%8,4','AI tasarruf fırsatı','₺70.778 potansiyel')],1 if narrow else 4),section('Harcama görünümü',[card([frame('chart',[row([text(m,w='fill_container') if False else text(m),frame('bar:'+str(v),[],w=v*2 if narrow else v*5,h=24,bg='action.primary',cornerRadius=4),text('₺'+str(v)+'.000')]) for m,v in [('Nisan',84),('Mayıs',96),('Haziran',112),('Temmuz',103),('Ağustos',128),('Eylül',142)]]),table(['Ay','Harcama'],[['Nisan','₺84.000'],['Mayıs','₺96.000'],['Haziran','₺112.000'],['Temmuz','₺103.000'],['Ağustos','₺128.000'],['Eylül','₺142.000']],'chart-data')])]),section('Son siparişler',[table(['Sipariş','Üretici','Tutar','Durum'],[['AR-0841','Ege Tekstil','₺71.250','Hazırlanıyor'],['AR-0836','Kutuna Ambalaj','₺24.800','Yolda'],['AR-0819','Anadolu Makina','₺312.000','Onay bekliyor']])]),button('Onay kuyruğunu aç','teklif-karsilastir')]
 if slug=='giris':
  if f=='tv':return tv_handoff('Hesabınıza telefonunuzla bağlanın.')
  return [intro('Ticaretinize kaldığınız\nyerden devam edin.','Güvenli, hızlı ve erişilebilir giriş.'),form_fields([('E-posta','','email'),('Parola','','password')],'Giriş yap','panel'),button('Passkey ile giriş',action='passkey',ic='fingerprint',width='fill_container'),button('Sihirli bağlantı gönder',action='magic',kind='Secondary',ic='envelope',width='fill_container'),button('Kurumsal SSO',action='sso',kind='Tertiary',width='fill_container'),button('İşletme hesabı oluştur','kayit','Tertiary')]
 if slug=='kayit':return [intro('İşletmenizle arasta’ya katılın.','1 / 3 · İşletme bilgileri'),card([field('Vergi kimlik numarası (VKN)','','text'),button('Bilgileri getir',action='company',ic='buildings',width='fill_container'),field('İşletme adı',''),field('İş e-postası','','email'),field('Yetkili adı',''),check('KVKK aydınlatma metnini okudum'),button('Devam et','panel',width='fill_container')])]
 if slug=='guvence':return [intro('Ticaret büyüsün.\nGüven hep sizinle olsun.','Siparişinizden teslimata, her adımda şeffaf koruma.'),blocks([stat('₺2,1 mlr','Güvenceli işlem'),stat('%99,2','Çözüme kavuşan talepler')]),section('Dört adımda güvenli alım',[timeline(['Doğrulanmış üreticiyi seçin','Güvenceli ödeme yapın','Siparişinizi takip edin','Teslimatı kontrol edip onaylayın'])]),section('Neleri kapsar?',[blocks([card([icon('shield-check',40,'text.brand'),text('Ürün ve miktar',24,weight=600,name='h3'),text('Sözleşilen ürün, kalite ve miktar koşullarına göre değerlendirme.')]),card([icon('truck',40,'text.brand'),text('Zamanında teslimat',24,weight=600,name='h3'),text('Belirlenen teslimat tarihine göre takip ve çözüm desteği.')])])]),faq()]
 if slug=='tedarikci-ol':return [intro('Üretiminiz güçlü.\nPazarınız daha da büyük.','Doğru alıcılarla buluşun, kapasitenizi büyütün.'),blocks([stat('48.000+','Üretici'),stat('190','Ülkeye erişim'),stat('24 saat','İlk teklif hedefi')],3),grid([card([badge(name,'Premium' if i==1 else 'Brand'),text(price,36,weight=700),text(desc),text('✓ Doğrulanmış işletme profili\n✓ Ürün vitrini\n✓ Alıcı mesajları'),button('Başvur','kayit','Primary' if i==1 else 'Secondary',width='fill_container')],bg='bg.brand-subtle' if i==1 else 'bg.surface') for i,(name,price,desc) in enumerate([('Başlangıç','Ücretsiz','Dijital vitrininizi açın.'),('Büyüme','₺2.490 / ay','Daha fazla nitelikli alıcıya erişin.'),('Kurumsal','Size özel','Ekibiniz için gelişmiş araçlar.')])],1 if narrow else 3)]
 if slug=='yardim':return [intro('İşiniz aksamasın.','İhtiyacınız olan yanıt, doğru yerde.'),search('Size nasıl yardımcı olabiliriz?'),grid([card([icon(ic,32,'text.brand'),text(l,24,weight=600,name='h2'),button('Yanıtları gör',action='help',kind='Tertiary')]) for l,ic in [('Sipariş & teslimat','truck'),('Ödeme & güvence','shield-check'),('Teklif & ürün','clipboard-text'),('Hesap & erişim','user')]],1 if narrow else 2),faq(),card([text('Birlikte çözelim.',28,weight=600,name='h2'),text('Hafta içi 09.00–18.00 destek ekibimiz yanınızda.'),button('Destek görüşmesi başlat','mesajlar',ic='headset')])]
 if slug=='hakkimizda':return [intro('Türkiye’nin üretim gücü.\nOrtak bir gelecek.','arasta, üreticilerle işletmeleri güven ve teknolojiyle buluşturan kurgusal bir B2B pazaryeridir.'),illustration('factory','blue',260),blocks([stat('81','İlde üretim ağı'),stat('48.000+','Üretici'),stat('10','Ana sektör')],3),section('Bizi bir arada tutan değerler',[blocks([card([text('Güven',28,weight=600,name='h3'),text('Şeffaf koşullar, doğrulanmış bilgiler ve hesap verebilir süreçler.')]),card([text('Birlikte büyüme',28,weight=600,name='h3'),text('Küçük üreticiden büyük işletmeye, daha adil ticaret fırsatları.')]),card([text('Sorumlu teknoloji',28,weight=600,name='h3'),text('Kararı kullanıcıda bırakan, anlaşılır ve erişilebilir AI.')])],3)]),card([text('Bu gelecekte yeriniz var.',32,weight=600,name='h2'),button('Ekibimizle tanışın','yardim','Secondary')],bg='bg.ai-subtle')]
 return [intro('Bu sayfa yolunu kaybetmiş.','Aradığınız ürün ya da üreticiye birlikte ulaşalım.','404'),search(),button('Ana sayfaya dön','ana-sayfa'),section('Henüz burada bir şey yok.',[card([illustration('package','blue',140),text('Kaydettiğiniz ürünler burada görünecek.'),button('Ürünleri keşfet','arama','Secondary')])]),card([text('Planlı bakım',24,weight=600,name='h2'),text('Pazar 02.00–03.00 arasında kısa bir bakım yapıyoruz.',name='status')],bg='bg.warning-subtle'),card([text('Bağlantınız kesildi',24,weight=600,name='h2'),text('Bağlantı geri geldiğinde kaldığınız yerden devam edebilirsiniz.',name='alert'),button('Yeniden dene',action='retry',kind='Secondary')],bg='bg.danger-subtle')]
def faq():return section('Sık sorulan sorular',[comp('FAQ/'+q,card([text(q,20,weight=600),text(a)],name='details:'+q)) for q,a in [('Ödemem ne zaman üreticiye aktarılır?','Teslimatı kontrol edip onayladığınızda aktarım başlatılır.'),('Teklif talebi ücretli mi?','Örnek deneyimde teklif oluşturmak ve karşılaştırmak ücretsizdir.'),('Üreticiler nasıl doğrulanır?','İşletme belgeleri, üretim kapasitesi ve bağımsız denetimler incelenir.')]])
def tv_handoff(title):return [intro(title,'Bu ekrandaki kodu telefonunuzda arasta hesabınıza girin.'),card([icon('qr-code',192,'text.primary'),text('K74QX',48,weight=700,fontFamily='Roboto Mono'),text('Cihaz kodu · 5 dakika geçerli'),button('Yardım al','yardim','Secondary')],alignItems='center')]
def configure(fam,w,h):
 g,gap,b,hero,cols,target=FAM[fam]; cw=min(w,2240 if fam=='wide' else 3200 if fam=='ultra' else w)-2*g-(96 if fam=='phoneL' else 0)
 CURRENT.update(fam=fam,width=w,height=h,gutter=g,gap=gap,body=b,hero=hero,cols=cols,target=target,cw=cw)
def screen(cluster,sid,fam,w,h,slug,title):
 configure(fam,w,h)
 content=page_content(slug)
 # Dark event heroes maintain semantic high contrast.
 if slug=='flash':
  content[0]['fill']=solid('bg.brand-subtle')
 navnode=nav()
 header_h={'phone':132,'phoneL':96,'tablet':256,'tabletL':104,'desktop':224,'wide':240,'ultra':272,'tv':132}[fam]
 main=frame('main',content+[footer()],h=max(96,h-header_h-(72 if fam=='phone' else 0)),gap=40 if fam not in ['phone','phoneL'] else 28,pad=[24 if fam=='phone' else 32,CURRENT['gutter']],clipContent=True)
 if fam in ['wide','ultra']:main['name']='main:max'+str(2240 if fam=='wide' else 3200)
 body=frame('device-content',[navnode,main,*([bottom(slug if slug in ['ana-sayfa','kategoriler','teklif-iste','panel'] else 'ana-sayfa')] if fam=='phone' else [])],w='fill_container',h='fill_container',gap=0)
 return frame('Screen/'+cluster+'/'+sid+'/'+slug,[rail(slug),body] if fam=='phoneL' else [body],w=w,h=h,layout='horizontal' if fam=='phoneL' else 'vertical',gap=0,bg='bg.canvas',clipContent=True,screen='/'+cluster+'/'+sid+'/'+slug,theme={'Mod':'Dark' if fam=='tv' else 'Light','Cihaz':fam})
def library_variants():
 configure('phone',320,480)
 for kind in ['Primary','Secondary','Tertiary','Danger']:
  for state in ['Default','Hover','Pressed','Focus','Disabled','Loading']:button('Devam et',kind=kind,state=state,ic='arrow-right')
 for kind in ['text','select','textarea']:
  for state in ['Default','Focus','Filled','Error','Disabled']:field('Alan etiketi','Girilen değer' if state=='Filled' else '',kind,state)
 for tone in ['Neutral','Brand','Success','Warning','Danger','AI','Premium']:badge(tone,tone)
 for name in sorted(set(k.split('/')[0] for k in ICON))[:80]:
  for size in [16,20,24,32]:icon(name,size)
 for name in ['t-shirt','gear','leaf','squares-four','package','lightbulb','chair','cube','wrench','drop','handbag','coffee','link-copy','factory','truck','shield-check','buildings','briefcase']:illustration(name,'blue',160)
 for checked in ['Checked','Unchecked','Indeterminate']:
  for state in ['Default','Focus','Disabled']:
   comp(f'Checkbox/{checked}/{state}',row([icon('check-square' if checked=='Checked' else 'squares-four',24,'text.brand'),text('Seçenek',16)],h=44))
 for tone in ['success','error','info']:
  comp('Toast/'+tone,card([row([icon('check-circle' if tone=='success' else 'warning' if tone=='error' else 'info'),text({'success':'İşlem tamamlandı','error':'Alanları kontrol edin','info':'Yeni bilginiz var'}[tone])])],w=288))
 for name,shape in [('Radio',icon('circle')),('Switch',icon('toggle-right')),('Tooltip',text('Yardım metni')),('Kbd',text('⌘ K',16,fontFamily='Roboto Mono')),('Avatar',text('DK',20)),('Rating',text('★ 4,8')),('Stepper',row([button('−',kind='Secondary'),text('500'),button('+',kind='Secondary')])),('TierProgress',frame('progress:64',[],h=8,bg='bg.muted')),('Skeleton',frame('skeleton',[],h=48,bg='bg.muted',cornerRadius=8))]:comp(name+'/Default',frame(name,[shape],w=288,pad=12))
def variables():
 v={k:{'type':'color','value':[{'value':val,'theme':{'Mod':'Light'}},{'value':DARK[k],'theme':{'Mod':'Dark'}}]} for k,val in COLORS.items()}
 for k,val in {'radius.xs':4,'radius.s':8,'radius.m':12,'radius.max':12,**{'space.'+str(i):i for i in range(0,129,4)}}.items():v[k]={'type':'number','value':val}
 for fam,vals in FAM.items():
  for k,val in zip(['gutter','gap','body','hero','columns','target'],vals):v[f'device.{fam}.{k}']={'type':'number','value':val}
 return v
IDS={}; META=[]
def refs(n):
 out=set()
 if n.get('type')=='ref':out.add(n['ref'])
 for c in n.get('children',[]):out.update(refs(c))
 return out

def replace_refs(n):
 n=copy.deepcopy(n)
 if n.get('type')=='ref':n['ref']=IDS.get(n['ref'],n['ref'])
 if 'children' in n:n['children']=[replace_refs(c) for c in n['children']]
 return n

def insert_nodes(nodes,pageid=None):
 ops='\n'.join('r'+str(i)+'=I(null,'+json.dumps(n,ensure_ascii=False,separators=(',',':'))+')' for i,n in enumerate(nodes))
 result=call('batch_design',operations=ops,**({'pageId':pageid} if pageid else {}))
 if 'results' not in result:print('unexpected batch reply',str(result)[:1500],flush=True);raise ValueError('missing results')
 return [r.get('id') or r.get('nodeId') or r.get('node_id') for r in result['results']]
def flush_masters(pageid):
 pending=[k for k in MASTERS if k not in IDS]
 while pending:
  available=[k for k in pending if refs(MASTERS[k])<=IDS.keys()]
  if not available:raise ValueError('component dependency cycle')
  for start in range(0,len(available),20):
   keys=available[start:start+20];nodes=[]
   for key in keys:
    d=replace_refs(MASTERS[key]);idx=len(IDS)+len(nodes);nodes.append(d)
   real=insert_nodes(nodes,pageid)
   for key,id in zip(keys,real):IDS[key]=id
   print('masters',len(IDS),flush=True)
  pending=[k for k in MASTERS if k not in IDS]

def snapshot(path):
 call('save_document',filePath='/tmp/'+path)
 print('saved',path,flush=True)

if __name__=='__main__':
 mode=sys.argv[1] if len(sys.argv)>1 else 'first'
 statefile=BASE/'measurements/generator-state.json'
 if statefile.exists():
  old=json.loads(statefile.read_text());IDS.update(old['ids']);lib=old['library'];META.extend(old.get('screens',[]))
 else:
  call('set_themes',themes={'Mod':['Light','Dark'],'Cihaz':list(FAM)})
  call('set_variables',variables=variables())
  created=call('add_page',name='00 · Tasarım Sistemi',children=[])
  print('library page',created,flush=True)
  lib=created.get('pageId') or created.get('id') or '1'
  (BASE/'design').mkdir(exist_ok=True)
 library_variants()
 if mode=='first':
  s=screen('mobil-dikey','320','phone',320,480,'ana-sayfa','Ana Sayfa')
  flush_masters(lib)
  pg=call('add_page',name='01 · Mobil · dikey',children=[]);print('page',pg,flush=True)
  pgs=call('list_pages');print('pages',pgs,flush=True)
  pid=pg.get('pageId') or pg.get('id') or '1'
  rid=insert_nodes([replace_refs(s)],pid)[0]
  META.append({'cluster':'mobil-dikey','screen':'320','family':'phone','width':320,'height':480,'page':'ana-sayfa','title':'Ana Sayfa','id':rid,'pageId':pid})
  print('first screen',rid,flush=True)
  call('set_active_page',index='1')
  snapshot('arasta-first.op')
 statefile.write_text(json.dumps({'ids':IDS,'library':lib,'screens':META},ensure_ascii=False))
 (BASE/'web/catalog.json').write_text(json.dumps({'clusters':CLUSTERS,'pages':PAGES,'families':FAM,'colors':COLORS,'dark':DARK,'products':PRODUCTS,'suppliers':SUPPLIERS,'screens':META},ensure_ascii=False))
