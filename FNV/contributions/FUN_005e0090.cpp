class SCRIPT_PARAMETER;
class Script;
class ScriptLocals;
struct PlayerMethods {
    void FUN_00969fa0();
};
extern TESObjectREFR* _g_thePlayer;
extern bool __cdecl FUN_005accb0(const SCRIPT_PARAMETER*, const char*, unsigned int*, TESObjectREFR*, TESObjectREFR*, Script*, ScriptLocals*, int*, int*);
extern void __cdecl FUN_007054f0(bool);

bool __cdecl FUN_005e0090(const SCRIPT_PARAMETER* parameters,
                          const char* scriptData,
                          TESObjectREFR* source,
                          TESObjectREFR* container,
                          Script* script,
                          ScriptLocals* locals,
                          double& result,
                          unsigned int& offset)
{
    int mode = 0;
    int selected;
    if (!FUN_005accb0(parameters, scriptData, &offset, source, container,
                       script, locals, &selected, &mode))
        return false;

    if (mode == 1)
        reinterpret_cast<PlayerMethods*>(_g_thePlayer)->FUN_00969fa0();
    else
        FUN_007054f0(selected == 1);

    return true;
}