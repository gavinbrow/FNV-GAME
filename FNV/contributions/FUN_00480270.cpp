struct PacketReadResult {
    bool FUN_004280f0();
};

struct PacketStream {
    PacketReadResult* FUN_00428110(void* destination, unsigned int size);
    void FUN_00865e50(void* destination, unsigned int kind, unsigned int flags);
};

struct FUN_00480270_shell {
    unsigned int unk00;
    unsigned int unk04;
    void FUN_00480270(PacketStream* stream);
};

void FUN_00480270_shell::FUN_00480270(PacketStream* stream)
{
    unsigned int value;
    if (stream->FUN_00428110(&value, 4)->FUN_004280f0()) {
        stream->FUN_00865e50(&unk04, 7, 0);
    }
}
