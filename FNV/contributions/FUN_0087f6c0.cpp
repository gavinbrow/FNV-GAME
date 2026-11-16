#include "h_d1fadad83c84.h"
struct NameRecord {
    int FUN_0048cee0();
    const char* FUN_00408da0();
};
struct NameHeader {
    unsigned int unk00;
    unsigned int unk04;
    unsigned int unk08;
    unsigned int unk0c;
    unsigned int unk10;
    unsigned int unk14;
};
struct FullRecord : NameHeader, NameRecord {};
struct CharacterRecord {
    FullRecord* FUN_004ac110();
};
struct FUN_0087f6c0_Class : TESObjectREFR {
    CharacterRecord* FUN_007af430();
    const char* FUN_0087f6c0();
};
const char* FUN_0087f6c0_Class::FUN_0087f6c0() {
    CharacterRecord* character = 0;
    if (IsCharacter()) {
        character = FUN_007af430();
    }
    if (character) {
        NameRecord* name = character->FUN_004ac110();
        if (name && name->FUN_0048cee0() != 0) {
            return name->FUN_00408da0();
        }
    }
    return 0;
}
