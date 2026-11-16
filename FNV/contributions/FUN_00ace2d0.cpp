extern int DAT_010a318c;
extern int DAT_010a2fa4;
extern int DAT_010a2f9c;
void __cdecl FUN_00ec3205(void* component);
struct FUN_00ace2d0_Class {
    int* virtualBaseOffsets;
    void* componentVTable;
    void FUN_00ace2d0();
};
void FUN_00ace2d0_Class::FUN_00ace2d0() {
    char* subobject;
    char* virtualBaseObject;
    virtualBaseObject = reinterpret_cast<char*>(this) + 4;
    *reinterpret_cast<void**>(
        virtualBaseObject + (*reinterpret_cast<int**>(virtualBaseObject - 4))[1] - 4) = &DAT_010a318c;
    subobject = reinterpret_cast<char*>(this) + 4;
    *reinterpret_cast<void**>(subobject) = &DAT_010a2fa4;
    *reinterpret_cast<void**>(subobject) = &DAT_010a2f9c;
    FUN_00ec3205(subobject);
}