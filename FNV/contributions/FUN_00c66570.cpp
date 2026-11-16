extern __declspec(thread) int DAT_000002b4;

struct ThreadMemoryScope {
    int previous;
    ThreadMemoryScope() : previous(DAT_000002b4) {
        DAT_000002b4 = 16;
    }
    ~ThreadMemoryScope() {
        DAT_000002b4 = previous;
    }
};

struct ThreadObserver {
    virtual void onInit();
    virtual void onShutdown();
    virtual void notify(int enabled);
};

extern ThreadObserver* DAT_01268450;

void __cdecl FUN_00c66570() {
    ThreadMemoryScope scope;
    if (DAT_01268450 != 0) {
        DAT_01268450->notify(1);
    }
}