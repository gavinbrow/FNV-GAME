struct PlayerCharacter { bool FUN_00953f60(); };
void __cdecl _DebugLog(const char* format, ...);
__declspec(thread) bool g_DebugLogFlag;
bool FUN_005a1e70(TESObjectREFR* reference, void* arg1, void* arg2, double& result)
{
    result = 0.0;
    result = ((PlayerCharacter*)g_thePlayer)->FUN_00953f60() ? 1.0f : 0.0f;
    if (g_DebugLogFlag)
        _DebugLog("IsPlayerAMurderer >> %0.2f", result);
    return true;
}