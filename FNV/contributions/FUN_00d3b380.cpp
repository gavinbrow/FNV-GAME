extern unsigned int DAT_010cef94;

struct FUN_00d3b380_object
{
    unsigned int* unk00;
    unsigned short unk04;
    unsigned short unk06;
    unsigned int unk08;
    unsigned short unk0c;
    unsigned short unk0e;
    unsigned short unk10;
};

struct FUN_00d3b380_allocator
{
    virtual void Unused()
    {
    }

    virtual FUN_00d3b380_object* Allocate(unsigned int size);
};

struct FUN_00d3b380_singleton
{
    int unk00;
    int unk04;
    int unk08;
    int unk0c;
    FUN_00d3b380_allocator* unk10;
};

extern "C" FUN_00d3b380_singleton* __cdecl FUN_00c85750();

void __cdecl FUN_00d3b380(int param_1, int param_2, int param_3,
                         unsigned int param_4)
{
    FUN_00d3b380_singleton* singleton = FUN_00c85750();
    FUN_00d3b380_object* object = singleton->unk10->Allocate(0x14);

    object->unk04 = 0x14;
    object->unk06 = 1;
    object->unk08 = param_4;
    object->unk00 = &DAT_010cef94;
    object->unk0c = 0xffff;
    object->unk0e = 0xffff;
    object->unk10 = 0xffff;
}