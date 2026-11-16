
struct ScriptTargetForm : TESForm {
    virtual void V58();
    virtual void V59();
    virtual void V60();
    virtual void V61();
    virtual void V62();
    virtual void V63();
    virtual bool Validate();
};

struct ScriptResult {
    void FUN_008c1ac0(bool positive);
};

extern bool __cdecl FUN_005accb0(
    unsigned int first, unsigned int second, unsigned int last,
    ScriptTargetForm* form, unsigned int fourth, unsigned int fifth,
    unsigned int sixth, int* result);

extern ScriptResult* __cdecl FUN_00ec43fb(
    ScriptTargetForm* form, int zero, const void* a,
    const void* b, int flags);

extern void __cdecl FUN_00703c00(const void* value);
extern const int DAT_011841cc;
extern const int DAT_011846d4;
extern const int DAT_0103d31c;

bool __cdecl FUN_005dfd30(
    unsigned int first, unsigned int second, ScriptTargetForm* form,
    unsigned int fourth, unsigned int fifth, unsigned int sixth,
    unsigned int seventh, unsigned int last)
{
    int outcome;
    if (!FUN_005accb0(first, second, last, form, fourth, fifth, sixth, &outcome))
        return false;

    if (form->Validate()) {
        ScriptResult* result = FUN_00ec43fb(form, 0, &DAT_011841cc, &DAT_011846d4, 0);
        result->FUN_008c1ac0(outcome > 0);
    } else if (__tls_index[0x268]) {
        FUN_00703c00(&DAT_0103d31c);
    }

    return true;
}
