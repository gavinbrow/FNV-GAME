#include <xmmintrin.h>
struct EntryState { unsigned int id; unsigned char active,mode; unsigned short category; };
struct __declspec(align(16)) EntryData { __m128 coordinates,rotation,metadata; };
struct FUN_00cdd2d0_Input {
 int unk00,unk04,unk08,unk0c,unk10,unk14;
 EntryState* states;
 int size;
 int unk20;
 EntryData* entries;
};
extern "C" void __cdecl FUN_00cdd2d0(FUN_00cdd2d0_Input* input, EntryData* output)
{
    int count = input->size;
    int index = 0;
    if (count <= 0) return;
    unsigned int offset = 0;
    do {
        if (input->states[index].active) {
            const __m128* value = (const __m128*)((const char*)input->entries + offset);
            __m128* destination = (__m128*)((char*)output + offset);
            *destination = *value;
        }
        ++index;
        offset += sizeof(EntryData);
    } while (index < count);
}