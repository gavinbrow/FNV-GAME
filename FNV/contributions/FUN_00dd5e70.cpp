struct Sub_dd5e70 {
    virtual void v00();
    virtual void v04();
    virtual void v08();
    virtual void v0C(const char* name, void* child, int flags);
};

extern int DAT_01268940;

struct Own_dd5e70 {
    int unk00;
    int unk04;
    int unk08;
    int unk0C;
    int unk10;
    int unk14;
    void* m_sub;

    void __thiscall FUN_00c90360(Sub_dd5e70* object, const int* attribute);
    void __thiscall FUN_00dd5e70(Sub_dd5e70* object, int unused);
};

void __thiscall Own_dd5e70::FUN_00dd5e70(Sub_dd5e70* object, int unused)
{
    object->v0C("Child", m_sub, 0);
    FUN_00c90360(object, &DAT_01268940);
}
