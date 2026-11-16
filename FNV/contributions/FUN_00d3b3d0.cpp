struct Callback
{
    virtual void slot00();
    virtual void slot04();
    virtual void slot08();
    virtual void slot0C();
    virtual void slot10();
    virtual void invoke(unsigned short, int);
};

struct FUN_00d3b3d0_Class
{
    virtual void release(int);
    int unk04;
    Callback* unk08;
    unsigned short unk0C;
    unsigned short unk0E;
    unsigned short unk10;
    void FUN_00d3b3d0(int);
};

void FUN_00d3b3d0_Class::FUN_00d3b3d0(int value)
{
    unsigned short* id = &unk0C;
    int count = 3;
    do
    {
        unsigned short current = *id;
        if (current != 0xffff)
            unk08->invoke(current, value);
        ++id;
        --count;
    } while (count != 0);

    if (this != 0)
        release(1);
}
