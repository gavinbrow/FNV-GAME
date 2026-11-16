struct Reader
{
    virtual void V0();
    virtual void V1();
    virtual void V2();
    virtual void V3();
    virtual void V4();
    virtual void V5();
    virtual int Read(int start, int length);
};

struct Owner
{
    unsigned char unk00[8];
    Reader* reader;
    int FUN_00d2b7b0(int start, int length);
};

int Owner::FUN_00d2b7b0(int start, int length)
{
    int done = 0;
    if (length > 0)
    {
        while (done < length)
        {
            int amount = reader->Read(start + done, length - done);
            done += amount;
            if (amount == 0)
                return done;
        }
    }
    return length;
}
