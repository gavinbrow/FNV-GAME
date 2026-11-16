class SCRIPT_PARAMETER;
class TESObjectREFR;
class Script;
class ScriptLocals;
extern bool __cdecl FUN_005accb0(
    const SCRIPT_PARAMETER*, const char*, unsigned int&,
    TESObjectREFR*, TESObjectREFR*, Script*, ScriptLocals*,
    int*, int*);
extern bool __cdecl FUN_005a4090(TESObjectREFR*, int, int, double&);

bool __cdecl FUN_005d75a0(
    const SCRIPT_PARAMETER* params, const char* arguments,
    TESObjectREFR* object, TESObjectREFR* container,
    Script* script, ScriptLocals* locals,
    double& result, unsigned int& offset)
{
    int parsedB = 0;
    int parsedA = 0;
    if (!FUN_005accb0(params, arguments, offset, object, container,
                     script, locals, &parsedB, &parsedA)) {
        return false;
    }
    return FUN_005a4090(object, parsedB, parsedA, result);
}