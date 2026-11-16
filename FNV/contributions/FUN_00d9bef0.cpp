struct BufferState { unsigned short* elements; unsigned int count; unsigned int capacity; };
struct AllocationContext { int unknown00, unknown04, unknown08, unknown0c; void* memory; };
void __cdecl FUN_00c90940(void* memory, BufferState* buffer, unsigned int count);
struct Owner { int unknown00, unknown04, unknown08; BufferState buffer; AllocationContext* FUN_00c85750(); unsigned short* FUN_00d9bef0(unsigned short value); };
unsigned short* Owner::FUN_00d9bef0(unsigned short value) {
    BufferState* dst = &buffer;
    AllocationContext* context = FUN_00c85750();
    if (dst->count == (dst->capacity & 0x3fffffff))
        FUN_00c90940(context->memory, dst, 2);
    unsigned short* position = dst->elements + dst->count;
    *position = value;
    ++dst->count;
    return position;
}