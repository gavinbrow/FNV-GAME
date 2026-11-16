extern const char DAT_010804c8[];

struct FUN_006815c0 {
    unsigned int itemId;
    unsigned int flags;
    unsigned int next;
    FUN_006815c0();
};

struct FUN_0096a2d0 {
    unsigned int first;
    unsigned int second;
    FUN_0096a2d0();
    void FUN_007a7eb0(FUN_006815c0*, int (*callback)(unsigned short*, unsigned short*));
};

struct ReferenceMap {
    bool FUN_00863b40(unsigned char id, FUN_0096a2d0** out);
    void FUN_00863a60(unsigned char id, FUN_0096a2d0* entry);
};

struct FUN_00855a20_This {
    ReferenceMap* references;
    void FUN_00855a20(const FUN_006815c0* input);
};

void FUN_00855a20_This::FUN_00855a20(const FUN_006815c0* input)
{
    AutoMemHelper frame9(0x11, true, DAT_010804c8, 0x286);
    FUN_006815c0* record = new FUN_006815c0;
    *record = *input;
    unsigned char id8 = (unsigned char)record->flags;
    FUN_0096a2d0* bucket6;
    bool found4 = references->FUN_00863b40(id8, &bucket6);
    if (!found4) {
        bucket6 = new FUN_0096a2d0;
        references->FUN_00863a60(id8, bucket6);
    }
    bucket6->FUN_007a7eb0(record, FUN_00855b60);
}
