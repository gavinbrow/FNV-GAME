struct NiPlane_004b6100 { int a, b, c, d; };
struct NiBound { };
struct B_004b6100 { int __thiscall FUN_004b6100(NiPlane_004b6100*); };
struct S694a0;
struct NiAVObject {
    int unk04, unk08, unk0c, unk10, unk14, unk18, unk1c;
    B_004b6100* bound;
    NiBound const& __thiscall FUN_0043d450() const;    virtual void vslot0();
    virtual void vslot1();
    virtual void vslot2();
    virtual void vslot3();
    virtual void vslot4();
    virtual void vslot5();
    virtual void vslot6();
    virtual void vslot7();
    virtual void vslot8();
    virtual void vslot9();
    virtual void vslot10();
    virtual void vslot11();
    virtual void vslot12();
    virtual void vslot13();
    virtual void vslot14();
    virtual void vslot15();
    virtual void vslot16();
    virtual void vslot17();
    virtual void vslot18();
    virtual void vslot19();
    virtual void vslot20();
    virtual void vslot21();
    virtual void vslot22();
    virtual void vslot23();
    virtual void vslot24();
    virtual void vslot25();
    virtual void vslot26();
    virtual void vslot27();
    virtual void vslot28();
    virtual void vslot29();
    virtual void vslot30();
    virtual void vslot31();
    virtual void vslot32();
    virtual void vslot33();
    virtual void vslot34();
    virtual void vslot35();
    virtual void vslot36();
    virtual void vslot37();
    virtual void vslot38();
    virtual void vslot39();
    virtual void vslot40();
    virtual void vslot41();
    virtual void vslot42();
    virtual void vslot43();
    virtual void vslot44();
    virtual void vslot45();
    virtual void vslot46();
    virtual void vslot47();
    virtual void vslot48();
    virtual void vslot49();
    virtual void vslot50();
    virtual void vslot51();
    virtual void vslot52();
    virtual void callback(S694a0*);
};
struct WorkerS694a0 {
    int unk00, unk04, unk08, unk0c, unk10, unk14, unk18, unk1c, unk20, unk24, unk28;
    NiPlane_004b6100 planes[6];
    unsigned int flags;
    void __thiscall FUN_00a694e0(NiAVObject* object);
};
void WorkerS694a0::FUN_00a694e0(NiAVObject* object) {
    B_004b6100* bound = object->bound;
    if (!bound) return;
    float radius = *reinterpret_cast<float*>(reinterpret_cast<char*>(bound) + 12);
    if (radius == 0.0f) return;
    unsigned int saved = flags;
    unsigned int i = 0;
    unsigned int mask = 1;
    NiPlane_004b6100* plane = planes;
    for (; i < 6; ++i, ++plane, mask = (mask << 1) | (mask >> 31)) {
        if (flags & mask) {
            int side = reinterpret_cast<B_004b6100&>(const_cast<NiBound&>(object->FUN_0043d450())).FUN_004b6100(plane);
            if (side == 2) break;
            if (side == 1) flags &= ~mask;
        }
    }
    if (i == 6) object->callback(reinterpret_cast<S694a0*>(this));
    flags = saved;
}







