struct ObjectReference { bool __thiscall FUN_00440d80(); };
struct ContainerNode {
    ContainerObject** __thiscall FUN_006815c0();
    ContainerNode* __thiscall FUN_00726070();
};
int __cdecl FUN_00ec7d40(int);
double __cdecl FUN_0048ebc0(void*, unsigned char);
struct FUN_00481e10_shell {
    ContainerNode* __thiscall FUN_00717e50();
    float __thiscall FUN_00481e10(unsigned char);
};
float __thiscall FUN_00481e10_shell::FUN_00481e10(unsigned char flag) {
    ContainerNode* node;
    float sum = 0.0f;
    node = FUN_00717e50();
    if (*node->FUN_006815c0() == 0) node = 0;
    while (node != 0) {
        ContainerObject* entry = *node->FUN_006815c0();
        node = node->FUN_00726070();
        if (reinterpret_cast<ObjectReference*>(entry->object)->FUN_00440d80()) continue;
        sum = static_cast<float>((double)FUN_00ec7d40(entry->count) * FUN_0048ebc0(entry->object, flag) + sum);
    }
    return sum;
}