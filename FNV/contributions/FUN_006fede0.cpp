struct PointerSource {
    int FUN_0059bb30();
    int FUN_0045cd60();
};
extern PointerSource* g_011dea10;

struct ScreenSize {
    int* FUN_0043d4d0();
};
extern ScreenSize g_011c63cc;

struct HitRect {
    int unk00;
    int extent;
    short left;
    short top;
    bool FUN_006fede0();
};

bool HitRect::FUN_006fede0()
{
    int y;
    int x;
    x = g_011dea10->FUN_0059bb30() - (int)((unsigned int)*g_011c63cc.FUN_0043d4d0() >> 1);
    y = g_011dea10->FUN_0045cd60() - (int)((unsigned int)*g_011c63cc.FUN_0043d4d0() >> 1);
    if (x + *g_011c63cc.FUN_0043d4d0() >= left
        && x <= left + extent
        && y + *g_011c63cc.FUN_0043d4d0() >= top
        && y <= top + extent) {
        return true;
    }
    return false;
}
