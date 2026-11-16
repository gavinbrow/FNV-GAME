
extern char vtable_010a1024;
void* __cdecl FUN_00aa13e0(unsigned int bytes);
struct ObjBase {
    void FUN_00a5ecb0(int);
};
struct SubObject {
    void FUN_00a69940();
};
struct ChildNode {
    void FUN_0060bef0(unsigned int);
};
struct FourInts { int first; int second; int third; int fourth; };
struct NodeOwner {
    void FUN_00a5dc80(void*, void*);
    void* FUN_00a9ae00(void* arg);
};
void* NodeOwner::FUN_00a9ae00(void* arg) {
    char* memory = (char*)FUN_00aa13e0(0xcc);
    char* result;
    if (memory) {
        ((ObjBase*)memory)->FUN_00a5ecb0(0);
        *(void**)memory = &vtable_010a1024;
        ((SubObject*)(memory+0xac))->FUN_00a69940();
        ((SubObject*)(memory+0xbc))->FUN_00a69940();
        ((ChildNode*)(memory+0x9c))->FUN_0060bef0(2);
        *(unsigned short*)(memory+0xaa) = 0;
        result = memory;
    } else {
        result = 0;
    }
    FUN_00a5dc80(result, arg);
    *(FourInts*)(result+0xac) = *(FourInts*)((char*)this+0xac);
    return result;
}