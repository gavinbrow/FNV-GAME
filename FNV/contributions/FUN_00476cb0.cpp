
struct InstanceData36 {
    unsigned int values[9];
};
struct InstanceData12 {
    unsigned int values[3];
};
struct OutputRenderer {
    unsigned int FUN_008d6f30();
};
struct ChildRange;
struct CollectionItem {
    virtual void Unused0();
    virtual void Unused1();
    virtual void Unused2();
    virtual ChildRange* GetChildren();
    bool FUN_00c455a0(unsigned char);
    InstanceData36* FUN_00461130();
    InstanceData12* FUN_0045bb80();
};
struct ChildRange {
    unsigned int FUN_0043b480();
    CollectionItem* FUN_0043b4a0(unsigned int);
};
extern unsigned char DAT_01202e7c;
bool __cdecl FUN_0043b300(const void*, CollectionItem*);
void __cdecl FUN_009ac9c0(int, OutputRenderer*, OutputRenderer*, unsigned int, InstanceData12, InstanceData36);
struct ActorProcessor {
    int FUN_00476cb0(CollectionItem*, int, unsigned int, OutputRenderer*);
};
int ActorProcessor::FUN_00476cb0(CollectionItem* item, int arg, unsigned int options, OutputRenderer* output) {
    if (item == 0) return 0;
    int processed = 0;
    if (FUN_0043b300(&DAT_01202e7c, item)) {
        CollectionItem* localItem = item;
        if (localItem->FUN_00c455a0(static_cast<unsigned char>(options))) {
            FUN_009ac9c0(arg, output, output, output->FUN_008d6f30(),
                         *localItem->FUN_0045bb80(), *localItem->FUN_00461130());
            ++processed;
        }
    }
    ChildRange* children = item->GetChildren();
    if (children != 0) {
        for (unsigned int index = 0; index < children->FUN_0043b480(); ++index)
            processed += FUN_00476cb0(children->FUN_0043b4a0(index), arg, options, output);
    }
    return processed;
}
