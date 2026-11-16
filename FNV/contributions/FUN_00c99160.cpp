extern "C" __declspec(dllimport) void __stdcall FUN_00fdf05c(void*);
extern "C" __declspec(dllimport) void __stdcall FUN_00fdf100(void*);
struct FUN_00c99160_Dispatch {
    virtual void fn00();
    virtual void fn04();
    virtual void fn08();
    virtual void fn0c();
    virtual void fn10();
    virtual void fn14();
    virtual void fn18();
    virtual void fn1c();
    virtual void fn20();
    virtual void fn24();
    virtual void fn28();
    virtual void fn2c();
    virtual void fn30();
    virtual void fn34();
    virtual void fn38();
    virtual void fn3c(int a, int b, int c, int d, int e);
};
struct FUN_00c99160_Owner {
    int unk00;
    int unk04;
    FUN_00c99160_Dispatch** listeners;
    int listenerCount;
    int unk10;
    void* mutex;
    void FUN_00c99160(int a, int b, int c, int d, int e);
};
void FUN_00c99160_Owner::FUN_00c99160(int a, int b, int c, int d, int e) {
    FUN_00fdf05c(mutex);
    for(int i = 0; i < listenerCount; ++i) {
        listeners[i]->fn3c(a, b, c, d, e);
    }
    FUN_00fdf100(mutex);
}
