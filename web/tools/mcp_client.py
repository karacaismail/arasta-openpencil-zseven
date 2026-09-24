import json,time,urllib.request,datetime,os
from pathlib import Path
BASE=Path(os.environ.get('ARASTA_ROOT','/work/repo'))
BASE.mkdir(parents=True,exist_ok=True)
(BASE/'measurements').mkdir(exist_ok=True)
URL=os.environ.get('ARASTA_MCP','http://127.0.0.1:3100/mcp')
def call(tool_name,**args):
 b=json.dumps({'jsonrpc':'2.0','id':1,'method':'tools/call','params':{'name':tool_name,'arguments':args}},ensure_ascii=False).encode()
 t=time.perf_counter(); err=None; result=None
 try:
  req=urllib.request.Request(URL,b,{'Content-Type':'application/json'})
  with urllib.request.urlopen(req,timeout=180) as r: raw=json.load(r)
  if 'error' in raw: raise RuntimeError(str(raw['error']))
  result=raw['result']
  if result.get('isError'): raise RuntimeError(str(result))
  texts=[c['text'] for c in result.get('content',[]) if c.get('type')=='text']
  if texts:
   try: result=json.loads(texts[0])
   except ValueError: result={'text':texts[0]}
  if result.get('success') in [False,'false'] or result.get('error'): raise RuntimeError(str(result))
 except Exception as e: err=str(e)
 with (BASE/'measurements/calls.jsonl').open('a') as f:
  f.write(json.dumps({'timestamp':datetime.datetime.now(datetime.timezone.utc).isoformat(),'tool':tool_name,'transport':URL,'duration_ms':round((time.perf_counter()-t)*1000,2),'success':err is None,'error':err,'body_size':len(b)},ensure_ascii=False)+'\n')
 if err: raise RuntimeError(err)
 return result
if __name__=='__main__': print(json.dumps(call('get_document_info')))
