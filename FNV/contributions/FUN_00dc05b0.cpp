struct AudioObject {
    int unk00; int unk04; int unk08; int unk0C;
};
struct Dc0380Layout { BSAudio* p; UnkHolder unk; int a; int b; int c; };
struct FUN_00dc05b0_writer {
    AudioObject first;
    AudioObject second;
    AudioObject third;
    int unk30;
    UnkHolder unk34;
    int unk40; int unk44; int unk48; int unk4C; int unk50; int unk54;
    Dc0380Layout audio;
    void __thiscall FUN_00dc0500(int, int);
    void __thiscall FUN_00d60940(unsigned int);
    void __thiscall FUN_00dbe790(unsigned int, unsigned int);
    void __thiscall FUN_00dbf450(int, int);
    void __thiscall FUN_00dc00b0(int);
    void __thiscall FUN_00dc0460();
};
struct CallbackTarget {
    virtual void Dummy0() {}
    virtual void Dummy1() {}
    virtual void Dummy2() {}
    virtual void Dummy3() {}
    virtual void Dummy4() {}
    virtual void Complete() {}
};
int __stdcall FUN_00dc05b0(int value, CallbackTarget* target, int source) {
    FUN_00dc05b0_writer writer;
    writer.FUN_00dc0500((int)target, source);
    writer.FUN_00d60940(0xcab00d1e);
    writer.FUN_00d60940(0xd011face);
    writer.FUN_00dbe790(1, 0);
    writer.FUN_00dbe790(0, 0);
    writer.FUN_00dbf450(value, 0);
    writer.FUN_00dc00b0(value);
    target->Complete();
    writer.FUN_00dc0460();
    return 0;
}
