struct Param { unsigned int unk00; unsigned int unk04; unsigned int unk08; Param* next0c; };
struct This { int FUN_00df7230(Param*); int FUN_00df72e0(Param*); };
int This::FUN_00df72e0(Param* p)
{
    Param* q = p;
    q = q->next0c;
    return ((This*)((char*)this - 0xc))->FUN_00df7230(q);
}
