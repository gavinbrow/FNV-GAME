struct NiPoint3StartupTable {};
extern NiPoint3StartupTable gNiPoint3StartupDst;
extern "C" void __fastcall FUN_00a7cca0(NiPoint3StartupTable*);
void FUN_00fb5860() { FUN_00a7cca0(&gNiPoint3StartupDst); }
