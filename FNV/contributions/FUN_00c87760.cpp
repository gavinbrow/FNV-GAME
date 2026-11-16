struct ObjectController {
    virtual void v00();
    virtual void v01();
    virtual void v02();
    virtual void v03();
    virtual void v04();
    virtual void v05();
    virtual void v06();
    virtual void v07();
    virtual void v08();
    virtual void v09();
    virtual void v0a();
    virtual void v0b();
    virtual void v0c();
    virtual void v0d();
    virtual void v0e();
    virtual void v0f();
    virtual void v10();
    virtual void v11();
    virtual void v12();
    virtual void v13();
    virtual void v14();
    virtual void v15();
    virtual void v16();
    virtual void v17();
    virtual void v18();
    virtual void v19();
    virtual void v1a();
    virtual void v1b();
    virtual void v1c();
    virtual void v1d();
    virtual void v1e();
    virtual void v1f();
    virtual void v20();
    virtual void v21();
    virtual void v22();
    virtual void v23();
    virtual void v24();
    virtual void* v25();
    virtual void v26();
    virtual void v27();
    virtual void v28();

    void* unk04;
    void* m_pObject;
    void FUN_00c87760(void* replacement);
    void FUN_00c87c50(void* replacement);
};

void ObjectController::FUN_00c87760(void* replacement)
{
    void* current = this ? m_pObject : 0;
    if (replacement != current) {
        if (current) {
            void* state = v25();
            if (state && *reinterpret_cast<int*>(static_cast<char*>(state) + 0x350))
                v28();
        }
        FUN_00c87c50(replacement);
    }
}
