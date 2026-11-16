#include <string.h>
struct BufferInfo { char *volatile data; unsigned int length; unsigned int capacity; };
struct AllocInfo { int unk00, unk04, unk08, unk0C; void *unk10; };
extern AllocInfo *__cdecl FUN_00c85750();
extern void __cdecl FUN_00c90940(void *, BufferInfo *, int);
void __cdecl FUN_00e31850(unsigned int alignment, BufferInfo *buffer)
{
    unsigned int mask = alignment - 1;
    while (buffer->length & mask) {
        AllocInfo *alloc = FUN_00c85750();
        if (buffer->length == (buffer->capacity & 0x3fffffff))
            FUN_00c90940(alloc->unk10, buffer, 1);
        memset(buffer->data + buffer->length, 0, 1);
        ++buffer->length;
    }
}