struct Inner;
typedef void (__fastcall *Fn)(Inner*, int);

struct Inner {
    Fn* vtbl;
};

struct FUN_00dbae50_cls {
    Inner* unk00;
};

void __fastcall FUN_00dbae50(FUN_00dbae50_cls* self, int arg)
{
    Inner* p = self->unk00;
    p->vtbl[28](p, arg);
}
