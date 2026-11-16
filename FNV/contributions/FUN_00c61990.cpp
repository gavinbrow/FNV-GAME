extern "C" void* DAT_012043ac;
extern "C" int DAT_0109b220;

struct S61990Obj
{
    int vt;
};

void __cdecl FUN_00c61990()
{
    S61990Obj* ptr = (S61990Obj*)DAT_012043ac;
    S61990Obj* mgr = ptr;
    S61990Obj* beta;
    volatile long* temp;
    if (mgr != 0) {
        if (mgr->vt == DAT_0109b220) {
        } else {
            temp = (volatile long*)(mgr->vt - 8);
            InterlockedDecrement(temp);
        }
        if ((1, 1) & 1) {
            g_memoryManager.Deallocate(mgr);
        }
        beta = mgr;
    } else {
        beta = 0;
    }
    DAT_012043ac = 0;
}
