"""Transaction wrapper pinned to independently revalidated default-build evidence."""
import argparse,hashlib,sys
from pathlib import Path
H=Path(__file__).resolve().parent;BASE=H/'rtti_tesform_bindings_transaction.py';BASE_SHA='116d9db04e79b8fe1e2e6b7bfe37635cc8050f41743476ebbca455536d04b57d';EVIDENCE_SHA='7242e851405ec30aed816f65d1c134405f229b4458ee6ec3f4a5bca4cb327c59'
if hashlib.sha256(BASE.read_bytes()).hexdigest()!=BASE_SHA:raise ValueError('reviewed transaction code changed')
sys.path.insert(0,str(H));import rtti_tesform_bindings_transaction as tx
tx.E=tx.M/'out/phase2-tesform-binding-repair-v3';tx.T=tx.M/'out/phase2-tesform-bindings-transaction-v2';tx.EVIDENCE_SHA=EVIDENCE_SHA
p=argparse.ArgumentParser();p.add_argument('action',choices=('prepare','apply','restore','recover'));a=p.parse_args();tx.prepare() if a.action=='prepare' else tx.run(a.action)
