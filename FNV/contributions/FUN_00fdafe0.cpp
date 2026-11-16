extern "C" __declspec(dllimport) long __stdcall InterlockedDecrement(volatile long*);
extern "C" char* DAT_011f49e0;
extern "C" char* DAT_0109b220;
void FUN_00fdafe0() {
 char* p = DAT_011f49e0;
 if (p != DAT_0109b220)
     InterlockedDecrement(reinterpret_cast<volatile long*>(p - 8));
}