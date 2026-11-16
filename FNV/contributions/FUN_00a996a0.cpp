struct FUN_00a94360_Base {
    virtual void v00();
    FUN_00a94360_Base();
};
struct CloneLODNode : FUN_00a94360_Base {
    virtual void v01();
    CloneLODNode() {
        *reinterpret_cast<int*>(reinterpret_cast<char*>(this) + 0xcc) = 0;

    }
};
inline void* operator new(unsigned int, void* p) { return p; }
struct FUN_00a996a0_shell : FUN_00a99390_shell {
    CloneLODNode* FUN_00a996a0(NiCloningProcess& process);
};
CloneLODNode* FUN_00a996a0_shell::FUN_00a996a0(NiCloningProcess& process) {
    void* memory = BSFadeNode::operator new(0xd4);
    CloneLODNode* clone = memory ? new (memory) CloneLODNode() : 0;
    if (clone) {
        *reinterpret_cast<int*>(reinterpret_cast<char*>(clone) + 0xb0) = 0;
        *reinterpret_cast<unsigned char*>(reinterpret_cast<char*>(clone) + 0xd0) = 1;
    }
    FUN_00a99390(reinterpret_cast<NiSwitchNode*>(clone), process);
    return clone;
}