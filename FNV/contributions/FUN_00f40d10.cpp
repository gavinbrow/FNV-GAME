union SETTING_VALUE
{
    float floatValue;
};

class GameSettingCollection;

template <class Collection>
class SettingT
{
public:
    SETTING_VALUE* Float();
};

class GlobalObject_0045d060
{
public:
    void FUN_0045d060(const char* name, float value);
};

extern SettingT<GameSettingCollection> DAT_011c7494;
extern GlobalObject_0045d060 DAT_011c7598;
extern const char DAT_01022354[];
extern void __cdecl FUN_00fc9720();
extern "C" int __cdecl atexit(void (__cdecl* callback)());

// @fnv 0x00f40d10
void FUN_00f40d10()
{
    DAT_011c7598.FUN_0045d060(DAT_01022354, DAT_011c7494.Float()->floatValue);
    atexit(FUN_00fc9720);
}
