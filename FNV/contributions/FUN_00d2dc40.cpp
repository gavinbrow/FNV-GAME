struct Heap
{
    virtual void unused0();
    virtual void unused1();
    virtual void Free(void*, unsigned int);
};
struct Global
{
    unsigned int unk00, unk04, unk08, unk0c;
    Heap* heap10;
};
Global* FUN_00c85750();
struct FUN_00d2dc40
{
    int unk04;
    int unk08;
    virtual ~FUN_00d2dc40();
    static void operator delete(void* p);
};
FUN_00d2dc40::~FUN_00d2dc40()
{
}
void FUN_00d2dc40::operator delete(void* p)
{
    Global* global = FUN_00c85750();
    global->heap10->Free(p, 0xc);
}
