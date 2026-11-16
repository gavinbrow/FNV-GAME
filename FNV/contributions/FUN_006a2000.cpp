void* __cdecl operator new(unsigned int size, void* placement);
struct FUN_006a14b0 {
    unsigned int unk00;
    unsigned int unk04;
    unsigned int unk08;
    unsigned int unk0c;
    FUN_006a14b0();
};
struct Proc006a20 { void FUN_006a2000(int base, int count); };
void Proc006a20::FUN_006a2000(int base, int count)
{
    for (unsigned int index = 0; index < (unsigned int)count; ++index) {
        new (reinterpret_cast<char*>(base) + index * 16) FUN_006a14b0;
    }
}