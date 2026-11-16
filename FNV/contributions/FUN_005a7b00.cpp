struct FUN_005a7b00_Record {
    unsigned int unk00;
    unsigned int unk04;
    unsigned int unk08;
    unsigned int unk0c;
    unsigned int unk10;
    unsigned int unk14;
    unsigned int unk18;
    unsigned int unk1c;
    unsigned int unk20;
    unsigned int m_24;
};
extern int DAT_01186490;
extern int DAT_01183028;
FUN_005a7b00_Record* __cdecl FUN_00ec43fb(unsigned int id, int unused, const int* descriptor, const int* type, int flag);
void __cdecl FUN_00401460(unsigned int* destination, unsigned int* source, int flag);
struct FUN_005a7b00_Class {
    unsigned int unk00;
    unsigned int unk04;
    unsigned int unk08;
    unsigned int unk0c;
    unsigned int unk10;
    unsigned int unk14;
    unsigned int unk18;
    unsigned int unk1c;
    unsigned int unk20;
    unsigned int m_24;
    void FUN_004851b0(unsigned int id);
    void FUN_005a7b00(unsigned int id);
};
void FUN_005a7b00_Class::FUN_005a7b00(unsigned int id)
{
    FUN_005a7b00_Record* record = FUN_00ec43fb(id, 0, &DAT_01183028, &DAT_01186490, 0);
    if (record == 0) return;
    FUN_00401460(&m_24, &record->m_24, 1);
    FUN_004851b0(id);
}