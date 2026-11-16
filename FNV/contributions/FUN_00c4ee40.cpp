struct DispatchObject {
    virtual void __stdcall reserved0();
    virtual void __stdcall reserved1();
    virtual void __stdcall reserved2();
    virtual void __stdcall reserved3();
    virtual void __stdcall reserved4();
    virtual void __stdcall reserved5();
    virtual void __stdcall reserved6();
    virtual int __stdcall Execute(int code, int mode, int flag);
};
struct DispatchOwner {
    DispatchObject* object;
    bool __thiscall FUN_00c4ee40(int code, unsigned char enabled);
};
bool __thiscall DispatchOwner::FUN_00c4ee40(int code, unsigned char enabled) {
    int flag = 0;
    int result;
    if (enabled) flag = 1;
    result = object->Execute(code, 4, flag);
    if (result == 0) return true;
    return false;
}
