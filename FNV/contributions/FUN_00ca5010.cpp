struct Interface {
    virtual void slot00() = 0;
    virtual void slot04() = 0;
    virtual void slot08() = 0;
    virtual void slot0C() = 0;
    virtual void* GetObject() = 0;
};
typedef void (__thiscall *FinishObject)(Interface*);
struct Owner { int unk00; int unk04; Interface* unk08; void FUN_00ca5010(); };
void Owner::FUN_00ca5010() {
    if (this == 0) return;
    Interface* input = unk08;
    if (input == 0) return;
    void* raw = input->GetObject();
    if (raw == 0) return;
    char* base = (char*)raw - 0x10;
    if (base == 0) return;
    Interface* object = *(Interface**)(base + 8);
    if (object == 0) return;
    FinishObject finish = (FinishObject)(*(void***)object)[54];
    finish(object);
}

