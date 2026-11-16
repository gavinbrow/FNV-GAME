struct FUN_00cb7790_node
{
    unsigned int unk00;
    unsigned int unk04;
    unsigned int unk08;
    unsigned int unk0C;
    unsigned int unk10;
    unsigned int unk14;
    unsigned int unk18;
    unsigned int unk1C;
    unsigned int unk20;
    unsigned int unk24;
    unsigned int unk28;
    unsigned int unk2C;
    unsigned int unk30;
    unsigned int unk34;
    unsigned int unk38;
    unsigned int unk3C;
    unsigned int unk40;
    unsigned int unk44;
    unsigned int unk48;
    unsigned int unk4C;
    unsigned int unk50;
    unsigned int unk54;
    unsigned int unk58;
    unsigned int unk5C;
    unsigned int unk60;
    unsigned int unk64;
    Buf00cb7750 transform;
    void __thiscall FUN_00a68bf0();
};

struct FUN_00cb7790_receiver
{
    unsigned int unk00;
    unsigned int unk04;
    void* object;
    void __thiscall FUN_0056df20(Buf00cb7750*);
};

struct FUN_00cb7790_state
{
    unsigned int owner;
    unsigned int depth;
    void __thiscall FUN_0040fbf0(int);
};
extern FUN_00cb7790_state DAT_01267b80;

struct FUN_00cb7790_class
{
    unsigned int unk00;
    unsigned int unk04;
    FUN_00cb7790_node* node;
    unsigned int unk0C;
    FUN_00cb7790_receiver* receiver;
    void __thiscall FUN_00cb7790();
};

void FUN_00cb7790_class::FUN_00cb7790()
{
    FUN_00cb7790_receiver* target = receiver;
    FUN_00cb7790_node* source = node;
    if (source)
    {
        source->FUN_00a68bf0();
        if (target && target->object)
        {
            Buf00cb7750 transform = source->transform;
            DAT_01267b80.FUN_0040fbf0(0);
            target->FUN_0056df20(&transform);
            if (--DAT_01267b80.depth == 0)
                DAT_01267b80.owner = 0;
        }
    }
}
