struct FNV_93dee0_Entry {
    unsigned int formID;
    unsigned char state;
};
struct FNV_93dee0_Node {
    FNV_93dee0_Entry** FUN_006815c0();
    FNV_93dee0_Node* FUN_00726070();
};
struct FNV_93dee0_Host : PlayerCharacter {
    unsigned char FUN_0093dee0(unsigned int formID);
};
unsigned char FNV_93dee0_Host::FUN_0093dee0(unsigned int formID) {
    FNV_93dee0_Node* node = *reinterpret_cast<FNV_93dee0_Node**>(&layoutPaddingADC[0x26c]);
    FNV_93dee0_Entry* entry = 0;
    while (node && *node->FUN_006815c0()) {
        entry = *node->FUN_006815c0();
        if (entry->formID == formID)
            return entry->state;
        node = node->FUN_00726070();
    }
    return 0;
}