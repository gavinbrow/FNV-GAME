class GameSettingCollection;

union SETTING_VALUE
{
    float floatingPoint;
    unsigned int integer;
    const char* text;
};

template <class Collection>
class SettingT
{
public:
    SETTING_VALUE* Float();
};

extern SettingT<GameSettingCollection> DAT_011ccc40;
extern float DAT_011ccc60;

// @fnv 0x00f587a0
void FUN_00f587a0()
{
    DAT_011ccc60 = 1.0f / DAT_011ccc40.Float()->floatingPoint;
}
