struct IndexedRecord {
    unsigned int unk00;
    unsigned int unk04;
    unsigned int unk08;
    unsigned int unk0c;
    unsigned int unk10;
    unsigned int unk14;
    unsigned int unk18;
    unsigned int unk1c;
    unsigned int unk20;
    unsigned int unk24;
    unsigned int unk28;
    unsigned int unk2c;
    unsigned int unk30;
    unsigned int unk34;
    unsigned int unk38;
    unsigned int unk3c;
    unsigned int unk40;
    unsigned int unk44;
    unsigned int unk48;
};
struct IndexCollection {
    void __thiscall FUN_006f23d0(unsigned int first, unsigned int* last);
    unsigned int __thiscall FUN_0044ddc0();
    IndexedRecord** __thiscall FUN_00877a30(unsigned int index);
};
struct FUN_006eecc0_Owner {
    void __thiscall FUN_006eecc0(unsigned int first, unsigned int last);
};
void __thiscall FUN_006eecc0_Owner::FUN_006eecc0(unsigned int first, unsigned int last) {
    reinterpret_cast<IndexCollection*>(reinterpret_cast<char*>(this) + 0x90)->FUN_006f23d0(first, &last);
    for (unsigned int index = first;
         index < reinterpret_cast<IndexCollection*>(reinterpret_cast<char*>(this) + 0x90)->FUN_0044ddc0();
         ++index) {
        (*reinterpret_cast<IndexCollection*>(reinterpret_cast<char*>(this) + 0x90)->FUN_00877a30(index))->unk48 = index;
    }
}