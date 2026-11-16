struct FUN_00759760_storage : FUN_00759760_shell {
    int unk00;
    int unk04;
    int unk08;
};
S_7597c0* __cdecl FUN_007596d0() {
    if (!DAT_011d9338)
        DAT_011d9338 = reinterpret_cast<S_7597c0*>(new FUN_00759760_storage());
    return DAT_011d9338;
}