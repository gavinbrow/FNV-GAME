extern "C" void __cdecl FUN_00aa10f0(void* resource);

struct EventBase {
    virtual __forceinline ~EventBase() {
        FUN_00b601a0();
        FUN_00aa10f0(resource);
    }
    void FUN_00b601a0();
    int state;
    void* resource;
};

struct FUN_00c75ed0 : EventBase {
    ~FUN_00c75ed0();
};

FUN_00c75ed0::~FUN_00c75ed0() {
    FUN_00b601a0();
}