
#include <windows.h>
extern __declspec(thread) int gThreadAllocState;
struct ManagedReference {
    virtual void unused();
    virtual void destroy();
    volatile long references;
};
struct ResourceRecord {
    void* unk00;
    void* unk04;
    ManagedReference* resource;
};
struct OwnerRecord {
    void* unk00;
    void* unk04;
    void* unk08;
    void* unk0c;
    void* unk10;
    void* unk14;
    ResourceRecord* active;
};
struct ScopedThreadSetting {
    int prior;
    ScopedThreadSetting() : prior(gThreadAllocState) {
        gThreadAllocState = 16;
    }
    ~ScopedThreadSetting() { gThreadAllocState = prior; }
};
void __thiscall FUN_00ccf060_stub::FUN_00ccf060() {
    ScopedThreadSetting scope;
    if (this != 0) {
        OwnerRecord* owner = *(OwnerRecord**)((char*)this + 8);
        if (owner != 0 && owner->active != 0) {
            ManagedReference* p = owner->active->resource;
            if (p != 0 && InterlockedDecrement(&p->references) == 0)
                p->destroy();
        }
    }
}
