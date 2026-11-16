struct FUN_00cb3ca0_object {
    int unk00;
    int unk04;
    int unk08;
    int unk0c;
    int unk10;
    int unk14;
    int unk18;
    int unk1c;
    int unk20;
    int unk24;
    int unk28;
    int unk2c;
    int unk30;
    int unk34;
    int unk38;
    int unk3c;
    int unk40;
    int unk44;
    int unk48;
    int unk4c;
    int unk50;
    int unk54;
    int unk58;
    int unk5c;
    int unk60;
    int unk64;
    int unk68;
    int unk6c;
    int unk70;
    int unk74;
    int unk78;
    int unk7c;
    int unk80;
    int unk84;
    int unk88;
    int unk8c;
    int unk90;
    int refCount94;
    int unk98;
    unsigned char flag9c;
    unsigned char unk9d;
    unsigned char unk9e;
    unsigned char unk9f;
    int unkA0;
    int unkA4;
    void __thiscall FUN_00c91120();
    void __thiscall FUN_00c91140();
};

void __cdecl FUN_00d27ac0(FUN_00cb3ca0_object* object, int* value);
void __cdecl FUN_00d00960(FUN_00cb3ca0_object* object, int* value);

int* __cdecl FUN_00cb3ca0(FUN_00cb3ca0_object* object, int* value, int shouldNotify) {
    ++object->refCount94;
    FUN_00d27ac0(object, value);
    if (shouldNotify != 0) {
        FUN_00d00960(object, value);
    }
    --object->refCount94;
    if (object->refCount94 == 0 && object->flag9c == 0) {
        if (object->unk8c != 0) {
            object->FUN_00c91120();
        }
        if (object->unkA4 == 1 && object->unk90 != 0) {
            object->FUN_00c91140();
        }
    }
    return value;
}


