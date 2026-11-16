struct FUN_0076b900 {
    unsigned int unk00;
    unsigned int unk04;
    unsigned int unk08;
    FUN_0076b900* next;
    FUN_0076b900(GO* owner);
};

struct Owner : GO {
    unsigned int unk00;
    unsigned int unk04;
    unsigned int unk08;
    FUN_0076b900* first;

    void FUN_00418900(Flt* value);
    void FUN_0076b6a0(Flt* value);
};

void Owner::FUN_0076b6a0(Flt* value)
{
    if (value->FUN_0076b780(0)) {
    } else {
        if (FUN_0076a3b0(0)) {
            FUN_0076b900* entry = new FUN_0076b900(this);
            entry->next = first;
            first = entry;
            FUN_00418900(value);
        } else {
            FUN_00418900(value);
        }
    }
}
