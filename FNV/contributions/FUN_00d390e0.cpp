struct D390Callback {
    virtual void method00();
    virtual void method04();
    virtual void method08();
    virtual void method0c();
    virtual void method10();
    virtual void method14(unsigned int key, void* context);
};

struct D390HandleTable {
    unsigned short handles[3];
    unsigned short state06;
    unsigned short state08;
    unsigned short state0a;
    unsigned short state0c;
    unsigned short state0e;
    unsigned short state10;
    unsigned short state12;
    unsigned short state14;
    unsigned short state16;
    unsigned short state18;
    unsigned short state1a;
    unsigned short state1c;
    unsigned short state1e;
    unsigned short state20;
};

unsigned short* __cdecl FUN_00d390e0(void* unused, D390HandleTable* handles, D390Callback* callback, void* context)
{
    for (int index = 0; index < 3; ++index) {
        unsigned int handle = handles->handles[index];
        if ((unsigned short)handle != 0xffff) {
            callback->method14(handle, context);
            handles->handles[index] = 0xffff;
        }
    }
    return &handles->state20;
}
