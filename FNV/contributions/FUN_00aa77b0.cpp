class Reader
{
public:
    virtual void Unknown00() = 0;
    virtual void Unknown04() = 0;
    virtual void Unknown08() = 0;
    virtual void Unknown0c() = 0;
    virtual void Unknown10() = 0;
    virtual void Unknown14() = 0;
    virtual void Unknown18() = 0;
    virtual void Unknown1c() = 0;
    virtual void Unknown20() = 0;
    virtual int Operation24(int value, int mode) = 0;

    int FUN_00aa77b0(int value);
};

// @fnv 0x00aa77b0
int Reader::FUN_00aa77b0(int value)
{
    return Operation24(value, 0) + 4;
}
