struct Allocator
{
    virtual void slot00();
    virtual void slot04();
    virtual void Deallocate(void*, unsigned short);
};

struct Manager
{
    int unk00;
    int unk04;
    int unk08;
    int unk0c;
    Allocator* allocator;
};

extern "C" Manager* __cdecl FUN_00c85750();

struct FUN_00d0bbf0
{
    __declspec(noinline) virtual ~FUN_00d0bbf0();
    unsigned short unk04;
    unsigned short unk06;
    void* unk08;
    void* unk0c;
    int unk10;
    void* unk14;
    void* unk18;
    void* unk1c;
    void* unk20;
    void* unk24;
    void* unk28;
    void* unk2c;
    static void operator delete(void* object)
    {
        Manager* manager = FUN_00c85750();
        manager->allocator->Deallocate(object, ((FUN_00d0bbf0*)object)->unk04);
    }
};

FUN_00d0bbf0::~FUN_00d0bbf0() {}

