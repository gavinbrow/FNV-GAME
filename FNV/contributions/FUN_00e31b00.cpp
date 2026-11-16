extern void __cdecl FUN_00e31800(int amount, struct MemWriter* writer);

struct MemWriter
{
    int used;
    char* data;
};

void __cdecl FUN_00e31b00(float value, MemWriter* writer)
{
    FUN_00e31800(4, writer);
    *(float*)(writer->data + writer->used - 4) = value;
}
