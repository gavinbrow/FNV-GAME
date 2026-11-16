struct FUN_00e488a0_data {
    int unknown00;
    int unknown04;
    int unknown08;
    int unknown0c;
    int unknown10;
    int unknown14;
    int unknown18;
    int unknown1c;
    int value20;
};

struct FUN_00e488a0_object {
    virtual void unused0();
    virtual void unused1();
    virtual void unused2();
    virtual void unused3();
    virtual int getValue(int input);
};

struct FUN_00e488a0_class {
    int* FUN_00e488a0(int* value, FUN_00e488a0_data* data, int unused, FUN_00e488a0_object* object, int input);
};

int* FUN_00e488a0_class::FUN_00e488a0(int* value, FUN_00e488a0_data* data, int unused, FUN_00e488a0_object* object, int input) {
    int result = object->getValue(input);
    FUN_00e48830_class* owner = reinterpret_cast<FUN_00e48830_class*>(reinterpret_cast<char*>(this) - 16);
    owner->FUN_00e48830(value, data->value20, result);
    return value;
}