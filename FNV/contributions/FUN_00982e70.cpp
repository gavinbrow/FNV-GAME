struct FUN_0044ddc0_Class { unsigned int FUN_0044ddc0(); };
struct FUN_00982e70_Temporary {
    int item;
    void* context;
    FUN_00982e70_Temporary* FUN_004b0680(int item, void* context);
};
struct FUN_00982e70_Class {
    void FUN_006db840(FUN_00982e70_Temporary* value);
    void FUN_00982e70(int item, void* context);
};
void FUN_00982e70_Class::FUN_00982e70(int item, void* context) {
    for (unsigned int index = 0; index < ((FUN_0044ddc0_Class*)this)->FUN_0044ddc0(); ++index) {
        int* entry = (int*)((FUN_00844160_shell*)this)->FUN_00844160(index);
        if (*entry == item) {
            return;
        }
    }
    if (!*((unsigned char*)this + 0x15)) {
        ((FUN_00982f10*)this)->Set((const char*)context + 0x70);
    }
    unsigned int flags = ((FUN_00982b90_class*)((char*)context + 0x70))->FUN_00982b90();
    *((unsigned int*)((char*)this + 0x10)) |= flags;
    {
        FUN_00982e70_Temporary temporary;
        FUN_006db840(temporary.FUN_004b0680(item, context));
    }
}