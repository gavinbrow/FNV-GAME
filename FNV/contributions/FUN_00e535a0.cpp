__declspec(noinline) float FUN_00e53580_cls::FUN_00e53580(int idx)
{
    return reinterpret_cast<float*>(this)[idx];
}
float FUN_00e535a0(FUN_00e53580_cls* a, FUN_00e53580_cls* b)
{
    return a->FUN_00e53580(1) * b->FUN_00e53580(1)
         + a->FUN_00e53580(0) * b->FUN_00e53580(0)
         + a->FUN_00e53580(2) * b->FUN_00e53580(2)
         + a->FUN_00e53580(3) * b->FUN_00e53580(3);
}