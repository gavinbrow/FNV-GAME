extern SettingT_GameSettingCollection_ DAT_011cfd58;
extern SettingT_GameSettingCollection_ DAT_011cf618;
extern SettingT_GameSettingCollection_ DAT_011cf624;
extern SettingT_GameSettingCollection_ DAT_011cfe74;
extern SettingT_GameSettingCollection_ DAT_011cfd04;
extern SettingT_GameSettingCollection_ DAT_011cf724;
extern SettingT_GameSettingCollection_ DAT_011cf950;
extern SettingT_GameSettingCollection_ DAT_011cfb9c;
float __cdecl FUN_00408840(float);

float __cdecl FUN_006466e0(float aValue, bool bAlternative) {
    float maxValue = bAlternative ? DAT_011cfd58.Float()->f : DAT_011cf618.Float()->f;
    float lowOutput = bAlternative ? DAT_011cf624.Float()->f : DAT_011cfe74.Float()->f;
    float value = bAlternative ? DAT_011cfd04.Float()->f : DAT_011cf724.Float()->f;
    float minValue = bAlternative ? DAT_011cf950.Float()->f : DAT_011cfb9c.Float()->f;
    float highOutput = FUN_00408840(aValue);
    highOutput = (highOutput - maxValue) / (lowOutput - maxValue);
    highOutput = FUN_0040ebd0(1.0f, FUN_00404010(highOutput, 0.0f));
    return (minValue - value) * highOutput + value;
}