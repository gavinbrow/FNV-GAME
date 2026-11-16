extern "C" void __cdecl FUN_00406d30(char*, unsigned int, const char*);
extern "C" void* __cdecl FUN_00afdf20(const char*, int, int, int);
struct FNVHandle {
    virtual ~FNVHandle();
    bool FUN_008905f0();
};
struct FUN_0082f240 {
    FUN_0082f240();
    virtual ~FUN_0082f240();
};
struct FUN_0044fae0 {
    FUN_0044fae0();
    ~FUN_0044fae0();
    unsigned int state00;
    unsigned int state04;
    unsigned int state08;
    unsigned int state0c;
    unsigned int state10;
    unsigned int state14;
    unsigned int state18;
    unsigned int state1c;
    unsigned int state20;
};
struct FUN_0082f010 : FUN_0082f240 {
    char path[0x104];
    FNVHandle* handle;
    FUN_0044fae0 lock;
    unsigned __int64 counter;
    FUN_0082f010(const char* pathName);
    virtual ~FUN_0082f010();
};

FUN_0082f010::FUN_0082f010(const char* pathName) {
    counter = 0;
    FUN_00406d30(path, 0x104, pathName);
    handle = (FNVHandle*)FUN_00afdf20(path, 0, 0x4000, 8);
    if (!handle || !handle->FUN_008905f0()) {
        if (handle) {
            delete handle;
        }
        handle = 0;
    }
}