struct FUN_00559450_Object { void* FUN_00559450(); };
extern FUN_00559450_Object DAT_011c73b4;
struct FUN_004b9930_Object { unsigned char FUN_004b9930(int id, int enabled); };
extern FUN_004b9930_Object DAT_011c77b4;
int __cdecl FUN_004dc270();
int __cdecl FUN_004dcbe0(int value);
int __stdcall FUN_004dc210(int value);
struct FUN_004dd220_Object { int FUN_004dd220(); };
struct DispatchInterface;
struct DispatchVTable {
    void* method00;
    void* method01;
    void* method02;
    void* method03;
    void* method04;
    void* method05;
    void* method06;
    void* method07;
    void* method08;
    void* method09;
    void* method10;
    long (__stdcall* dispatch)(DispatchInterface*, int, int, int);
};
struct DispatchInterface { DispatchVTable* vtable; };
DispatchInterface* __cdecl FUN_004dc040();
bool __cdecl FUN_004dd180(int formId, int requestedValue) {
    int result;
    DispatchInterface* selectedValue;
    long dispatcher;
    if (DAT_011c73b4.FUN_00559450()) {
        if (requestedValue)
            result = requestedValue;
        else
            result = FUN_004dcbe0(FUN_004dc270());

        DAT_011c73b4.FUN_00559450();
        selectedValue = FUN_004dc040();
        dispatcher = selectedValue->vtable->dispatch(
            selectedValue,
            FUN_004dc210(((FUN_004dd220_Object*)DAT_011c73b4.FUN_00559450())->FUN_004dd220()),
            result,
            DAT_011c77b4.FUN_004b9930(formId, 0));
        if (dispatcher >= 0)
            return true;
    }
    return false;
}