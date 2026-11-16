union SETTING_VALUE
{
    float floatingValue;
    int integerValue;
    const char* stringValue;
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

extern SettingT<GameSettingCollection> DAT_011d8770;
extern const char DAT_0106e700[];
extern GlobalObject_0045d060 DAT_011d8788;
extern void FUN_00fd7a70();
extern "C" int __cdecl atexit(void (__cdecl* callback)());

// @fnv 0x00f8bd80
void FUN_00f8bd80()
{
    DAT_011d8788.FUN_0045d060(DAT_0106e700, DAT_011d8770.Float()->floatingValue);
    atexit(FUN_00fd7a70);
}
