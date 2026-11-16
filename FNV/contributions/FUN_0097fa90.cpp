struct FUN_0097fa90_Class {
    float value;
    float FUN_0097fa90();
};
extern double __cdecl FUN_00435dd0();
extern double _DAT_01017b70;

float FUN_0097fa90_Class::FUN_0097fa90()
{
    return (float)(FUN_00435dd0() - value > _DAT_01017b70
        ? _DAT_01017b70
        : FUN_00435dd0() - value);
}