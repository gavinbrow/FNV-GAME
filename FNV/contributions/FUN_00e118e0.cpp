struct DataBlock_00e118e0
{
    unsigned int unk00;
    unsigned int unk04;
    unsigned int unk08;
    unsigned int unk0C;
    unsigned char data;
};

struct Inputs_00e118e0
{
    unsigned int unk00;
    unsigned int unk04;
    DataBlock_00e118e0* first;
    DataBlock_00e118e0* second;
    DataBlock_00e118e0* third;
};

struct FUN_00e118e0_class
{
    void __thiscall FUN_00e11710(void*, void*, void*, void*, void*);
    void __thiscall FUN_00e118e0(const volatile Inputs_00e118e0*, void*, void*);
};

void FUN_00e118e0_class::FUN_00e118e0(
    const volatile Inputs_00e118e0* inputs, void* argument2, void* argument3)
{
    DataBlock_00e118e0* third = inputs->third;
    DataBlock_00e118e0* second = inputs->second;
    DataBlock_00e118e0* first = inputs->first;
    FUN_00e11710(&first->data, &second->data,
        &third->data, argument2, argument3);
}
