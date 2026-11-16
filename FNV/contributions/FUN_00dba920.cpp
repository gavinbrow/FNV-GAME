struct FirstInterface
{
    virtual void slot0();
    virtual void slot1();
    virtual int acquire();
};
struct SecondInterface
{
    virtual void slot0(); virtual void slot1(); virtual void slot2(); virtual void slot3();
    virtual void slot4(); virtual void slot5(); virtual void slot6(); virtual void slot7();
    virtual void slot8(); virtual void slot9();
    virtual void write(int value, int* output);
    virtual int query(int value);
};
struct ResultData
{
    int unk00; int unk04; int value; int unk0c; int unk10;
};
struct Target
{
    void* object;
    int value;
    int FUN_00dba920();
};
int Target::FUN_00dba920()
{
    if (object != 0)
    {
        FirstInterface* first = (FirstInterface*)object;
        SecondInterface* second = (SecondInterface*)first->acquire();
        ResultData result;
        result.unk00 = 0;
        result.unk04 = 0;
        result.value = 0;
        result.unk0c = 0;
        result.unk10 = 0;
        int queried = second->query(value);
        second->write(queried, &result.unk00);
        return result.value;
    }
    return 0;
}
