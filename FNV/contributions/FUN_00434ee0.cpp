extern char DAT_01183b2c;
extern char DAT_01184058;

struct LinkedNode;
struct ValueArg { int value; };
struct LinkedNode {
    int* GetItem();
    bool IsEmpty();
    LinkedNode* GetNext();
};

struct ResultContainer {
    void* pOwner;
    void* pFirst;
    void* pLast;
    LinkedNode entries;
};

extern "C" ResultContainer* __cdecl func_0x00ec43fb(int, int, void*, void*, int);
extern "C" void __fastcall FUN_00434fa0(void*);
extern "C" void __fastcall FUN_00434f60(void*, ValueArg);
extern "C" bool __fastcall FUN_008256d0(LinkedNode*);
extern "C" ValueArg* __fastcall FUN_006815c0(LinkedNode*);
extern "C" LinkedNode* __fastcall FUN_00726070(LinkedNode*);

struct FUN_00434ee0_Class {
    void FUN_00434ee0(int);
};

void FUN_00434ee0_Class::FUN_00434ee0(int id)
{
    ResultContainer* container = func_0x00ec43fb(id, 0, &DAT_01183b2c, &DAT_01184058, 0);
    if (container == 0)
        return;

    FUN_00434fa0(this);
    LinkedNode* node = &container->entries;
    while (node != 0 && !FUN_008256d0(node)) {
        FUN_00434f60(this, *FUN_006815c0(node));
        node = FUN_00726070(node);
    }
}