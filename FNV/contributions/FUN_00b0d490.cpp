struct StringRecord {
    int metadata;
    union { char* allocated; char inlineChars[16]; };
    unsigned int length, capacity;
    int extra1, extra2, extra3, extra4;
};
struct RecordVector { int metadata0,metadata4,metadata8; StringRecord *first,*last; };
void __cdecl FUN_00ec7c56();
struct FUN_00b0d490_Class {
    int unk00,unk04,unk08,unk0c,unk10,unk14,unk18,unk1c;
    int unk20,unk24,unk28,unk2c,unk30,unk34,unk38,unk3c;
    int unk40,unk44,unk48,unk4c;
    RecordVector records;
    char* FUN_00b0d490(unsigned int index);
};
char* FUN_00b0d490_Class::FUN_00b0d490(unsigned int index) {
    RecordVector* data = &records;
    if (index >= static_cast<unsigned int>(data->last - data->first)) {
        FUN_00ec7c56();
    }
    do {} while (false);
    StringRecord* entry = data->first + index;
    return entry->capacity >= 16 ? entry->allocated : entry->inlineChars;
}