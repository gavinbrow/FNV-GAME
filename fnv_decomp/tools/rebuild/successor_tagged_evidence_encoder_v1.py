"""Bounded tagged-tree-v1 encoder; pure source, no files or native operations.

Builds at most MAX_DOCUMENT_BYTES of output. Input is assumed already resident;
Python container/sort/bytearray overhead and decoder memory are additional.
Independent review is required before actual use.
"""
import base64
import json
import math

MAX_DOCUMENT_BYTES = 128 * 1024 * 1024
MAX_NODES = 1_000_000
MAX_DEPTH = 128
MAX_DECODED_BYTES = 128 * 1024 * 1024
CHUNK = 4096


def require(ok,message):
    if not ok:raise ValueError(message)


def encode_document(value):
    """Emit canonical V7 envelope incrementally, rejecting bounds before growth."""
    out=bytearray(); budget={'nodes':0,'bytes':0}
    def emit(chunk):
        require(type(chunk) is bytes and len(chunk)<=MAX_DOCUMENT_BYTES-len(out),'document byte cap')
        out.extend(chunk)
    def string(text):
        require(type(text) is str,'string required')
        emit(b'"')
        for offset in range(0,len(text),CHUNK):
            part=json.encoder.encode_basestring_ascii(text[offset:offset+CHUNK])[1:-1]
            emit(part.encode('ascii'))
        emit(b'"')
    def visit(node,depth):
        require(depth<=MAX_DEPTH,'tree depth exceeded')
        budget['nodes']+=1;require(budget['nodes']<=MAX_NODES,'tree node count exceeded')
        if type(node) is bytes:
            budget['bytes']+=len(node);require(budget['bytes']<=MAX_DECODED_BYTES,'decoded byte cap')
            emit(b'{"base64":"')
            for offset in range(0,len(node),CHUNK*3):emit(base64.b64encode(node[offset:offset+CHUNK*3]))
            emit(b'","type":"bytes"}');return
        if type(node) is list:
            require(len(node)<=MAX_NODES-budget['nodes'],'tree node count exceeded')
            emit(b'{"items":[')
            for index,item in enumerate(node):
                if index:emit(b',')
                visit(item,depth+1)
            emit(b'],"type":"list"}');return
        if type(node) is dict:
            require(len(node)<=MAX_NODES-budget['nodes'] and all(type(k) is str for k in node),
                    'map keys or node count differ')
            emit(b'{"items":[')
            for index,key in enumerate(sorted(node)):
                if index:emit(b',')
                emit(b'[');string(key);emit(b',');visit(node[key],depth+1);emit(b']')
            emit(b'],"type":"map"}');return
        require(node is None or type(node) in (str,int,float,bool),'unsupported output type')
        require(type(node) is not float or math.isfinite(node),'nonfinite scalar')
        emit(b'{"type":"scalar","value":')
        if type(node) is str:string(node)
        else:
            if type(node) is int:
                require(node.bit_length() <= 3*(MAX_DOCUMENT_BYTES-len(out)), 'integer exceeds output budget')
            emit(json.dumps(node,ensure_ascii=True,separators=(',',':'),allow_nan=False).encode('ascii'))
        emit(b'}')
    emit(b'{"encoding":"tagged-tree-v1","evidence":')
    visit(value,0)
    emit(b',"kind":"successor-semantic-composition-v12"}\n')
    return bytes(out)
