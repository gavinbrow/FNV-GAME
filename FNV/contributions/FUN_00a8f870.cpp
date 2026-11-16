extern "C" __declspec(dllimport) long __stdcall InterlockedDecrement(volatile long*);
struct Handler {
    virtual void slot00();
    virtual void slot04();
    virtual void slot08();
    virtual void slot0c();
    virtual void slot10();
    virtual void slot14();
    virtual void slot18();
    virtual void slot1c();
    virtual void slot20();
    virtual void slot24();
    virtual void slot28();
    virtual void slot2c();
    virtual void slot30();
    virtual void slot34();
    virtual void slot38();
    virtual void slot3c();
    virtual void slot40();
    virtual void slot44();
    virtual void slot48();
    virtual void slot4c();
    virtual void run();
};
struct Registry {
    int unk00;
    unsigned count04;
    void** entries08;
    void FUN_00a8f770(void** current, char** data, Handler** next);
};
struct CallbackState {
    Handler* handler;
    void* current;
    char* data;
};
extern Registry* DAT_011f5e34;
extern char* DAT_0109b220;
void __cdecl FUN_00a8f870() {
    CallbackState state;
    Registry* registry = DAT_011f5e34;
    unsigned index = 0;
    if (index < registry->count04) {
        void** iterator = registry->entries08;
        do {
            if (*iterator != 0) {
                state.current = registry->entries08[index];
                goto found;
            }
            ++index;
            ++iterator;
        } while (index < registry->count04);
    }
    state.current = 0;
found:
    state.handler = 0;
    state.data = DAT_0109b220;
    if (state.current != 0) {
        do {
            DAT_011f5e34->FUN_00a8f770(&state.current, &state.data, &state.handler);
            if (state.handler) {
                state.handler->run();
            }
        } while (state.current != 0);
        if (state.data != DAT_0109b220) {
            InterlockedDecrement((volatile long*)(state.data - 8));
        }
    }
}
