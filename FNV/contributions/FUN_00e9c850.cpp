#include <string.h>
extern int DAT_011a946c; extern int DAT_011a9478; extern int DAT_011a9484; extern int DAT_011a9490; extern int DAT_011f426c;
struct TempBounds { int unk00; int unk04; int unk08; int unk0c; int unk10; int unk14; int unk18; int unk1c; int unk20; int unk24; int unk28; int unk2c; int unk30; int unk34; int unk38; void FUN_00eadf30(unsigned int code, int* point); };
struct NiPoint3 { float x; float y; float z; };
struct NiBoundingVolume { int vtable; int unk04; int unk08; int unk0c; int unk10; int unk14; int unk18; int unk1c; int unk20; int unk24; int unk28; int unk2c; int unk30; int unk34; int unk38; int unk3c; };
struct Helper { NiBoundingVolume* FUN_00ea0820(const NiPoint3&, const NiPoint3&, const NiPoint3&, const NiPoint3&, const NiPoint3&); };
NiBoundingVolume* __cdecl FUN_00e9c850(unsigned int code, int* point)
{
    if ((unsigned short)code == 0 || point == 0) return 0;
    TempBounds temp;
    temp.FUN_00eadf30(code, point);
    NiBoundingVolume* result = (NiBoundingVolume*)g_memoryManager.Allocate(0x40);
    if (result != 0)
        result = ((Helper*)result)->FUN_00ea0820(*(NiPoint3*)&DAT_011a9490, *(NiPoint3*)&DAT_011f426c, *(NiPoint3*)&DAT_011a946c, *(NiPoint3*)&DAT_011a9478, *(NiPoint3*)&DAT_011a9484);
    else
        result = 0;
    memcpy((char*)result + 4, &temp, 60);
    return result;
}



