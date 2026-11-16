struct FUN_00c5c400 {
    unsigned int unk00;
    unsigned int unk04;
    unsigned int unk08;
    unsigned int unk0c;
    unsigned int unk10;
    unsigned int unk14;
    unsigned int unk18;
    unsigned int unk1c;
    unsigned int unk20;
    unsigned int unk24;
    unsigned int unk28;
    unsigned int unk2c;
    unsigned int unk30;
    unsigned int unk34;
    unsigned int unk38;
    unsigned int unk3c;
    unsigned int unk40;
    unsigned int unk44;
    unsigned int unk48;
    unsigned int unk4c;
    unsigned int unk50;
    unsigned int unk54;
    unsigned int unk58;
    unsigned int m_0x5c;
    unsigned int m_0x60;
    static void* __cdecl operator new(unsigned int size);
    FUN_00c5c400();
};
struct NiPSysEmitterCtlr_CloneShell {
    void FUN_00c5cb20(FUN_00c5c400* clone, void* process);
    FUN_00c5c400* FUN_00c5ca90(void* process);
};
FUN_00c5c400* NiPSysEmitterCtlr_CloneShell::FUN_00c5ca90(void* process) {
    FUN_00c5c400* clone = new FUN_00c5c400;
    FUN_00c5cb20(clone, process);
    return clone;
}
