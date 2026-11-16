struct MemoryManager {
    void* __thiscall FUN_00aa3e40(unsigned int);
};
extern MemoryManager DAT_011f6238;
extern char DAT_01400000;
struct Buffer {
    unsigned int unk00;
    const char* unk04;
    unsigned int unk08, unk0c, unk10, unk14, unk18, unk1c;
    unsigned int unk20, unk24, unk28, unk2c, unk30, unk34, unk38, unk3c;
    unsigned int unk40, unk44, unk48, unk4c, unk50;
    Buffer* __thiscall FUN_00e947c0();
};
struct Destination {
    unsigned int unk00, unk04, unk08, unk0c, unk10, unk14;
    unsigned short index18, unk1a;
    Buffer* buffer1c;
};
struct FUN_00e95500_Class {
    void __thiscall FUN_00e98730(Buffer*);
    void __thiscall FUN_00e95500(Destination*);
};
void FUN_00e95500_Class::FUN_00e95500(Destination* destination) {
    if (destination->buffer1c == 0) {
        Buffer* ptr = static_cast<Buffer*>(DAT_011f6238.FUN_00aa3e40(0x54));
        Buffer* newBuffer = ptr ? ptr->FUN_00e947c0() : 0;
        newBuffer->unk3c = 4;
        destination->buffer1c = newBuffer;
        newBuffer->unk04 = &DAT_01400000;
        FUN_00e98730(newBuffer);
        destination->index18 = 0xffff;
    }
}