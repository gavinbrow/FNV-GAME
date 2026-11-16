class ScriptParameter;
class TESObjectREFR;
class Script;
class ScriptLocals;

extern "C" bool __cdecl FUN_005accb0(const ScriptParameter*, const char*,
    unsigned int*, TESObjectREFR*, TESObjectREFR*, Script*, ScriptLocals*, ...);
extern "C" float __cdecl FUN_004b5510(float value);
extern "C" float __cdecl FUN_004e44b0(float value);

extern const double DAT_0102f248;

// @fnv 0x005dc0f0
bool FUN_005dc0f0(const ScriptParameter* parameters, const char* scriptData,
    TESObjectREFR* reference, TESObjectREFR* containingReference,
    Script* script, ScriptLocals* locals, double& result, unsigned int& offset)
{
    float value = 0.0f;
    int option = 0;
    if (!FUN_005accb0(parameters, scriptData, &offset, reference,
        containingReference, script, locals, &value, &option))
    {
        return false;
    }
    if (option != 0)
    {
        if (value < -1.0f)
        {
            value = -1.0f;
        }
        if (value > 1.0f)
        {
            value = 1.0f;
        }
        result = FUN_004b5510(value) * DAT_0102f248;
    }
    else
    {
        result = FUN_004e44b0(static_cast<float>(value * 0.01745329238474369));
    }
    return true;
}
