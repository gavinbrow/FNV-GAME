struct FUN_006dcf20 {
    void** vtable;
    NiPoint3 location;
    const NavMeshInfo* navMesh;
    const BSSimpleArray<NavMeshInfo_const*,1024>* navMeshes;
    TESObjectCELL* cell;
    TESWorldSpace* worldSpace;
    unsigned int cellKey;
    unsigned short triangle;
    unsigned char flags;
    unsigned char reserved;
    FUN_006dcf20(const NiPoint3& position, TESObjectREFR* reference);
    ~FUN_006dcf20();
};
struct PathingLocationOwner {
    void FUN_006ed7a0(FUN_006dcf20* location);
    void FUN_006ed730(const NiPoint3& position, TESObjectREFR* reference);
};
void PathingLocationOwner::FUN_006ed730(const NiPoint3& position, TESObjectREFR* reference) {
    FUN_006dcf20 location(position, reference);
    FUN_006ed7a0(&location);
}