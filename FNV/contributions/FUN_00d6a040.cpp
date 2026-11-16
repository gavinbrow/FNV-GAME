extern const char str_0102f13c[];
extern const char DAT_010ccf7c[];
extern const char DAT_010d22a8[];
extern const char DAT_010d2288[];
extern const char DAT_010d2278[];
extern const char DAT_010d225c[];
extern const char DAT_010d224c[];
struct FUN_00ddccb0 {
    void* unk00;
    FUN_00ddccb0(void* input);
};
struct FUN_00d6a040 : FUN_00ddccb0 {
    void* unk04; void* unk08; void* unk0c; void* unk10; void* unk14;
    void* unk18; void* unk1c; void* unk20; void* unk24;
    void* volatile unk28; void* volatile unk2c;
    volatile unsigned int unk30; volatile unsigned int unk34; volatile unsigned int unk38;
    FUN_00d6a040(void* input);
};
FUN_00d6a040::FUN_00d6a040(void* input) : FUN_00ddccb0(input) {
    unk28 = (void*)str_0102f13c;
    unk2c = (void*)DAT_010ccf7c;
    unk00 = (void*)DAT_010d22a8;
    unk08 = (void*)DAT_010d2288;
    unk20 = (void*)DAT_010d2278;
    unk28 = (void*)DAT_010d225c;
    unk2c = (void*)DAT_010d224c;
    unk30 = 0;
    unk34 = 0;
    unk38 = 0x80000000u;
}