class SCRIPT_PARAMETER;
class Script;
class ScriptLocals;

class ExtendedREFR : public TESObjectREFR {
public:
    void* FUN_007af430(int, int, int, int, int, int, int, int, int);
    virtual void UnknownVirtual58() = 0;
    virtual void UnknownVirtual59() = 0;
    virtual void UnknownVirtual60() = 0;
    virtual void UnknownVirtual61() = 0;
    virtual void UnknownVirtual62() = 0;
    virtual void UnknownVirtual63() = 0;
    virtual void UnknownVirtual64() = 0;
    virtual void UnknownVirtual65() = 0;
    virtual void UnknownVirtual66() = 0;
    virtual void UnknownVirtual67() = 0;
    virtual void UnknownVirtual68() = 0;
    virtual void UnknownVirtual69() = 0;
    virtual void UnknownVirtual70() = 0;
    virtual void UnknownVirtual71() = 0;
    virtual void UnknownVirtual72() = 0;
    virtual void UnknownVirtual73() = 0;
    virtual void UnknownVirtual74() = 0;
    virtual void UnknownVirtual75() = 0;
    virtual void UnknownVirtual76() = 0;
    virtual void UnknownVirtual77() = 0;
    virtual void UnknownVirtual78() = 0;
    virtual void UnknownVirtual79() = 0;
    virtual void UnknownVirtual80() = 0;
    virtual void UnknownVirtual81() = 0;
    virtual void UnknownVirtual82() = 0;
    virtual void UnknownVirtual83() = 0;
    virtual void UnknownVirtual84() = 0;
    virtual void UnknownVirtual85() = 0;
    virtual void UnknownVirtual86() = 0;
    virtual void UnknownVirtual87() = 0;
    virtual void UnknownVirtual88() = 0;
    virtual void UnknownVirtual89() = 0;
    virtual void UnknownVirtual90() = 0;
    virtual void UnknownVirtual91() = 0;
    virtual void UnknownVirtual92() = 0;
    virtual void UnknownVirtual93() = 0;
    virtual void UnknownVirtual94() = 0;
    virtual void ReceiveTarget(void*) = 0;
};

class RefManager {
public:
    void FUN_00952c30(ExtendedREFR*);
};

extern RefManager* DAT_011dea3c;
bool __cdecl FUN_00702360();
void __cdecl FUN_00704af0();

bool __cdecl FUN_005b5860(const SCRIPT_PARAMETER*, const char*,
                           ExtendedREFR* source, ExtendedREFR* target,
                           Script*, ScriptLocals*, double&, unsigned int&)
{
    if (source != 0 && target != 0) {
        target->ReceiveTarget(source->FUN_007af430(0, 1, 0, 1, 0, 0, 0, 1, 0));
        DAT_011dea3c->FUN_00952c30(source);
        if (FUN_00702360()) {
            FUN_00704af0();
        }
        return false;
    }
    return true;
}