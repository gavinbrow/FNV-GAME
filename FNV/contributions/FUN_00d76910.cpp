struct D76910Inner { void FUN_00d7cf00(); };
struct D76910Owner {
    int unk00;
    int unk04;
    D76910Inner* inner;
    void FUN_00d76910();
};
void D76910Owner::FUN_00d76910()
{
    inner->FUN_00d7cf00();
}
