"""Strict bounded decoder for the successor tagged-tree-v1 evidence envelope.

Pure parser; no files, native calls, admission or operation authority. It is not
integrated into a production consumer. Frozen source and tests require independent
review before use with actual evidence.
"""
import base64
import binascii
import json
import math

MAX_DOCUMENT_BYTES = 128 * 1024 * 1024
MAX_NODES = 1_000_000
MAX_DEPTH = 128
MAX_DECODED_BYTES = 128 * 1024 * 1024


def require(ok, message):
    if not ok:
        raise ValueError(message)


def _pairs(items):
    result = {}
    for key, value in items:
        require(key not in result, 'duplicate JSON object key')
        result[key] = value
    return result


def decode_document(raw):
    """Decode a single strict envelope into JSON values and immutable bytes.

    Bounds count every encoded tree node and total decoded byte payload. Parsing
    rejects duplicate JSON keys, nonfinite numbers, unknown fields, malformed
    tagged nodes and noncanonical base64. No trust or provenance is inferred.
    """
    require(type(raw) is bytes and len(raw) <= MAX_DOCUMENT_BYTES, 'bounded bytes document required')
    try:
        document = json.loads(raw.decode('utf-8'), object_pairs_hook=_pairs,
            parse_constant=lambda _: (_ for _ in ()).throw(ValueError('nonfinite JSON number')))
    except (UnicodeError, json.JSONDecodeError, RecursionError) as exc:
        raise ValueError('invalid JSON document') from exc
    require(type(document) is dict and set(document) == {'kind','encoding','evidence'} and
            document['kind'] == 'successor-semantic-composition-v12' and
            document['encoding'] == 'tagged-tree-v1', 'exact envelope required')
    budget = {'nodes': 0, 'bytes': 0}

    def visit(node, depth):
        require(depth <= MAX_DEPTH, 'tree depth exceeded')
        budget['nodes'] += 1
        require(budget['nodes'] <= MAX_NODES, 'tree node count exceeded')
        require(type(node) is dict and type(node.get('type')) is str, 'tagged node required')
        tag = node['type']
        if tag == 'bytes':
            require(set(node) == {'type','base64'} and type(node['base64']) is str, 'bytes node schema')
            encoded = node['base64']
            # Bound before allocating the decoded value.
            require(len(encoded) <= 4 * ((MAX_DECODED_BYTES - budget['bytes'] + 2) // 3), 'decoded byte cap')
            try:
                value = base64.b64decode(encoded, validate=True)
            except (ValueError, binascii.Error) as exc:
                raise ValueError('invalid base64') from exc
            require(base64.b64encode(value).decode('ascii') == encoded, 'noncanonical base64')
            budget['bytes'] += len(value)
            require(budget['bytes'] <= MAX_DECODED_BYTES, 'decoded byte cap')
            return value
        if tag == 'scalar':
            require(set(node) == {'type','value'}, 'scalar node schema')
            value = node['value']
            require(value is None or type(value) in (str,int,float,bool), 'scalar value type')
            require(type(value) is not float or math.isfinite(value), 'nonfinite scalar')
            return value
        if tag == 'list':
            require(set(node) == {'type','items'} and type(node['items']) is list, 'list node schema')
            require(len(node['items']) <= MAX_NODES - budget['nodes'], 'tree node count exceeded')
            return [visit(item, depth+1) for item in node['items']]
        if tag == 'map':
            require(set(node) == {'type','items'} and type(node['items']) is list, 'map node schema')
            require(len(node['items']) <= MAX_NODES - budget['nodes'], 'tree node count exceeded')
            result = {}
            for pair in node['items']:
                require(type(pair) is list and len(pair)==2 and type(pair[0]) is str and
                        pair[0] not in result, 'invalid or duplicate map key')
                result[pair[0]] = visit(pair[1], depth+1)
            return result
        raise ValueError('unknown node tag')

    return visit(document['evidence'], 0)
