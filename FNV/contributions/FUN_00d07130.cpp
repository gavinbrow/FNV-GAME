struct FUN_00d07130Arg
{
    int unk00;
    int unk04;
    int unk08;
    int unk0c;
};
struct SaveBuffer
{
    int unk00;
    int unk04;
    int unk08;
    int unk0c;
    int unk10;
    int unk14;
    int unk18;
    int unk1c;
    int unk20;
    unsigned char unk24;
    unsigned char flags;
    unsigned short unk26;
    int unk28;
    int unk2c;
    int unk30;
    int unk34;
    FUN_00d07130Arg** entries;
    int count;
    void FUN_00d07130(FUN_00d07130Arg* value);
};
void SaveBuffer::FUN_00d07130(FUN_00d07130Arg* value)
{
    int length = count;
    int index = 0;
    if (length > 0)
    {
        FUN_00d07130Arg** current = entries;
        do
        {
            if (*current == value)
                goto found;
            ++index;
            ++current;
        } while (index < length);
    }
    index = -1;
found:
    entries[index] = 0;
    value->unk0c = 0;
    flags = (flags & 0xdd) | 0x11;
}
