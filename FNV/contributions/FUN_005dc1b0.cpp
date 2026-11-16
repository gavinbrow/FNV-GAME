class ScriptParameter;
class TESObjectREFR;
class Script;
class ScriptLocals;

extern bool __cdecl FUN_005accb0(
    const ScriptParameter*, const char*, unsigned int*, TESObjectREFR*,
    TESObjectREFR*, Script*, ScriptLocals*, ...);
extern float __cdecl FUN_005dc270(float value);
extern float __cdecl FUN_004e4470(float value);
extern const double DAT_0102f248;

// @fnv 0x005dc1b0
bool FUN_005dc1b0(
    const ScriptParameter* parameters,
    const char* data,
    TESObjectREFR* reference,
    TESObjectREFR* container,
    Script* script,
    ScriptLocals* locals,
    double& result,
    unsigned int& offset)
{
    float value = 0.0f;
    int mode = 0;
    if (!FUN_005accb0(parameters, data, &offset, reference, container,
                     script, locals, &value, &mode))
    {
        return false;
    }
    if (mode != 0)
    {
        if (value < -1.0f)
        {
            value = -1.0f;
        }
        if (value > 1.0f)
        {
            value = 1.0f;
        }
        result = FUN_005dc270(value) * DAT_0102f248;
    }
    else
    {
        result = FUN_004e4470(value * 0.01745329251994329577f);
    }
    return true;
}
