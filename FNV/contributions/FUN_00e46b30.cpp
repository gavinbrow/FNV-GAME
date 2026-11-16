extern int DAT_010e7874;
extern int DAT_010e7868;
extern int DAT_010e7854;
extern int DAT_010e7848;
extern int DAT_010e783c;
extern int DAT_010e781c;
extern int DAT_010cb1e4;

struct FUN_00cbfba0_Base {
    void FUN_00cbfba0();
};
struct FUN_00c90510_Reference {
    void FUN_00c90510();
};
struct FUN_00e46b30_Layout {
    void* primaryVtable;
    int referenceCount;
    void* secondaryVtable;
    void* thirdVtable;
    void* fourthVtable;
    void* fifthVtable;
    int field18;
    int field1c;
    int field20;
    int field24;
    int field28;
    int field2c;
    void* volatile listenerVtable;
    FUN_00c90510_Reference* reference;
};
struct FUN_00e46b30_Class : FUN_00e46b30_Layout {
    FUN_00e46b30_Class* FUN_00e46b30(FUN_00c90510_Reference* value);
};
FUN_00e46b30_Class* FUN_00e46b30_Class::FUN_00e46b30(FUN_00c90510_Reference* value)
{
    reinterpret_cast<FUN_00cbfba0_Base*>(this)->FUN_00cbfba0();
    listenerVtable = &DAT_010cb1e4;
    primaryVtable = &DAT_010e7874;
    secondaryVtable = &DAT_010e7868;
    thirdVtable = &DAT_010e7854;
    fourthVtable = &DAT_010e7848;
    fifthVtable = &DAT_010e783c;
    listenerVtable = &DAT_010e781c;
    reference = value;
    if (value) {
        value->FUN_00c90510();
    }
    return this;
}
