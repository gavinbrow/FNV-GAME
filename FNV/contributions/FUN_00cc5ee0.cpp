struct FUN_00cc5ee0_interface
{
    virtual void __thiscall FUN_00cc5ee0_call(int value) = 0;
};

struct FUN_00cc5ee0_class
{
    void* unk00;
    void* unk04;
    void* unk08;
    void* unk0c;

    void __thiscall FUN_00cc5ee0(char param_2);
};

void __thiscall FUN_00cc5ee0_class::FUN_00cc5ee0(char param_2)
{
    if (param_2 != 0)
    {
        if (unk0c != 0)
        {
            FUN_00cc5ee0_interface* object =
                reinterpret_cast<FUN_00cc5ee0_interface*>(
                    reinterpret_cast<unsigned char*>(unk0c) - 4);

            if (object != 0)
            {
                object->FUN_00cc5ee0_call(1);
            }
        }

        unk0c = 0;
    }
}