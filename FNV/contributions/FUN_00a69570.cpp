
extern "C" __declspec(dllimport) long __stdcall InterlockedDecrement(volatile long*);
struct RefObjView {
    virtual void vslot0();
    virtual void vslot1();
    virtual void vslot2();
    virtual void vslot3();
    virtual void vslot4();
    virtual void vslot5();
    virtual void vslot6();
    virtual void vslot7();
    virtual void vslot8();
    virtual void vslot9();
    virtual void vslot10();
    virtual void vslot11();
    virtual void vslot12();
    virtual void vslot13();
    virtual void vslot14();
    virtual void vslot15();
    virtual void vslot16();
    virtual void vslot17();
    virtual void vslot18();
    virtual void vslot19();
    virtual void vslot20();
    virtual void vslot21();
    virtual void vslot22();
    virtual void vslot23();
    virtual void vslot24();
    virtual void vslot25();
    virtual void vslot26();
    virtual void vslot27();
    virtual void vslot28();
    virtual void vslot29();
    virtual void vslot30();
    virtual void vslot31();
    virtual void vslot32();
    virtual void vslot33();
    virtual void vslot34();
    virtual void vslot35(void*);
    virtual void vslot36();
    volatile long refCount;
};
struct GlobalMgr {
    int unk00,unk04;
    void* unk08;
    void __thiscall FUN_004e9bb0(void*);
};
extern GlobalMgr* DAT_011f4748;
struct RefLookup {
    RefObjView* volatile obj;
    void __thiscall FUN_0066b0d0(void*);
};
struct Handler {
    void __thiscall FUN_00a59e00(void*);
};
struct Sub694a0 : S694a0 {
    void __thiscall FUN_00a69570(void* worker,Handler* handler,void* temporary);
};
void Sub694a0::FUN_00a69570(void* worker,Handler* handler,void* temporary) {
    if (worker != 0 && handler != 0) {
        _0c=(char*)worker;
        FUN_00a694a0((char*)worker+0xdc);
        void* previous=0;
        if (temporary) {
            previous=*(void**)(_00+8);
            *(void**)(_00+8)=temporary;
        }
        RefObjView* ref=0;
        RefLookup lookup;
        lookup.obj=0;
        if (!*(void**)(_00+8)) {
            lookup.FUN_0066b0d0(DAT_011f4748->unk08);
            ref=lookup.obj;
            if(ref) ref->vslot35(worker);
        }
        handler->FUN_00a59e00(this);
        if(ref) {
            DAT_011f4748->FUN_004e9bb0(worker);
            ref->vslot36();
        }
        if (temporary) *(void**)(_00+8)=previous;
        _0c=0;
        if(ref && InterlockedDecrement(&ref->refCount)==0)
            ref->vslot1();
    }
}
