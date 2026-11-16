struct ContactSubobject {
    virtual void __fastcall method00(void*);
    virtual void __fastcall method04(void*);
    virtual void __fastcall method08(void*);
    virtual void __fastcall method0c(void*);
    virtual void __fastcall method10(void*);
    virtual void __fastcall method14(void*);
    virtual void __fastcall method18(void*);
    virtual void __fastcall method1c(void*);
    virtual void __fastcall method20(void*);
    virtual void __fastcall method24(void*);
    virtual void __fastcall method28(void*);
    virtual void __fastcall method2c(void*);
    virtual void __fastcall method30(void*);
    virtual void __fastcall method34(void*);
    virtual void __fastcall method38(void*);
    virtual void __fastcall method3c(void*);
    virtual void __fastcall method40(void*);
};
struct FUN_00cfccb0_class {
    void* m_00; void* m_04; void* m_08; void* m_0c; void* m_10;
    ContactSubobject embedded;
    void __fastcall FUN_00cfccb0(void* forwardedArg);
};
void FUN_00cfccb0_class::FUN_00cfccb0(void* forwardedArg) {
    embedded.method40(forwardedArg);
}