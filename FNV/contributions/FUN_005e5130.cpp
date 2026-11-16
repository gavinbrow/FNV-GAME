
struct FUN_005e5130_Elem {
    int unk00,unk04,unk08,unk0c,unk10,unk14,unk18,unk1c;
    int unk20,unk24,unk28,unk2c,unk30,unk34,unk38,unk3c;
    int unk40,unk44,unk48,unk4c,unk50,unk54,unk58,unk5c;
    signed char flag;
    signed char unk61,unk62,unk63;
    signed char FUN_005e5190();
};
struct FUN_005e5130_Class {
    int unk00,unk04,unk08,unk0c,unk10,unk14,unk18,unk1c;
    int unk20,unk24,unk28,unk2c,unk30;
    FUN_005e5130_Elem* entries[15];
    FUN_005e5130_Elem* FUN_005e5130(int value);
};
FUN_005e5130_Elem* FUN_005e5130_Class::FUN_005e5130(int value) {
    FUN_005e5130_Elem* result = 0;
    for(int index=0;index<15;++index) {
        FUN_005e5130_Elem* current=entries[index];
        if(!current)
            continue;
        if(current->FUN_005e5190()==value) {
            result=current;
            break;
        }
    }
    return result;
}
