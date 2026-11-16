struct RecordVector {
    float x, y, z;
    void FUN_006815c0();
};
struct RecordData {
    void FUN_00812b00(RecordVector*);
    void FUN_0066ca00(RecordVector*);
};
struct RecordValue {
    unsigned int FUN_00ca9600();
};
struct RecordFlags {
    unsigned int FUN_00621270(int mask);
};
struct SaveBuffer {
    void FUN_008579b0(const void* data, unsigned int count);
    unsigned char FUN_008df040();
};
extern SaveBuffer* DAT_011de45c;
struct SaveContext {
    void FUN_00926490(void* actor);
};
typedef RecordData* (__thiscall* GetRecordFunction)(SaveContext*);
typedef bool (__thiscall* GetStateFunction)(void*, int);
typedef bool (__thiscall* GetSwitchFunction)(void*);
void SaveContext::FUN_00926490(void* actor) {
    RecordData* record = ((GetRecordFunction)(*(void***)this)[0xa3])(this);
    if (record != 0) {
        if (!((GetStateFunction)(*(void***)actor)[0x8b])(actor, 0)) {
            unsigned int packed = ((RecordValue*)((char*)record + 0x3e0))->FUN_00ca9600();
            DAT_011de45c->FUN_008579b0(&packed, 4);
            DAT_011de45c->FUN_008579b0((char*)record + 0x520, 4);
            unsigned int flags2 = ((RecordFlags*)((char*)record + 0x410))->FUN_00621270(-1);
            DAT_011de45c->FUN_008579b0(&flags2, 4);
            if (flags2 & 0x800) {
                RecordVector position;
                position.FUN_006815c0();
                record->FUN_00812b00(&position);
                DAT_011de45c->FUN_008579b0(&position, 12);
            }
            DAT_011de45c->FUN_008579b0((char*)record + 0x4f0, 16);
            DAT_011de45c->FUN_008579b0((char*)record + 0x500, 16);
            RecordVector direction;
            direction.FUN_006815c0();
            record->FUN_0066ca00(&direction);
            DAT_011de45c->FUN_008579b0(&direction, 12);
            if (((GetSwitchFunction)(*(void***)actor)[0x40])(actor)) {
                DAT_011de45c->FUN_008579b0((char*)record + 0x540, 4);
                DAT_011de45c->FUN_008579b0((char*)record + 0x544, 4);
                DAT_011de45c->FUN_008579b0((char*)record + 0x548, 4);
            } else {
                DAT_011de45c->FUN_008579b0((char*)record + 0x54c, 4);
                DAT_011de45c->FUN_008579b0((char*)record + 0x548, 4);
            }
            if (DAT_011de45c->FUN_008df040() >= 0x77) {
                DAT_011de45c->FUN_008579b0((char*)record + 0x550, 4);
                DAT_011de45c->FUN_008579b0((char*)record + 0x558, 4);
            }
        }
    }
}
