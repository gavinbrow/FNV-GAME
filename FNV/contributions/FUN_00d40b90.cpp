struct FNVTypeRecord { int unknown0; int unknown4; int unknown8; int type; };
struct FNVObject { FNVTypeRecord* record; };
struct FNVPair { FNVObject* first; FNVObject* second; };
struct FNVFlags { int unknown0; int unknown4; short unknown8; unsigned char unknownA; unsigned char flags; };
extern "C" int __cdecl FUN_00d418d0(FNVPair*, int, FNVFlags*);
int __cdecl FUN_00d40b90(FNVPair* pair, int mode, FNVFlags* result)
{
    int converted = FUN_00d418d0(pair, mode, result);
    result->flags &= 0xF0;
    if (pair->first->record->type == 2) {
        result->flags |= 5;
    }
    if (pair->second->record->type == 2) {
        result->flags |= 10;
    }
    return converted;
}