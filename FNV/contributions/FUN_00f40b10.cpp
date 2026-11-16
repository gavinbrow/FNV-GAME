union SETTING_VALUE
{
    float floatingPoint;
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

extern SettingT<GameSettingCollection> DAT_011c744c;
extern GlobalObject_0045d060 DAT_011c7740;
extern const char DAT_01022218[];
extern void __cdecl FUN_00fc9680();
extern "C" int __cdecl atexit(void (__cdecl* callback)());

// @fnv 0x00f40b10
void FUN_00f40b10()
{
    DAT_011c7740.FUN_0045d060(DAT_01022218, DAT_011c744c.Float()->floatingPoint);
    atexit(FUN_00fc9680);
}
