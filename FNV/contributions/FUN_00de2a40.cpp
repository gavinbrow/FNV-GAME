struct hkBaseObject { virtual void base0() throw(); int unk04; };
struct hkProcess { virtual void process0() throw(); virtual void process1() throw(); virtual void process2() throw(); virtual void process3() throw(); virtual void process4() throw(); virtual void process5() throw(); virtual void process6() throw(); int unk04, unk08, unk0c, unk10, unk14; };
struct ContactArray { int unk00; int unk04; int unk08; int unk0c; int unk10; int unk14; int unk18; int unk1c; int unk20; int unk24; int unk28; int unk2c; int unk30; int unk34; int unk38; int unk3c; int unk40; int unk44; int unk48; int unk4c; int unk50; int unk54; int unk58; int unk5c; int unk60; int unk64; int unk68; void** data; int size; };
struct hkpPhysicsContextWorldListener { virtual void world0() throw(); virtual void world1() throw(); virtual void world2() throw(); ContactArray* contacts; void FUN_00de2980(void*) throw(); };
struct hkpWorldViewerBase : hkBaseObject, hkProcess, hkpPhysicsContextWorldListener { void FUN_00ddcc60() throw(); };
struct hkpWorldPostSimulationListener { virtual void post0() throw(); virtual void post1() throw(); virtual void post2() throw(); __forceinline ~hkpWorldPostSimulationListener() throw(); };
__forceinline hkpWorldPostSimulationListener::~hkpWorldPostSimulationListener() throw() {
    ((hkpWorldViewerBase*)((char*)this - 0x28))->FUN_00ddcc60();
}
struct hkpContactPointViewer : hkpWorldViewerBase, hkpWorldPostSimulationListener {
    __forceinline virtual ~hkpContactPointViewer() throw();
    void FUN_00de2a40() throw();
};
__forceinline hkpContactPointViewer::~hkpContactPointViewer() throw() {
    for (int i = 0; this->contacts && i < this->contacts->size; ++i)
        this->hkpPhysicsContextWorldListener::FUN_00de2980(this->contacts->data[i]);
}
void hkpContactPointViewer::FUN_00de2a40() throw() {
    this->hkpContactPointViewer::~hkpContactPointViewer();
}
