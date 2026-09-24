from design import *
sfile=BASE/'measurements/generator-state.json';s=json.loads(sfile.read_text());IDS.update(s['ids']);META.extend(s['screens']);lib=s['library']
def save():
 sfile.write_text(json.dumps({'ids':IDS,'library':lib,'screens':META},ensure_ascii=False))
 (BASE/'web/catalog.json').write_text(json.dumps({'clusters':CLUSTERS,'pages':PAGES,'families':FAM,'colors':COLORS,'dark':DARK,'products':PRODUCTS,'suppliers':SUPPLIERS,'screens':META},ensure_ascii=False))
existing={(m['cluster'],m['screen'],m['page']) for m in META}
for ci,(cl,label,fam,dims) in enumerate(CLUSTERS):
 pages=call('list_pages')['pages']; pname=f'{ci+1:02d} · '+label
 pg=next((p for p in pages if p['name']==pname),None)
 if not pg:
  call('add_page',name=pname,children=[]);pg=call('list_pages')['pages'][-1]
 pid=pg['id']
 for di,(w,h) in enumerate(dims):
  ff='wide' if w==2560 else fam;sid='4k' if cl=='tv' else str(w)
  nodes=[];metas=[]
  for pi,(slug,title) in enumerate(PAGES):
   if (cl,sid,slug) in existing:continue
   n=screen(cl,sid,ff,w,h,slug,title);n.update(x=pi*(w+120),y=di*(h+180));nodes.append(n)
   metas.append(dict(cluster=cl,screen=sid,family=ff,width=w,height=h,page=slug,title=title,pageId=pid))
  flush_masters(lib)
  for i in range(0,len(nodes),3):
   ids=insert_nodes([replace_refs(n) for n in nodes[i:i+3]],pid)
   for meta,rid in zip(metas[i:i+3],ids):meta['id']=rid;META.append(meta)
   save();print('screens',len(META),cl,sid,flush=True)
  snapshot('arasta-progress.op')
# Explicit state/component inventory, authored natively using the same master references.
for fam in FAM:
 configure(fam,320 if fam=='phone' else 1440,900)
 for style in ['ghost','tonal','outline','surface']:
  for state in ['Default','Focus','Disabled']:
   comp(f'IconButton/{fam}/{style}/{state}',frame('action:toast:Bildirimler',[icon('bell',32 if fam=='tv' else 24,'text.brand')],w=CURRENT['target'],h=CURRENT['target'],bg='bg.brand-subtle' if style=='tonal' else 'bg.surface',pad=8,cornerRadius=8,stroke={'thickness':2 if state=='Focus' else 1,'fill':solid('border.default')}))
 for kind in ['Filter','AI suggestion']:
  for state in ['Default','Selected']:comp(f'Chip/{fam}/{kind}/{state}',row([icon('check' if state=='Selected' else 'plus'),text('Organik pamuk')],pad=[8,12],bg='bg.ai-subtle' if kind.startswith('AI') else 'bg.brand-subtle',cornerRadius=8))
 for state in ['Default','Hover','Loading','Focused']:
  p=product(0);master=copy.deepcopy(MASTERS[p['ref']]);master.pop('reusable',None)
  if state=='Loading':master['children']=[frame('skeleton',[],h=170,bg='bg.muted'),text('Ürün yükleniyor…')]
  if state=='Focused':master['stroke']={'thickness':2,'fill':solid('focus.ring')}
  comp(f'ProductCardState/{fam}/{state}',master)
 for i in range(3):comp(f'EventCard/{fam}/{i}',event(i))
 comp('CommandPalette/'+fam,card([text('Hızlı erişim',28,weight=600),field('Sayfa veya işlem ara','','search'),button('Siparişler','siparis'),button('Yeni teklif','teklif-iste')],w=600))
 comp('FilterSheet/'+fam,card([text('Filtreler',28,weight=600),field('Şehir','Denizli','select'),field('Minimum sipariş','500','number'),button('Sonuçları göster',action='filter')],w=320))
 comp('CompareTray/'+fam,card([text('2 ürün seçildi',weight=600),button('Karşılaştır','karsilastirma')],w=600))
flush_masters(lib);save()
# Arrange masters inside library group wrappers. Their own coordinates stay absent,
# which is required for this native version's auto-layout instance expansion.
groups={}
for key,rid in IDS.items():groups.setdefault(key.split('/')[0],[]).append(rid)
for gi,(name,rids) in enumerate(groups.items()):
 wrapper=frame('Kütüphane / '+name,[],w=420,gap=24,pad=20,bg='bg.subtle',x=(gi%8)*500,y=(gi//8)*16000)
 wid=insert_nodes([wrapper],lib)[0]
 for i in range(0,len(rids),20):call('batch_design',operations='\n'.join('M('+json.dumps(rid)+','+json.dumps(wid)+')' for rid in rids[i:i+20]),pageId=lib)
print('complete',len(META),'screens',len(IDS),'masters',flush=True)
call('set_active_page',index='1');snapshot('arasta.op');save()
