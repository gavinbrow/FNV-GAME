class ScriptParameter;
class TESObjectREFR;
class Script;
class ScriptLocals;

extern bool __cdecl FUN_005accb0(const ScriptParameter*, const char*, unsigned int*, TESObjectREFR*, TESObjectREFR*, Script*, ScriptLocals*, ...);
namespace fnv_00953060
{
    float xAtan(float);
}
extern float FUN_0057dd70(float);
extern const double DAT_0102f248;

// @fnv 0x005dc290
bool FUN_005dc290(const ScriptParameter* parameters, const char* data, TESObjectREFR* reference, TESObjectREFR* container, Script* script, ScriptLocals* locals, double& result, unsigned int& offset)
{
    float value = 0.0f;
    int inverse = 0;
    if (!FUN_005accb0(parameters, data, &offset, reference, container, script, locals, &value, &inverse))
    {
        return false;
    }
    if (inverse != 0)
    {
        result = fnv_00953060::xAtan(value) * DAT_0102f248;
    }
    else
    {
        result = FUN_0057dd70(value * 0.017453292519943295f);
    }
    return true;
}
