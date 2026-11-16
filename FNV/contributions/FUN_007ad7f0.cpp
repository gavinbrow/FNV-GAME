int __fastcall FUN_0044ddc0(void* self);
HairResult* __fastcall FUN_004ac110(void* self);
char __cdecl FUN_007ad7f0(Obj0* p)
{
    int result;
    if (p != 0 && FUN_0044ddc0(p) != 0 && DAT_011da634 != 0 && ((Holder*)DAT_011da634)->m_d8 != 0 && (int)FUN_004ac110(((Holder*)DAT_011da634)->m_d8) == FUN_0044ddc0(p))
        result = 1;
    else
        result = 0;
    return *(char*)&result;
}