struct CBB050Array {
    void FUN_00cbadf0(unsigned int count, bool enabled);
};
struct CBB050Object {
    int unk00;
    int unk04;
    int unk08;
    CBB050Array array;
    void FUN_00a7b4a0(ReadStream* stream);
    void FUN_00cbb050(ReadStream* stream);
};
void CBB050Object::FUN_00cbb050(ReadStream* stream)
{
    FUN_00a7b4a0(stream);
    unsigned int count = 0;
    Load(*stream->binary, &count, 1);
    array.FUN_00cbadf0(count, true);
    for (unsigned int i = 0; i < count; ++i)
        stream->FUN_00a645b0();
}