class TESForm {
public:
    virtual void RTTIAnchor();
};
class TESAttackDamageForm {
public:
    virtual int v0();
    virtual int v1();
    virtual int v2();
    virtual int v3();
    virtual int GetResult();
};
int __cdecl FUN_0047fef0(TESForm* form) {
    TESAttackDamageForm* found = dynamic_cast<TESAttackDamageForm*>(form);
    if (found != 0) {
        return found->GetResult();
    } else {
        return 0;
    }
}