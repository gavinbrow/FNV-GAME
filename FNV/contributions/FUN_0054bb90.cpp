struct FormType {
    unsigned int FUN_00401170();
};

struct FUN_0054bb90_shell : TESObjectCELL {
    unsigned int FUN_0054bb90();
};

unsigned int FUN_0054bb90_shell::FUN_0054bb90()
{
    CellRefLockEnter();
    unsigned int count = 0;
    NodeStub* node = (NodeStub*)FUN_009604f0();

    while (node) {
        RefStub* reference = *node->_ref_006815c0();
        node = node->_ref_00726070();
        if (reference) {
            switch (((FormType*)reference->_FNV_GetObjectReference())->FUN_00401170()) {
            case 30:
                count++;
                break;
            }
        }
    }
    CellRefLockLeave();
    return count;
}