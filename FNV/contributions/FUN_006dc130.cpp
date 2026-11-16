void* __cdecl operator new(unsigned int size, void* where);
void __cdecl operator delete(void* allocated, void* where);

struct PlacementObject32 : FUN_006d4550_Class {
    unsigned int unk00;
    unsigned int unk04;
    unsigned int unk08;
    unsigned int unk0C;
    unsigned int unk10;
    unsigned int unk14;
    unsigned int unk18;
    unsigned int unk1C;
};

void FUN_006dc1d0_Class::FUN_006dc130(int base, unsigned int count)
{
    for (unsigned int index = 0; index < count; ++index) {
        new ((void*)(base + index * 32)) PlacementObject32;
    }
}
