struct PlayerCharacter {
    bool IsSneaking();
    bool MovingCheck();
};
struct TESSound;
struct SoundDataHandler {
    TESSound* GetSound(const char*);
};
extern PlayerCharacter* g_thePlayer;
extern SoundDataHandler* DAT_011c3f2c;
const char* __cdecl FUN_005e2b50(const char*);
int __cdecl _sprintf_s(char*, unsigned int, const char*, ...);

TESSound* FUN_005e2a70(const char* apPrefix)
{
    char soundName[40];
    char fallbackName[40];
    if (g_thePlayer)
    {
        const char* motion;
        if (g_thePlayer->IsSneaking())
            motion = "Sneak";
        else
        {
            const char* regularMotion;
            if (g_thePlayer->MovingCheck())
                regularMotion = "Run";
            else
                regularMotion = "Walk";
            motion = regularMotion;
        }
        _sprintf_s(soundName, 40, "BRUSH%s%s", FUN_005e2b50(apPrefix), motion);
        return DAT_011c3f2c->GetSound(soundName);
    }
    else
    {
        _sprintf_s(fallbackName, 40, "BRUSH%sWalk", FUN_005e2b50(apPrefix));
        return DAT_011c3f2c->GetSound(fallbackName);
    }
    return 0;
}