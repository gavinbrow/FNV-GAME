struct FUN_006eec00_Entry {
    unsigned int unk00;
    unsigned int unk04;
    unsigned int unk08;
    unsigned int unk0c;
    unsigned int unk10;
    unsigned int unk14;
    unsigned int index;
};
struct FUN_006eec00_Array {
    void FUN_006f23d0(unsigned int index, void*& value);
    unsigned int FUN_0044ddc0();
    FUN_006eec00_Entry** FUN_00877a30(unsigned int index);
};
struct FUN_006eec00_Class {
    void FUN_006eec00(unsigned int index, void* value, unsigned char usePrimary);
};
void FUN_006eec00_Class::FUN_006eec00(unsigned int index, void* value, unsigned char usePrimary) {
    if (usePrimary) {
        reinterpret_cast<FUN_006eec00_Array*>(reinterpret_cast<char*>(this) + 0x68)->FUN_006f23d0(index, value);
        for (unsigned int i = index; i < reinterpret_cast<FUN_006eec00_Array*>(reinterpret_cast<char*>(this) + 0x68)->FUN_0044ddc0(); ++i) {
            (*reinterpret_cast<FUN_006eec00_Array*>(reinterpret_cast<char*>(this) + 0x68)->FUN_00877a30(i))->index = i;
        }
    } else {
        reinterpret_cast<FUN_006eec00_Array*>(reinterpret_cast<char*>(this) + 0x7c)->FUN_006f23d0(index, value);
        for (unsigned int j = index; j < reinterpret_cast<FUN_006eec00_Array*>(reinterpret_cast<char*>(this) + 0x7c)->FUN_0044ddc0(); ++j) {
            (*reinterpret_cast<FUN_006eec00_Array*>(reinterpret_cast<char*>(this) + 0x7c)->FUN_00877a30(j))->index = j;
        }
    }
}