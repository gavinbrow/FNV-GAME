struct ValueHolder
{
    int unk00;
    int unk04;
    int unk08;
    int unk0C;
    int unk10;
    unsigned char value;
    unsigned char* FUN_00df8910(unsigned char* output);
};

unsigned char* ValueHolder::FUN_00df8910(unsigned char* output)
{
    *output = value;
    return output;
}

