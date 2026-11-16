class SCRIPT_PARAMETER;
class TESObjectREFR;
class Script;
class ScriptLocals;

bool __cdecl FUN_005accb0(
    const SCRIPT_PARAMETER*, const char*, unsigned int*,
    TESObjectREFR*, TESObjectREFR*, Script*, ScriptLocals*, unsigned int*);

bool __cdecl FUN_005a3f00(TESObjectREFR*, unsigned int, int, double*);

bool __cdecl FUN_005d74e0(
    const SCRIPT_PARAMETER* parameters,
    const char* commandText,
    TESObjectREFR* reference,
    TESObjectREFR* containingReference,
    Script* script,
    ScriptLocals* locals,
    double* result,
    unsigned int* opcodeOffset)
{
    unsigned int extractedValue = 0;
    if (!FUN_005accb0(parameters, commandText, opcodeOffset, reference,
                       containingReference, script, locals, &extractedValue)) {
        return false;
    }
    return FUN_005a3f00(reference, extractedValue, 0, result);
}