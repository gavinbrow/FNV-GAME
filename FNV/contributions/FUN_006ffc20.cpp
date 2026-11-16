extern "C" __declspec(dllimport) void __cdecl SteamAPI_RegisterCallback(void* callback, int callbackId);

struct FUN_006ffc20_shell : FUN_006ff970_Class {
    int callbackObject;
    int callbackTarget;
    enum { kGameServerCallback = 0 };
    void FUN_006ffc20(int object, int target);
};

void FUN_006ffc20_shell::FUN_006ffc20(int object, int target)
{
    if (object == 0 || target == 0)
        return;

    if ((static_cast<unsigned char>(m_b) & 1) != 0)
        reinterpret_cast<FUN_006ffc00_Class*>(this)->FUN_006ffc00();

    if (kGameServerCallback)
        m_b = static_cast<unsigned char>(m_b) | 2;

    callbackObject = object;
    callbackTarget = target;
    SteamAPI_RegisterCallback(this, 0x44f);
}