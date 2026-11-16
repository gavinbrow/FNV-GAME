extern "C" __declspec(thread) unsigned int g_tlsMode;
struct ThreadModeGuard {
    unsigned int previous;
    ThreadModeGuard() : previous(g_tlsMode) { g_tlsMode = 16; }
    ~ThreadModeGuard() { g_tlsMode = previous; }
};
struct OutputBuffer {
    void* unk00; void* unk04; void* unk08;
    struct ListStorage { void __thiscall FUN_00cc1b40(unsigned int count); } list;
    void __thiscall FUN_00cc2080(void* value);
};
struct SceneNode {
    virtual void unknown_slot_00();
    virtual void unknown_slot_04();
    virtual void unknown_slot_08();
    virtual void unknown_slot_0c();
    virtual void unknown_slot_10();
    virtual void unknown_slot_14();
    virtual void unknown_slot_18();
    virtual void unknown_slot_1c();
    virtual void unknown_slot_20();
    virtual void unknown_slot_24();
    virtual void unknown_slot_28();
    virtual void unknown_slot_2c();
    virtual void unknown_slot_30();
    virtual void unknown_slot_34();
    virtual void unknown_slot_38();
    virtual void unknown_slot_3c();
    virtual void unknown_slot_40();
    virtual void unknown_slot_44();
    virtual void* ReadValue(void* context);
};
struct SceneList {
    void* unk00; void* unk04; void* unk08; void* unk0c;
    SceneNode** entries;
    void* unk14; void* unk18;
    unsigned int count;
    void __thiscall FUN_00a7b330(OutputBuffer* dest, void* context);
    void __thiscall FUN_00cc2120(OutputBuffer* dest, void* context);
};
void __thiscall SceneList::FUN_00cc2120(OutputBuffer* dest, void* context) {
    ThreadModeGuard mode;
    FUN_00a7b330(dest, context);
    unsigned int n = count;
    dest->list.FUN_00cc1b40(n);
    for (unsigned int i = 0; i < n; ++i) {
        SceneNode* node = entries[i];
        void* value = node;
        if (node) value = node->ReadValue(context);
        dest->FUN_00cc2080(value);
    }
}