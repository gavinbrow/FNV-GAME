// FUN_00e9e730 — clone method: allocates a new object via the memory
// manager, initializes its member, copies the bounding-volume data and the
// trailing NiPoint3, and returns the clone (NULL when allocation fails).
//
// Target: __thiscall, caller pops, size 78, /MT /O2 /GS /EHsc /Gy.
// Uses the pack's declarations: NiBoundingVolume, NiPoint3, P03MM,
// g_memoryManager.

// Non-polymorphic stand-in for the member object living at wrapper offset
// +4 (16 bytes); FUN_00a69940 is its out-of-line initialization helper.
struct FUN_00a69940_Member {
    int unk04;
    int unk08;
    int unk0C;
    int unk10;
    void FUN_00a69940();
};

// The cloned object: NiBoundingVolume-derived, vtable at +0, member at +4,
// NiPoint3 at +0x14, total size 0x20 (operator new hands exactly 0x20 to
// the memory manager). The class carries no FUN_00e9e730 token in its own
// name so the target symbol stays unique.
struct CloneNode : NiBoundingVolume {
    virtual ~CloneNode();
    void FUN_00e9cbb0(const FUN_00a69940_Member* kABV);
    FUN_00a69940_Member member;
    NiPoint3 point;
    void* operator new(unsigned int size) { return g_memoryManager.Allocate(size); }
    NiBoundingVolume* FUN_00e9e730();
};

CloneNode::~CloneNode() {}

NiBoundingVolume* CloneNode::FUN_00e9e730() {
    CloneNode* clone = new CloneNode();
    if (clone == 0) {
        return 0;
    }
    clone->member.FUN_00a69940();
    clone->FUN_00e9cbb0(&this->member);
    clone->point = this->point;
    return clone;
}
