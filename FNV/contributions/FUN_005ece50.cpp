int __cdecl FUN_00408b20(const char*, const char*);
struct NavMeshStaticAvoidNode : FUN_005ecd10_cls {};
struct NodeArray : BSSimpleArray<NavMeshStaticAvoidNode*, 1024> {
    NavMeshStaticAvoidNode* FUN_00691750(int index);
};
struct FUN_005ece50_class {
    unsigned char m0;
    BSSimpleArray<const char*, 1024> m4;
    NodeArray m14;
    unsigned char FUN_005ece50(FUN_005ece50_class* other);
};
unsigned char FUN_005ece50_class::FUN_005ece50(FUN_005ece50_class* other)
{
    unsigned char bStack_5 = 0;
    unsigned int uStack_18;
    {
        unsigned int uStack_c;
        if (m14.GetSize() != other->m14.GetSize())
            bStack_5 = 1;
        if (bStack_5 == 0) {
            for (uStack_18 = 0; uStack_18 < m14.GetSize() && bStack_5 == 0; ++uStack_18) {
                bStack_5 = (bStack_5 == 0 && m14.FUN_00691750((int)uStack_18)->FUN_005ece20(
                     (int)other->m14.FUN_00691750((int)uStack_18)) == 0) ? 0 : 1;
            }
        }
        if (m4.GetSize() != other->m4.GetSize())
            bStack_5 = 1;
        if (bStack_5 == 0) {
            for (uStack_c = 0; uStack_c < m4.GetSize() && bStack_5 == 0; ++uStack_c) {
                bStack_5 = (bStack_5 == 0 && FUN_00408b20(m4.GetAt((int)uStack_c),
                     other->m4.GetAt((int)uStack_c)) == 0) ? 0 : 1;
            }
        }
    }
    if (bStack_5 != 0 || m0 != other->m0)
        bStack_5 = 1;
    return bStack_5;
}