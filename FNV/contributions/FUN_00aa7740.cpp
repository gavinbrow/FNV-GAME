struct Reader
{
    virtual void Unk_00() = 0;
    virtual void Unk_04() = 0;
    virtual int Read(void* destination, unsigned int count) = 0;
};

struct FUN_00aa7740_t
{
    int FUN_00aa7740(Reader* reader, unsigned int count);
};

// @fnv 0x00aa7740
int FUN_00aa7740_t::FUN_00aa7740(Reader* reader, unsigned int)
{
    if (!reader)
    {
        return 0;
    }
    int value = 0;
    return reader->Read(&value, sizeof(value));
}
