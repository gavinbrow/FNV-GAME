struct ResourceHandle {
    virtual void Unused0();
    virtual void Unused1();
    virtual void Dispatch(void* object, unsigned int flags);
};
struct Completion { void FUN_008c70c0(); };
struct ContextBlock {
    unsigned int unk00;
    ResourceHandle* FUN_0044edb0();
    Completion* FUN_006815c0(int first, int second);
};
struct TaskToken {
    unsigned int value;
    TaskToken(unsigned int initialValue);
    TaskToken(const TaskToken& other);
};
struct DispatchQueue {
    virtual void Unused0();
    virtual void Unused1();
    virtual void Unused2();
    virtual void Unused3();
    virtual void Queue(ContextBlock* context, TaskToken token);
};
void FUN_00cbb990();
DispatchQueue* FUN_00cbbfc0();
struct TaskOwner {
    unsigned int unk00, unk04, unk08, unk0c;
    unsigned int unk10, unk14, unk18, unk1c;
    unsigned int unk20, unk24, unk28, unk2c;
    unsigned int unk30, unk34, unk38, unk3c;
    unsigned int unk40, unk44, unk48, unk4c;
    ContextBlock context;
    unsigned int unk54, unk58, unk5c, unk60;
    unsigned int unk64, unk68, unk6c, unk70;
    void* payload;
    void FUN_008c9e40();
};
void TaskOwner::FUN_008c9e40() {
    context.FUN_0044edb0()->Dispatch(payload, 0x16800);
    FUN_00cbb990();
    FUN_00cbbfc0()->Queue(&context, TaskToken(1));
    context.FUN_006815c0(0, 0)->FUN_008c70c0();
}