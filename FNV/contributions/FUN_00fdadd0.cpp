extern "C" __declspec(dllimport) long __stdcall InterlockedDecrement(volatile long*);
extern "C" char* DAT_011f3ec0;
extern "C" char* DAT_0109b220;
void FUN_00fdadd0() {
 char* p = DAT_011f3ec0;
 if (p != DAT_0109b220)
     InterlockedDecrement(reinterpret_cast<volatile long*>(p - 8));
}