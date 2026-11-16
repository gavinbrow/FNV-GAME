struct FUN_0064fcd0_Other {
    virtual int v00();
    virtual int v01();
    virtual int v02();
    virtual float v03();
    unsigned int __thiscall FUN_0044edb0(int flag);
    float __thiscall FUN_005dd4e0(unsigned int index);
};

struct FUN_0064fcd0_Self {
    virtual int v00();
    virtual int v01();
    virtual int v02();
    virtual int v03();
    virtual void v04(float value);
    virtual int v05();
    virtual int v06();
    virtual int v07();
    virtual int v08();
    virtual int v09();
    virtual int v10();
    virtual int v11();
    virtual int v12();
    virtual int v13();
    virtual int v14();
    virtual int v15();
    virtual int v16();
    virtual int v17();
    virtual int v18();
    virtual int v19();
    virtual void v20(unsigned int value);
    int unk04;
    int unk08;
    int unk0c;
    unsigned int m_count;
    void __thiscall FUN_0064a4d0(unsigned int index, float value);
    FUN_0064fcd0_Self* __thiscall FUN_0064fcd0(FUN_0064fcd0_Other* other);
};

FUN_0064fcd0_Self* FUN_0064fcd0_Self::FUN_0064fcd0(FUN_0064fcd0_Other* other) {
    if (this->v01() != other->v01()) {
        return this;
    }
    this->v04(other->v03());
    this->v20(other->FUN_0044edb0(1));
    for (unsigned int i = 0; i < this->m_count; i++) {
        this->FUN_0064a4d0(i, other->FUN_005dd4e0(i));
    }
    return this;
}
