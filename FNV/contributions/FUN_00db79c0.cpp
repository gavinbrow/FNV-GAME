
extern int DAT_010cf7d4;
extern int DAT_010cf804;
extern char str_010cf830[];

struct Allocator {
    virtual void Reserved();
    virtual void* Alloc(unsigned int bytes);
};

struct Manager {
    int unk00;
    int unk04;
    int unk08;
    int unk0C;
    Allocator* heap;
};

struct SubObject {
    int unk00;
    int unk04;
    int unk08;
    int unk0C;
    void FUN_00d87790(int flags);
};

struct CreatedObject {
    void* vtable;
    unsigned short allocatedSize;
    unsigned short enabled;
    const char* typeName;
    SubObject base;

    void Init() {
        union Flag {
            unsigned char byte;
            unsigned int word;
        } flag;

        allocatedSize = 0x20;
        enabled = 1;
        flag.byte = 0;
        unsigned int arg = flag.word;

        vtable = &DAT_010cf7d4;
        typeName = str_010cf830;
        base.FUN_00d87790(arg);
        vtable = &DAT_010cf804;
    }
};

void* __cdecl FUN_00db79c0() {
    Manager* manager = (Manager*)FUN_00c85750();
    CreatedObject* object = (CreatedObject*)manager->heap->Alloc(0x20);
    object->Init();
    return object;
}
