
/* First reconstruction by GPT-6, 2026-10-23. */
struct GraphicsResource {
    virtual void UnknownMethod();
    virtual void ReleaseSelf();
    volatile long refCount;
    void IncRefCount() { InterlockedIncrement(&refCount); }
    void DecRefCount() { if (InterlockedDecrement(&refCount) == 0) ReleaseSelf(); }
};
struct GraphicsManager {
    void FUN_00e7f430(unsigned int setting, unsigned int mode, unsigned int enabled);
};
struct RefSlot {
    GraphicsResource* m_pObject;
    RefSlot& operator=(GraphicsResource* object) {
        if (m_pObject != object) {
            if (m_pObject) m_pObject->DecRefCount();
            m_pObject = object;
            if (m_pObject) m_pObject->IncRefCount();
        }
        return *this;
    }
};
struct GraphicsSystem {
    unsigned int unk00, unk04, unk08, unk0c, unk10;
    unsigned int device14;
    unsigned int version18;
    unsigned int GetVersion() const { return version18; }
    unsigned int unk1c, unk20, unk24, unk28, unk2c;
    GraphicsManager* manager30;
    unsigned int unk34, unk38, unk3c, unk40;
    RefSlot material44;
    unsigned int unk48, unk4c, unk50, unk54, unk58;
    RefSlot material5c;
    unsigned int unk60;
    unsigned int strongCount64;
    void FUN_00e802b0(unsigned int device, unsigned int value);
    void FUN_00e80190();
};
struct TemporaryResource {
    unsigned int unk00, unk04, unk08, unk0c, unk10, unk14, unk18, unk1c;
    unsigned int unk20, unk24, unk28, unk2c, unk30, unk34, unk38, unk3c;
    unsigned int unk40, unk44, unk48, unk4c, unk50, unk54, unk58, unk5c;
    unsigned int strongCount60;
    void FUN_00e7ecd0();
    void DecRefCount() { if (--strongCount60 == 0) FUN_00e7ecd0(); }
};
struct ScopedSystem {
    GraphicsSystem* ptr;
    ScopedSystem() : ptr(0) {}
    explicit ScopedSystem(GraphicsSystem* p) : ptr(p) {
        if (ptr) ++ptr->strongCount64;
    }
    ~ScopedSystem() {
        if (ptr && --ptr->strongCount64 == 0) ptr->FUN_00e80190();
    }
    void reset(GraphicsSystem* p) {
        if (p != ptr) {
            if (ptr && --ptr->strongCount64 == 0) ptr->FUN_00e80190();
            ptr = p;
            if (ptr) ++ptr->strongCount64;
        }
    }
    void resetFromGlobal(GraphicsSystem* const& p) {
        if (ptr != p) {
            if (ptr && --ptr->strongCount64 == 0) ptr->FUN_00e80190();
            ptr = p;
            if (ptr) ++ptr->strongCount64;
        }
    }
    GraphicsSystem* operator->() const { return ptr; }
};
struct ScopedTemporary {
    TemporaryResource* ptr;
    ScopedTemporary() : ptr(0) {}
    ~ScopedTemporary() {
        if (ptr) ptr->DecRefCount();
    }
};
extern GraphicsSystem* DAT_011fe938;
extern GraphicsSystem* DAT_011fe93c;
extern GraphicsResource* DAT_011fdfb8;
extern GraphicsResource* DAT_011fdfbc;
extern GraphicsResource* DAT_011fdc6c;
extern int DAT_011fd5c0, DAT_011fc9e0, DAT_011fd5c4, DAT_011fc9e4;
extern "C" void __cdecl FUN_00e7edf0(ScopedTemporary* out);
extern "C" void __cdecl FUN_00be0cf0(TemporaryResource* res, unsigned int a, unsigned int b, unsigned int c, unsigned int d);
extern "C" GraphicsManager* __cdecl FUN_00e7f5d0();
void __cdecl FUN_00c00be0() {
    ScopedSystem current;
    ScopedTemporary temporary;
    current.reset(DAT_011fe938);
    if (current->GetVersion() < 2) {
        FUN_00e7edf0(&temporary);
        FUN_00be0cf0(temporary.ptr, 0, 1, 2, 1);
        current->FUN_00e802b0(current->device14, (unsigned int)temporary.ptr);
        FUN_00e7edf0(&temporary);
        FUN_00be0cf0(temporary.ptr, 1, 1, 2, 1);
        current->FUN_00e802b0(current->device14, (unsigned int)temporary.ptr);
    }
    current->material5c = DAT_011fdfb8;
    current->material44 = DAT_011fdc6c;
    if (!current->manager30) current->manager30 = FUN_00e7f5d0();
    current->manager30->FUN_00e7f430(0x1b, 1, 1);
    if (!current->manager30) current->manager30 = FUN_00e7f5d0();
    current->manager30->FUN_00e7f430(0x13, 5, 1);
    if (!current->manager30) current->manager30 = FUN_00e7f5d0();
    current->manager30->FUN_00e7f430(0x14, 6, 1);
    if (!current->manager30) current->manager30 = FUN_00e7f5d0();
    current->manager30->FUN_00e7f430(0xab, 1, 1);
    if (!current->manager30) current->manager30 = FUN_00e7f5d0();
    current->manager30->FUN_00e7f430(0xf, 0, 1);
    if (!current->manager30) current->manager30 = FUN_00e7f5d0();
    current->manager30->FUN_00e7f430(7, 1, 1);
    if (!current->manager30) current->manager30 = FUN_00e7f5d0();
    current->manager30->FUN_00e7f430(0x17, 3, 1);
    if (!current->manager30) current->manager30 = FUN_00e7f5d0();
    current->manager30->FUN_00e7f430(0xe, 0, 1);
    DAT_011fd5c0 = DAT_011fc9e0 = 0;
    current.resetFromGlobal(DAT_011fe93c);
    if (current->GetVersion() < 2) {
        FUN_00e7edf0(&temporary);
        FUN_00be0cf0(temporary.ptr, 0, 1, 2, 1);
        current->FUN_00e802b0(current->device14, (unsigned int)temporary.ptr);
        FUN_00e7edf0(&temporary);
        FUN_00be0cf0(temporary.ptr, 1, 1, 2, 1);
        current->FUN_00e802b0(current->device14, (unsigned int)temporary.ptr);
    }
    current->material5c = DAT_011fdfbc;
    current->material44 = DAT_011fdc6c;
    if (!current->manager30) current->manager30 = FUN_00e7f5d0();
    current->manager30->FUN_00e7f430(0x1b, 1, 1);
    if (!current->manager30) current->manager30 = FUN_00e7f5d0();
    current->manager30->FUN_00e7f430(0x13, 5, 1);
    if (!current->manager30) current->manager30 = FUN_00e7f5d0();
    current->manager30->FUN_00e7f430(0x14, 6, 1);
    if (!current->manager30) current->manager30 = FUN_00e7f5d0();
    current->manager30->FUN_00e7f430(0xab, 1, 1);
    if (!current->manager30) current->manager30 = FUN_00e7f5d0();
    current->manager30->FUN_00e7f430(0xf, 0, 1);
    if (!current->manager30) current->manager30 = FUN_00e7f5d0();
    current->manager30->FUN_00e7f430(7, 1, 1);
    if (!current->manager30) current->manager30 = FUN_00e7f5d0();
    current->manager30->FUN_00e7f430(0x17, 3, 1);
    if (!current->manager30) current->manager30 = FUN_00e7f5d0();
    current->manager30->FUN_00e7f430(0xe, 0, 1);
    DAT_011fd5c4 = DAT_011fc9e4 = 0;
}