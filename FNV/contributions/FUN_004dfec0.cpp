extern double DAT_010229b8;
extern double DAT_01012070;
struct FUN_004dfec0_Class {
    unsigned int FUN_00476be0();
    float FUN_004dfec0();
};
float FUN_004dfec0_Class::FUN_004dfec0()
{
    unsigned int randomValue = FUN_00476be0();
    return static_cast<float>(
        static_cast<double>(randomValue) * DAT_010229b8 - DAT_01012070);
}
