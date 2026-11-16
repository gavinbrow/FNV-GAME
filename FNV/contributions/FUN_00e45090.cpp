struct V {
    virtual void __fastcall f0(int);
    virtual void __fastcall f1(int);
    virtual void __fastcall f2(int);
    virtual void __fastcall f3(int);
    virtual void __fastcall f4(int);
};
struct C { void __fastcall FUN_00e45090(int); };
void __fastcall C::FUN_00e45090(int x) {
    V* base = reinterpret_cast<V*>(reinterpret_cast<char*>(this)-8);
    base->f4(x);
}