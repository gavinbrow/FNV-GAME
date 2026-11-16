extern "C" void* __cdecl FUN_00c85750();
extern "C" void __cdecl FUN_00cd72a0(const void*, void*);

struct FUN_00d398c0_Vtable
{
    virtual void Method();
};

struct FUN_00d398c0_Allocator
{
    virtual void Method();
    virtual void* Allocate(unsigned int size);
};

struct FUN_00d398c0_Factory
{
    void* unk00;
    void* unk04;
    void* unk08;
    void* unk0c;
    FUN_00d398c0_Allocator* unk10;
};

struct FUN_00d398c0_Object
{
    void* unk00;
    unsigned short unk04;
    unsigned short unk06;
    int unk08;
    unsigned short unk0c;
    unsigned short unk0e;
    unsigned short unk10;
    unsigned short unk12;
    char unk14;
    char unk15;
    char unk16;
    char unk17;
    char unk18;
    char unk19;
    char unk1a;
    char unk1b;
    char unk1c;
    char unk1d;
    char unk1e;
    char unk1f;
    char unk20;
    char unk21;
    char unk22;
    char unk23;
    char unk24;
    char unk25;
    char unk26;
    char unk27;
};

extern FUN_00d398c0_Vtable DAT_010ceefc;

extern "C" void* __cdecl FUN_00d398c0(
    int param_1,
    int* param_2,
    int param_3,
    int param_4)
{
    FUN_00d398c0_Factory* factory =
        reinterpret_cast<FUN_00d398c0_Factory*>(FUN_00c85750());

    FUN_00d398c0_Object* object =
        reinterpret_cast<FUN_00d398c0_Object*>(
            factory->unk10->Allocate(0x28));

    object->unk00 = reinterpret_cast<void*>(&DAT_010ceefc);
    object->unk04 = 0x28;
    object->unk06 = 1;
    object->unk08 = param_4;
    object->unk0c = 0xffff;
    object->unk0e = 0xffff;
    object->unk10 = 0xffff;

    FUN_00cd72a0(
        reinterpret_cast<const void*>(
            static_cast<unsigned int>(*reinterpret_cast<int*>(param_2)) + 0x20),
        reinterpret_cast<void*>(&object->unk14));

    return object;
}