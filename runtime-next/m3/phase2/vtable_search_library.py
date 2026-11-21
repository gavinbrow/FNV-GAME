"""Fail-closed SEARCH_LIBRARY proof over an explicitly frozen input closure.

Metadata only. Does not perform library extraction, placement, or source edits.
Callers must supply the actual complete ordered archive and object closure from
an archived build; there is intentionally no inferred default closure.
"""
import hashlib,struct
from pathlib import Path

def sha(data):return hashlib.sha256(data).hexdigest()
def scan_coff(blob, target):
 if len(blob)<20:raise ValueError('truncated COFF')
 machine,nsec,_,_,_,optional,_=struct.unpack_from('<HHIIIHH',blob)
 if machine==0:
  if nsec!=1 or optional!=0:raise ValueError('unsupported neutral COFF')
  section=struct.unpack_from('<8sIIIIIIHHI',blob,20)
  if section[0].rstrip(b'\0')!=b'.drectve' or section[3] or section[5] or section[7]:raise ValueError('unsupported neutral COFF section')
 elif machine!=0x14c:raise ValueError('not supported COFF')
 pos,count=struct.unpack_from('<II',blob,8)
 if pos<20 or pos+18*count+4>len(blob):raise ValueError('invalid symbol table')
 st=pos+18*count;size=struct.unpack_from('<I',blob,st)[0]
 if size<4 or st+size>len(blob):raise ValueError('invalid string table')
 result=[];i=0
 while i<count:
  p=pos+18*i;raw,value,section,typ,storage,aux=struct.unpack_from('<8sIhHBB',blob,p)
  if i+aux>=count:raise ValueError('truncated auxiliary')
  if raw[:4]==b'\0'*4:
   off=struct.unpack_from('<I',raw,4)[0]
   if not 4<=off<size:raise ValueError('bad name offset')
   end=blob.find(b'\0',st+off,st+size)
   if end<0:raise ValueError('unterminated name')
   name=blob[st+off:end]
  else:name=raw.split(b'\0',1)[0]
  if name==target and storage==2 and section>0:result.append((i,section,value,typ))
  i+=1+aux
 return result

def archive_members(blob):
 if not blob.startswith(b'!<arch>\n'):raise ValueError('not archive')
 p=8
 while p<len(blob):
  if p+60>len(blob) or blob[p+58:p+60]!=b'`\n':raise ValueError('bad archive header')
  hdr=blob[p:p+60];name=hdr[:16].decode('ascii').strip()
  try:n=int(hdr[48:58])
  except ValueError:raise ValueError('bad archive length')
  start=p+60;end=start+n
  if n<0 or end>len(blob):raise ValueError('truncated archive member')
  yield name,blob[start:end]
  p=end+(n&1)
 if p!=len(blob):raise ValueError('bad archive padding')

def validate_archive_indexes(blob):
 """Cross-check both MS COFF linker indexes and physical member offsets."""
 import collections
 pos=8; members=[]; links=[]
 if not blob.startswith(b'!<arch>\n'):raise ValueError('not archive')
 while pos<len(blob):
  if pos+60>len(blob) or blob[pos+58:pos+60]!=b'`\n':raise ValueError('invalid archive header')
  h=blob[pos:pos+60]; name=h[:16].decode('ascii').strip(); n=int(h[48:58]); begin=pos+60;end=begin+n
  if end>len(blob):raise ValueError('truncated archive')
  if name=='/':links.append(blob[begin:end])
  elif name!='//':members.append(pos)
  pos=end+(n&1)
 if pos!=len(blob) or len(links)!=2:raise ValueError('missing linker indexes')
 one,two=links; n=struct.unpack_from('>I',one,0)[0];start=4+4*n
 if start>len(one):raise ValueError('short first index')
 ofs=struct.unpack_from('>%dI'%n,one,4);names=one[start:].split(b'\0')
 if len(names)!=n+1 or names[-1]!=b'':raise ValueError('invalid first index names')
 m=struct.unpack_from('<I',two,0)[0];p=4+4*m
 if p+4>len(two):raise ValueError('short second index')
 mo=struct.unpack_from('<%dI'%m,two,4); count=struct.unpack_from('<I',two,p)[0];p+=4
 if p+2*count>len(two):raise ValueError('short index entries')
 ids=struct.unpack_from('<%dH'%count,two,p);names2=two[p+2*count:].split(b'\0')
 if len(names2)!=count+1 or names2[-1]!=b'' or any(i<1 or i>m for i in ids):raise ValueError('invalid second index names')
 if set(mo)!=set(members) or len(set(mo))!=len(members):raise ValueError('index member set mismatch')
 if collections.Counter(zip(names[:-1],ofs))!=collections.Counter((name,mo[i-1]) for name,i in zip(names2[:-1],ids)):raise ValueError('linker indexes disagree')
 return {'members':m,'exported_entries':count}

def prove_absent(primary, archives, expected_archive_names, objects, expected_object_ids):
 """Return metadata iff every frozen input is checked and no strong primary exists.

 Each archive tuple is (name,path,expected_sha256), objects likewise use unit id.
 The expected lists come from independent serialized build configuration, not
 from scanning what happens to exist. Duplicate or reordered archives fail.
 """
 if not isinstance(primary,str) or not primary:raise ValueError('empty name')
 if [x[0] for x in archives]!=list(expected_archive_names) or len(set(expected_archive_names))!=len(expected_archive_names):raise ValueError('incomplete or reordered archive closure')
 if set(x[0] for x in objects)!=set(expected_object_ids) or len(objects)!=len(expected_object_ids):raise ValueError('incomplete or duplicate object closure')
 if not archives or not objects:raise ValueError('empty closure cannot prove library precedence')
 target=primary.encode('ascii');hits=[];manifest=[]
 for ident,path,digest in objects:
  raw=Path(path).read_bytes()
  if sha(raw)!=digest:raise ValueError('object digest mismatch')
  hit=scan_coff(raw,target);manifest.append(('object',ident,digest));hits.extend(('object',ident,x) for x in hit)
 for name,path,digest in archives:
  raw=Path(path).read_bytes()
  if sha(raw)!=digest:raise ValueError('archive digest mismatch')
  validate_archive_indexes(raw)
  for index,(member,blob) in enumerate(archive_members(raw)):
   if member in ('/', '//', '/SYM64/'):continue
   if blob[:2] not in (b'\x4c\x01',b'\0\0'):raise ValueError('unsupported archive member; cannot prove closure')
   hits.extend(('archive',name,index,member,x) for x in scan_coff(blob,target))
  manifest.append(('archive',name,digest))
 if hits:raise ValueError('strong primary exists: '+repr(hits))
 return {'symbol':primary,'ordered_closure':manifest,'strong_primary_count':0,'scope':'frozen supplied closure only; no placement or full linker semantics'}


