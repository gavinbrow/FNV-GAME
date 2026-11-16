struct FUN_00c99fb0_Interface
{
    virtual void Slot0();
    virtual void Slot1();
    virtual void FreeObject(void* object, unsigned int size);
    virtual void Slot3();
    virtual void FreeBuffer(void* buffer, unsigned int bytes);
};
struct FUN_00c99fb0_Manager
{
    int unk00;
    int unk04;
    int unk08;
    int unk0c;
    FUN_00c99fb0_Interface* allocator;
};
extern FUN_00c99fb0_Manager* __cdecl FUN_00c85750();
extern "C" void __stdcall DeleteCriticalSection(void* section);
struct FUN_00c99fb0
{
    virtual ~FUN_00c99fb0();
    unsigned short unk04;
    void* field08;
    int field0c;
    int field10;
    void* field14;
    static void operator delete(void* object);
};
FUN_00c99fb0::~FUN_00c99fb0()
{
    if (field14)
    {
        DeleteCriticalSection(field14);
        FUN_00c85750()->allocator->FreeObject(field14, 0x18);
    }
    int count = field10;
    FUN_00c99fb0_Manager* manager = FUN_00c85750();
    field0c = 0;
    if (count >= 0)
        manager->allocator->FreeBuffer(field08, (count & 0x3fffffff) * 4);
    field08 = 0;
    field10 = (int)0x80000000;
}
void FUN_00c99fb0::operator delete(void* object)
{
    FUN_00c99fb0* self = (FUN_00c99fb0*)object;
    FUN_00c99fb0_Manager* manager = FUN_00c85750();
    unsigned short size = self->unk04;
    manager->allocator->FreeObject(object, size);
}