struct StreamRecord {
    unsigned int unknown00;
    unsigned int bytesRead;
    int (__cdecl *read)(StreamRecord*, void*, unsigned int, unsigned int*, unsigned int);
};
struct NiStream {
    StreamRecord* record() { return *(StreamRecord**)((char*)this + 0x24c); }
    unsigned int version() { return *(unsigned int*)((char*)this + 0xd8); }
    unsigned short savedFlags() { return *(unsigned short*)((char*)this + 0x286); }
    void FUN_00a645b0();
};
void __stdcall FUN_00a57c70(NiStream*);
struct Stand840 {
    unsigned int unk00, unk04, unk08, unk0c, unk10, unk14, unk18, unk1c;
    unsigned int unk20, unk24, unk28, unk2c, unk30, unk34;
    unsigned short selected;
    void FUN_00a4b7c0(NiStream* stream);
};
void Stand840::FUN_00a4b7c0(NiStream* stream) {
    unsigned int value;
    FUN_00a57c70(stream);
    if (stream->version() < 0x0a000102) {
        selected = (stream->savedFlags() >> 5) & 0xff;
    } else {
        StreamRecord* record = stream->record();
        int (__cdecl *read)(StreamRecord*, void*, unsigned int, unsigned int*, unsigned int) = record->read;
        value = 2;
        unsigned int added = read(record, &selected, 2, &value, 1);
        record->bytesRead += added;
    }
    if (stream->version() < 0x0a010068)
        stream->FUN_00a645b0();
}
