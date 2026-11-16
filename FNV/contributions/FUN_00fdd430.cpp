extern "C" __declspec(dllimport) void __stdcall DeleteCriticalSection(void*);
extern "C" char DAT_01202d78;
struct FUN_00fdd430 {
  ~FUN_00fdd430() { DeleteCriticalSection(&DAT_01202d78); }
};
static FUN_00fdd430 g_fdd430;