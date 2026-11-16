extern double DAT_01012060;
struct MotionRule {
    bool FUN_00946280();
};
bool MotionRule::FUN_00946280()
{
    return *reinterpret_cast<const float*>(reinterpret_cast<const char*>(this) + 0x198)
        <= DAT_01012060;
}