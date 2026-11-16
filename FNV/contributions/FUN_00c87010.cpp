void FUN_00c876f0();
void FUN_00c87700();
void* __cdecl FUN_00aa13e0(unsigned int bytes);
extern int DAT_0102016c;
extern int DAT_0102009c;
extern int DAT_0101ffcc;

class AllocatedNode {
public:
    int* vtable;
    int unk04;
    int unk08;
    int unk0c;

    static void* operator new(unsigned int n) { return FUN_00aa13e0(n); }
    void FUN_00c87c30();

    AllocatedNode()
    {
        FUN_00c87c30();
        vtable = &DAT_0102016c;
        unk0c = 0;
        ++DAT_01268154;
        vtable = &DAT_0102009c;
        ++DAT_01268118;
        vtable = &DAT_0101ffcc;
        ++DAT_01268124;
    }
};

class FUN_00c87010_cls : public FUN_00c86800_Class
{
public:
    AllocatedNode* FUN_00c87010(FUN_00c86800_Table* p);
};

AllocatedNode* FUN_00c87010_cls::FUN_00c87010(FUN_00c86800_Table* p)
{
    ScopedAllocationMode mode;
    FUN_00c876f0();
    AllocatedNode* node = new AllocatedNode();
    FUN_00c86800((int)node, p);
    FUN_00c87700();
    return node;
}
