
struct FNVActivationNode_00564b70 {
    virtual void Unknown000() = 0;
    virtual void Unknown004() = 0;
    virtual void Unknown008() = 0;
    virtual void Unknown00c() = 0;
    virtual void Unknown010() = 0;
    virtual void Unknown014() = 0;
    virtual void Unknown018() = 0;
    virtual void Unknown01c() = 0;
    virtual void Unknown020() = 0;
    virtual void Unknown024() = 0;
    virtual void Unknown028() = 0;
    virtual void Unknown02c() = 0;
    virtual void Unknown030() = 0;
    virtual void Unknown034() = 0;
    virtual void Unknown038() = 0;
    virtual void Unknown03c() = 0;
    virtual void Unknown040() = 0;
    virtual void Unknown044() = 0;
    virtual void Unknown048() = 0;
    virtual void Unknown04c() = 0;
    virtual void Unknown050() = 0;
    virtual void Unknown054() = 0;
    virtual void Unknown058() = 0;
    virtual void Unknown05c() = 0;
    virtual void Unknown060() = 0;
    virtual void Unknown064() = 0;
    virtual void Unknown068() = 0;
    virtual void Unknown06c() = 0;
    virtual void Unknown070() = 0;
    virtual void Unknown074() = 0;
    virtual void Unknown078() = 0;
    virtual void Unknown07c() = 0;
    virtual void Unknown080() = 0;
    virtual void Unknown084() = 0;
    virtual void Unknown088() = 0;
    virtual void Unknown08c() = 0;
    virtual void Unknown090() = 0;
    virtual void Unknown094() = 0;
    virtual void Unknown098() = 0;
    virtual void Unknown09c() = 0;
    virtual void Unknown0a0() = 0;
    virtual void Unknown0a4() = 0;
    virtual bool HasState() = 0;
};
struct FUN_00564b70_Class : TESObjectREFR {
    FNVActivationNode_00564b70* FUN_007af430();
    bool FUN_00564b70();
};
bool FUN_00564b70_Class::FUN_00564b70()
{
    return FUN_007af430() != 0 && FUN_007af430()->HasState();
}
