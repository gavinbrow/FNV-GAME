extern int DAT_010e33dc;
struct FUN_00dfd990_class {
    void* vtable;
    int field04;
    int field08;
    int field0c;
    int field10;
    FUN_00cb0a70_class field14;
};
void __cdecl FUN_00dfd990(FUN_00dfd990_class* object, int value)
{
    if (object) {
        object->vtable = &DAT_010e33dc;
        object->field14.FUN_00cb0a70(value);
    }
}