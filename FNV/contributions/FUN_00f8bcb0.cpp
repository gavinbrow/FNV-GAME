class GameSettingCollection;

union SETTING_VALUE
{
    int integerValue;
    float floatValue;
    const char* stringValue;
};

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

extern SettingT<GameSettingCollection> DAT_011d870c;
extern GlobalObject_0045d060 DAT_011d8724;
extern const char DAT_0106e660[];

extern "C" void __cdecl FUN_00fd7a30();
extern "C" int __cdecl atexit(void (__cdecl* callback)());

// @fnv 0x00f8bcb0
void __cdecl FUN_00f8bcb0()
{
    DAT_011d8724.FUN_0045d060(DAT_0106e660, DAT_011d870c.Float()->floatValue);
    atexit(FUN_00fd7a30);
}
