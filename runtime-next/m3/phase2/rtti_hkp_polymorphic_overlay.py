"""Private hkp RTTI hypothesis: make hkBaseObject polymorphic via destructor."""
import hashlib,json
from pathlib import Path
H=Path(__file__).resolve().parent;M=H.parent;BASE=M/'out/phase2-hkp-postsim-v3';OUT=M/'out/phase2-hkp-polymorphic-v4';BASE_SHA='e0b06d67aaab1599b1733efaab71388958619576702abb238cdc665cf6c4f385'


def transform(data):
 old=b'class hkBaseObject\r\n{\r\n};';new=b'class hkBaseObject\r\n{\r\n  public:\r\n    virtual ~hkBaseObject();\r\n};'
 if data.count(old)!=1:raise ValueError('base anchor changed or ambiguous')
 return data.replace(old,new,1)


def main():
 m=json.loads((BASE/'manifest.json').read_text());data=(BASE/'hkpconstraintviewer.cpp').read_bytes()
 if hashlib.sha256(data).hexdigest()!=BASE_SHA or m['new_overlay_sha256']!=BASE_SHA:raise ValueError('prior overlay changed')
 result=transform(data);OUT.mkdir(parents=False,exist_ok=False)
 with (OUT/'hkpconstraintviewer.cpp').open('xb') as f:f.write(result)
 meta=dict(m);meta.update(scope='private polymorphic hkBaseObject and post-simulation hypothesis, not ABI or identity proof',prior_overlay_sha256=BASE_SHA,new_overlay_sha256=hashlib.sha256(result).hexdigest(),
  hypothesis='polymorphic hkBaseObject at offset zero; project generated hkBase.h declares virtual destructor; related surrogate disagrees',
  status='uncompiled; mapped constructor, destructor, all graph/vtable/ODR gates remain required')
 with (OUT/'manifest.json').open('x',encoding='utf8') as f:json.dump(meta,f,indent=2)
 print(json.dumps({'overlay_sha256':meta['new_overlay_sha256'],'status':meta['status']}))

if __name__=='__main__':main()
