struct hkBaseObject { virtual void BaseV() = 0; };
struct hkReferencedObject : hkBaseObject { unsigned short unk04; unsigned short unk06; hkReferencedObject(); };
hkReferencedObject::hkReferencedObject() : unk06(1) {}
struct hkpWorldPostSimulationListener { virtual void ListenerMethod() = 0; };
struct FUN_00d9e860 : hkReferencedObject, hkpWorldPostSimulationListener {
    volatile int unk0C; volatile unsigned char unk10; volatile int unk14; volatile int unk18;
    volatile int unk1C; volatile int unk20; volatile int unk24; volatile int unk28; volatile int unk2C; volatile int unk30; volatile int unk34;
    virtual ~FUN_00d9e860() = 0;
    FUN_00d9e860();
};
FUN_00d9e860::FUN_00d9e860() {
    unk0C = 0; unk10 = 0; unk14 = 0; unk18 = 0;
    unk1C = (int)0x80000000; unk20 = 0; unk24 = 0; unk28 = (int)0x80000000;
    unk2C = 0; unk30 = 0; unk34 = (int)0x80000000;
}

