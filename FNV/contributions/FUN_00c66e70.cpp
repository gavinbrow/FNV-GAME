extern __declspec(thread) int hkThreadHeapState;

struct HavokOwner {
    virtual void release(unsigned int flag);
};

struct HavokThreadStateScope {
    int previousState;

    HavokThreadStateScope() : previousState(hkThreadHeapState) {
        hkThreadHeapState = 16;
    }

    ~HavokThreadStateScope() {
        hkThreadHeapState = previousState;
    }
};

struct FUN_00c66e70_Class {
    int unk00;
    int unk04;
    int unk08;
    char* objectData;

    void FUN_00c66e70(char destroy);
};

void FUN_00c66e70_Class::FUN_00c66e70(char destroy) {
    HavokThreadStateScope scope;
    if (destroy) {
        if (objectData) {
            HavokOwner* owner = reinterpret_cast<HavokOwner*>(objectData - 0xf0);
            if (owner)
                owner->release(1);
        }
        objectData = 0;
    }
}
