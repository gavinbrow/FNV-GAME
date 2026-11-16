struct TemporaryContext {
    unsigned int unk00, unk04, unk08, unk0C;
    TemporaryContext(unsigned int);
    ~TemporaryContext();
    void FUN_00438af0();
};
struct FUN_00569cb0_Class;
struct NetworkStream {
    bool FUN_0057c850(FUN_00569cb0_Class* obj, unsigned char* flag);
    void FUN_005594e0(FUN_00569cb0_Class* obj, unsigned char flag);
};
struct NodeEntry {
    bool FUN_008256d0();
    FUN_00569cb0_Class** FUN_006815c0();
    NodeEntry* FUN_00726070();
};
struct NodeCollection {
    NodeEntry* FUN_0041e500();
};
struct FUN_00569cb0_Class {
    FUN_00569cb0_Class* FUN_00569b80();
    void FUN_00569be0(unsigned char flag);
    NodeCollection* FUN_005d43c0();
    void FUN_00569cb0(unsigned char flag, NetworkStream* stream);
};
void FUN_00569cb0_Class::FUN_00569cb0(unsigned char flag, NetworkStream* stream) {
    TemporaryContext context(0x25);
    unsigned char value;
    if (!stream)
        stream = (NetworkStream*)&context;
    if (stream->FUN_0057c850(this, &value))
        return;
    stream->FUN_005594e0(this, value);
    if (FUN_00569b80()) {
        FUN_00569be0(flag);
        FUN_00569b80()->FUN_00569cb0(flag, stream);
    }
    NodeEntry* node = FUN_005d43c0()->FUN_0041e500();
    while (node != 0 && !node->FUN_008256d0()) {
        (*node->FUN_006815c0())->FUN_00569be0(flag);
        (*node->FUN_006815c0())->FUN_00569cb0(flag, stream);
        node = node->FUN_00726070();
    }
    context.FUN_00438af0();
}
