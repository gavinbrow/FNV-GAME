extern "C" __declspec(dllimport) long __stdcall InterlockedDecrement(volatile long*);
struct Ref462f0 { virtual void Dummy() = 0; virtual void Dispose() = 0; volatile long referenceCount; };
extern Ref462f0* DAT_01202e14;
// @fnv 0x00fdd690
void FUN_00fdd690(){if(DAT_01202e14){Ref462f0* original=DAT_01202e14; if(InterlockedDecrement(&original->referenceCount)==0){original->Dispose();}}}