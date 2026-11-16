struct NoteQuestList {
    unsigned int head;
    unsigned int tail;
    void __thiscall FUN_00470470();
};
struct NoteRecord {
    int unk00; int unk04; int unk08; int unk0c;
    int unk10; int unk14; int unk18; int unk1c;
    int unk20; int unk24; int unk28; int unk2c;
    int unk30; int unk34; int unk38; int unk3c;
    int unk40; int unk44; int unk48; int unk4c;
    int unk50; int unk54; int unk58; int unk5c;
    int unk60; int unk64; int unk68;
    TESDescription* noteData;
    void* speaker;
    NoteQuestList ownerQuests;
    unsigned char noteType;
    unsigned char wasRead;
    void __thiscall FUN_005e8270();
};
void NoteRecord::FUN_005e8270()
{
    ownerQuests.FUN_00470470();
    switch(noteType) {
        case 1:
            delete noteData;
            noteData = 0;
            break;
        case 2:
            delete reinterpret_cast<TESTexture*>(noteData);
            noteData = 0;
            break;
    }
}
