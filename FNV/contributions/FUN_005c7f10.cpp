class SCRIPT_PARAMETER;
class TESObjectREFR;
class Script;
class ScriptLocals;
class TESForm;
extern bool ExtractArgs(const SCRIPT_PARAMETER*, const char*, unsigned int*, TESObjectREFR*, TESObjectREFR*, Script*, ScriptLocals*, ...);
struct CommandTarget {
    int FUN_004181e0();
    void FUN_008b86e0(TESForm*, unsigned char, bool);
};
extern CommandTarget* __cdecl FUN_00ec43fb(TESObjectREFR*, int, const char*, const char*, int);
extern const char DAT_011841cc[];
extern const char DAT_011846d4[];
extern CommandTarget* DAT_011dea3c;

bool __cdecl FUN_005c7f10(const SCRIPT_PARAMETER* parameters,
                          const char* scriptData, TESObjectREFR* reference,
                          TESObjectREFR* container, Script* script,
                          ScriptLocals* locals, double& result,
                          unsigned int& offset)
{
    TESForm* form = 0;
    unsigned int value = 0;
    if (!ExtractArgs(parameters, scriptData, &offset, reference,
                     container, script, locals, &form, &value))
        return false;

    result = 0.0;
    CommandTarget* status = FUN_00ec43fb(reference, 0, DAT_011841cc, DAT_011846d4, 0);
    if (!status)
        return true;

    int target = status->FUN_004181e0();
    if (status && form)
        status->FUN_008b86e0(form, (unsigned char)value, status == DAT_011dea3c);
    return true;
}
