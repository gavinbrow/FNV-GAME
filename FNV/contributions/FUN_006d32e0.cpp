struct Vec3 {
    float x, y, z;
};
extern Vec3 DAT_011f426c;
extern float DAT_0106cb30;

struct FUN_00435de0 {
    float value;
    FUN_00435de0(float initial);
};
struct FUN_006dae60 {
    unsigned int field0, field4, field8, fieldC;
    FUN_006dae60();
};
struct FUN_006d32e0 {
    Vec3 translation;
    Vec3 rotation;
    float progress;
    FUN_00435de0 time;
    FUN_006dae60 state;
    unsigned int count;
    unsigned int flags;
    unsigned char enabled;
    FUN_006d32e0();
};

FUN_006d32e0::FUN_006d32e0()
    : translation(DAT_011f426c),
      rotation(DAT_011f426c),
      progress(0.0f),
      time(-DAT_0106cb30),
      state(),
      count(0),
      flags(0),
      enabled(0)
{
}