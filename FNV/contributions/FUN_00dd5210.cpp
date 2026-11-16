struct FUN_00dd5210_Interface
{
    virtual void First();
    virtual void Second();
    virtual int GetValue();
    virtual int UseValue(int value);
};

struct FUN_00dd5210_Record
{
    int value;
    int reserved;
    int unk08;
    int unk0c;
    int unk10;
};

struct FUN_00dd5210_Object
{
    int unk00;
    int unk04;
    FUN_00dd5210_Interface* unk08;
    int unk0c;
    void FUN_00dd5210(FUN_00dd5210_Record* records);
};

void FUN_00dd5210_Object::FUN_00dd5210(FUN_00dd5210_Record* records)
{
    int count = unk0c;
    int value = unk08->GetValue();
    if (count > 0)
    {
        do
        {
            records->value = value;
            records->reserved = 0;
            ++records;
            value = unk08->UseValue(value);
            --count;
        } while (count != 0);
    }
}
