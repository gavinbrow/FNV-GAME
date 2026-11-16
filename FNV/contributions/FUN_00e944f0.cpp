extern unsigned int DAT_011c0cdc;
extern int DAT_010f0f8c;
void* __cdecl FUN_00aa13e0(unsigned int);
struct LinkedVBBlock {
    NiVBBlock block;
    void* type;
    unsigned int index;
    unsigned short a;
    unsigned short b;
    unsigned short c;
    unsigned short used;
    LinkedVBBlock* previous;
    LinkedVBBlock* next;
    void FUN_00e942d0();
    __forceinline LinkedVBBlock* Initialize() {
        a = 0;
        used = 1;
        b = 0;
        c = 0;
        index = 0;
        type = &DAT_010f0f8c;
        FUN_00e942d0();
        return this;
    }
};
extern LinkedVBBlock* DAT_0126fa30;
void __cdecl FUN_00e944f0()
{
    for (unsigned int i = 0; i < DAT_011c0cdc; ++i) {
        LinkedVBBlock* raw = static_cast<LinkedVBBlock*>(FUN_00aa13e0(sizeof(LinkedVBBlock)));
        LinkedVBBlock* p = raw ? raw->Initialize() : 0;
        LinkedVBBlock* previous = p->previous;
        LinkedVBBlock* next = p->next;
        if (previous)
            previous->next = next;
        if (next)
            next->previous = previous;
        if (DAT_0126fa30)
            DAT_0126fa30->next = p;
        p->previous = DAT_0126fa30;
        p->next = 0;
        DAT_0126fa30 = p;
    }
}