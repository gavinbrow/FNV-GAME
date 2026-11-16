
extern "C" __declspec(dllimport) long __stdcall InterlockedDecrement(volatile long* value);

struct CallbackOwner;
struct ReleaseCallback {
    virtual void Method00();
    virtual void Method01();
    virtual void Method02();
    virtual void Method03();
    virtual void Method04();
    virtual void Method05();
    virtual void Method06();
    virtual void Method07();
    virtual void Method08();
    virtual void Method09();
    virtual void Method10();
    virtual void Method11();
    virtual void Method12();
    virtual void Method13();
    virtual void Method14();
    virtual void Method15();
    virtual void Method16();
    virtual void Method17();
    virtual void Method18();
    virtual void Method19();
    virtual void Method20();
    virtual void Method21();
    virtual void Method22();
    virtual void Method23();
    virtual void Method24();
    virtual void Method25();
    virtual void Method26();
    virtual void Method27();
    virtual void Method28();
    virtual void Method29();
    virtual void Method30();
    virtual void Method31();
    virtual void Method32();
    virtual void Method33();
    virtual void Method34();
    virtual void Method35();
    virtual void Method36();
    virtual void Method37();
    virtual void Method38();
    virtual void Method39();
    virtual void Method40();
    virtual void Method41();
    virtual void Method42();
    virtual void Method43();
    virtual void Method44();
    virtual void Method45();
    virtual void Method46();
    virtual void Method47();
    virtual void Method48();
    virtual void Method49();
    virtual void Method50();
    virtual void Method51();
    virtual void Method52();
    virtual void Method53();
    virtual void Method54();
    virtual void Method55();
    virtual void Method56();
    virtual void Method57();
    virtual void OnDetach(CallbackOwner* owner);
};

struct CallbackOwner {
    virtual void Unused();
    virtual void Release();
    volatile long referenceCount;
    void* unknown08;
    void* unknown0c;
    void* unknown10;
    void* unknown14;
    ReleaseCallback* callback;
    void DecrementReference() {
        if (InterlockedDecrement(&referenceCount) == 0) Release();
    }
};

struct ObjectReference {
    CallbackOwner* object;
    void Reset() {
        if (object) {
            object->DecrementReference();
            object = 0;
        }
    }
    ~ObjectReference() {
        if (object) object->DecrementReference();
    }
};

struct FUN_00bd6570 {
    ObjectReference owner;
    ObjectReference other;
    ObjectReference additional;
    void* unknown0c;
    void* allocation10;
    void* allocation14;
    void FUN_00bd6150();
    ~FUN_00bd6570();
};
FUN_00bd6570::~FUN_00bd6570() {
    additional.Reset();
    other.Reset();
    if (owner.object->callback)
        owner.object->callback->OnDetach(owner.object);
    owner.Reset();
    FUN_00bd6150();
    if (allocation10) {
        g_memoryManager.Deallocate(allocation10);
        allocation10 = 0;
    }
    { void* buffer = allocation14; g_memoryManager.Deallocate(buffer); }
    allocation14 = 0;
}
