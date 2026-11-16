struct CompareValue {
    unsigned int unk00, unk04, unk08, unk0c, unk10, unk14, unk18, unk1c;
    unsigned int unk20, unk24, unk28, unk2c, unk30, unk34, unk38, unk3c;
    unsigned int unk40, unk44, unk48, unk4c, unk50, unk54, unk58, unk5c;
    unsigned int unk60, unk64, unk68, unk6c, unk70, unk74, unk78, unk7c;
    unsigned int unk80, unk84, unk88, unk8c, unk90, unk94, unk98, unk9c;
    unsigned int unkA0, unkA4, unkA8, unkAc, unkB0, unkB4, unkB8, unkBc;
    unsigned int unkC0, unkC4, unkC8, unkCc, unkD0;
    unsigned int key;
};
struct CompareReference { CompareValue* value; };
struct CompareObject {
    unsigned int unk00, unk04, unk08, unk0c, unk10, unk14, unk18, unk1c;
    unsigned int unk20, unk24, unk28, unk2c, unk30, unk34, unk38, unk3c;
    unsigned int unk40, unk44;
    CompareReference* reference;
};
void __cdecl FUN_00d02220(bool* result, CompareObject* left, CompareObject* right) {
    *result = left->reference->value->key < right->reference->value->key;
}
