struct Item {
    int unk00;
    int unk04;
    float unk08;
};

struct Flag {
    bool value;
    Flag(bool v) : value(v) {}
};

Flag __cdecl FUN_00ddcda0(Item* a, Item* b)
{
    bool r;
    if (a->unk08 < b->unk08)
        r = true;
    else
        r = false;
    return Flag(r);
}
