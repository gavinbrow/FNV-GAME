class GameSettingCollection;

union SETTING_VALUE
{
    float floatValue;
};

template <class Collection>
class SettingT
{
public:
    SETTING_VALUE* Float();
};

extern SettingT<GameSettingCollection> DAT_011d9774;
extern const double DAT_0101e568;
extern float DAT_011d979c;

// @fnv 0x00f8fa80
void __cdecl FUN_00f8fa80()
{
    DAT_011d979c = DAT_011d9774.Float()->floatValue * DAT_0101e568;
}
