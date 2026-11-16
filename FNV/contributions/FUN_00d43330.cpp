extern float DAT_0104da48;
extern void __cdecl FUN_00d42e50(void*, void*, int, void*);

struct hkpSymmetricAgentFlipCollector
{
    virtual void unk00();
    float unk04;
    int unk08;
};

void __cdecl FUN_00d43330(void* arg1, void* arg2, int arg3, int arg4)
{
    hkpSymmetricAgentFlipCollector local;
    local.unk04 = DAT_0104da48;
    local.unk08 = arg4;
    FUN_00d42e50(arg2, arg1, arg3, &local);
}
