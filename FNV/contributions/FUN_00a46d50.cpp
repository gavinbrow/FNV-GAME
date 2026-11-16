struct FUN_00a57870_Class {
    void __thiscall FUN_00a57870();
};
struct MM {
    void __thiscall Deallocate(void*);
};
extern MM g_memoryManager;
struct NiStringsExtraData {
    void __thiscall FUN_00a7b300();
};
struct FUN_00a46d50_class {
    void __thiscall FUN_00a46d50();
};
void FUN_00a46d50_class::FUN_00a46d50() {
    *(void**)this = &DAT_0109827c;
    void* keys = *(void**)((char*)this + 0x10);
    if (keys) {
        int count = ((int*)keys)[-1];
        char* current = (char*)keys + count * 8;
        --count;
        if (count >= 0) {
            do {
                current -= 8;
                ((FUN_00a57870_Class*)current)->FUN_00a57870();
                --count;
            } while (count >= 0);
        }        g_memoryManager.Deallocate((char*)keys - 4);
    }
    ((NiStringsExtraData*)this)->FUN_00a7b300();
}

