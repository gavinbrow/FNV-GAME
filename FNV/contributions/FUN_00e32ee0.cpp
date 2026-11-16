struct FnvAnimation
{
    virtual void slot00();
    virtual void slot04();
    virtual void slot08();
    virtual void slot0C();
    virtual int slot10(float time, int blockOffset, int parameterA, int blockEnd, int parameterB, int parameterC);

    int unk04;
    int unk08;
    int unk0C;
    int blockOffset;
    int blockEnd;

    int FUN_00e32ee0(float time, int parameterA, int parameterB, int parameterC);
};

int FnvAnimation::FUN_00e32ee0(float time, int parameterA, int parameterB, int parameterC)
{
    return slot10(time, blockOffset, parameterA, blockEnd, parameterB, parameterC);
}