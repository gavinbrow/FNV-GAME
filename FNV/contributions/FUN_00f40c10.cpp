// @fnv 0x00f40c10
class GameSettingCollection;

union SETTING_VALUE
{
    float f;
    unsigned int u;
};

template <class T>
class SettingT
{
public:
    SETTING_VALUE* Float();
};

class GlobalObject_0045d060
{
public:
    // Calls the constructor entry point at 0x0045d060.
    void FUN_0045d060(const char* name, float value);
};

extern SettingT<GameSettingCollection> DAT_011c7278;
extern GlobalObject_0045d060 DAT_011c7568;
extern char DAT_010222b8;
extern "C" int __cdecl atexit(void (__cdecl*)());
extern "C" void FUN_00fc96d0();

void FUN_00f40c10()
{
    DAT_011c7568.FUN_0045d060(&DAT_010222b8, DAT_011c7278.Float()->f);
    atexit(&FUN_00fc96d0);
}
