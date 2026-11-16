struct Mesh308Compat {
    virtual void __thiscall a00(); virtual void __thiscall a01();
    virtual void __thiscall a02(); virtual void __thiscall a03();
    virtual void __thiscall a04(); virtual void __thiscall a05();
    virtual void __thiscall a06(); virtual void __thiscall a07();
    virtual void __thiscall a08(); virtual void __thiscall a09();
    virtual void __thiscall a10(); virtual void __thiscall a11();
    virtual void __thiscall a12(); virtual void __thiscall a13();
    virtual void __thiscall a14(); virtual void __thiscall a15();
    virtual void __thiscall a16(); virtual void __thiscall a17();
    virtual void __thiscall a18(); virtual void __thiscall a19();
    virtual void __thiscall a20(); virtual void __thiscall a21();
    virtual void __thiscall a22();
    virtual char __thiscall a23(Mesh308*);
};
struct DerivedThis308 : This308 {
    char __thiscall FUN_00c24de0(This308*);
    char __thiscall FUN_00c30970(This308*);
};
char __thiscall DerivedThis308::FUN_00c30970(This308* other) {
    if (!FUN_00c24de0(other))
        return 0;
    Mesh308Compat* thisMesh = reinterpret_cast<Mesh308Compat*>(m7c);
    Mesh308* otherMesh = other->m7c;
    return thisMesh->a23(otherMesh) != 0;
}
