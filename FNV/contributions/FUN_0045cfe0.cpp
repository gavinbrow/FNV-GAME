struct FUN_00404920
{
    FUN_00404920(int type, int value);
    ~FUN_00404920();
};

struct INISettingCollection
{
    virtual void Unknown() = 0;
    virtual void Register(FUN_00404920* setting) = 0;
};

extern INISettingCollection* FUN_0044f560();
extern char DAT_01017720;

struct FUN_0045cfe0 : FUN_00404920
{
    FUN_0045cfe0(int type, int value);
};

// @fnv 0x0045cfe0
FUN_0045cfe0::FUN_0045cfe0(int type, int value)
    : FUN_00404920(type, value)
{
    *reinterpret_cast<void**>(this) = &DAT_01017720;
    FUN_0044f560()->Register(this);
}
