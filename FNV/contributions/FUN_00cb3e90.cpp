struct FUN_00d070b0_class { void FUN_00d070b0(); };
struct CleanupList {
    int unk00;
    int unk04;
    int unk08;
    int unk0c;
    int unk10;
    int unk14;
    int unk18;
    int unk1c;
    FUN_00d070b0_class* finalObject;
    int unk24;
    FUN_00d070b0_class** firstObjects;
    int firstCount;
    int unk30;
    FUN_00d070b0_class** secondObjects;
    int secondCount;
};
void __cdecl FUN_00cb3e90(CleanupList* thisPtr) {
    int i = thisPtr->firstCount - 1;
    while (i >= 0) {
        thisPtr->firstObjects[i]->FUN_00d070b0();
        --i;
    }
    i = thisPtr->secondCount - 1;
    while (i >= 0) {
        thisPtr->secondObjects[i]->FUN_00d070b0();
        --i;
    }
    thisPtr->finalObject->FUN_00d070b0();
}
