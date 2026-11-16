struct Vec2 {
    unsigned int x;
    unsigned int y;
    void FUN_006815c0();
};
struct Vec3 {
    unsigned int x;
    unsigned int y;
    unsigned int z;
    void FUN_006815c0();
};
extern Vec3 DAT_011f426c;

struct FUN_004e8e40_owner {
    Vec2 first;
    Vec2 second;
    Vec3 third;
    FUN_004e8e40_owner* FUN_004e8e40();
};
FUN_004e8e40_owner* FUN_004e8e40_owner::FUN_004e8e40()
{
    first.FUN_006815c0();
    second.FUN_006815c0();
    third.FUN_006815c0();
    first = *reinterpret_cast<const Vec2*>(&DAT_011f4980);
    second = *reinterpret_cast<const Vec2*>(&DAT_011f4980);
    third = DAT_011f426c;
    return this;
}
