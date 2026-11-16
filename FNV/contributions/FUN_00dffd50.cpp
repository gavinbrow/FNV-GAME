struct Record;
struct Manager
{
    virtual void unk00();
    virtual void unk04();
    virtual void Notify(Record* record, unsigned short value);
};
struct Holder
{
    int unk00;
    int unk04;
    int unk08;
    int unk0c;
    Manager* manager;
};
Holder* FUN_00c85750();
struct Record
{
    int unk00;
    unsigned short value;
    void FUN_00dffca0();
    Record* FUN_00dffd50(unsigned int flags);
};
Record* Record::FUN_00dffd50(unsigned int flags)
{
    FUN_00dffca0();
    if (flags & 1)
    {
        Holder* holder = FUN_00c85750();
        holder->manager->Notify(this, value);
    }
    return this;
}


