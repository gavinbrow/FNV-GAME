struct FUN_004f5590 { int first; int second; int third; FUN_004f5590(int a, int b); };
struct FUN_004f5940_factory { virtual void v0(); virtual int GetFirst(); virtual void v2(); virtual int GetSecond(); FUN_004f5590* FUN_004f5940(FUN_004f5590* existing); };
FUN_004f5590* FUN_004f5940_factory::FUN_004f5940(FUN_004f5590* existing) {
    FUN_004f5590* result = existing != 0
        ? existing
        : new FUN_004f5590(GetFirst(), GetSecond());
    return result;
}