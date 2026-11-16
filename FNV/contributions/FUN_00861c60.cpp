struct Collection_00861c60 {
    unsigned int FUN_0084e3a0();
    unsigned int* FUN_00877a30(unsigned int index);
    unsigned short FUN_00863d90(const unsigned int& value);
};
struct FUN_00861c60_shell {
    unsigned int unknown_0;
    unsigned int unknown_4;
    unsigned int unknown_8;
    unsigned int unknown_c;
    unsigned int unknown_10;
    unsigned int unknown_14;
    unsigned int unknown_18;
    unsigned int unknown_1c;
    unsigned int unknown_20;
    unsigned int unknown_24;
    unsigned int unknown_28;
    unsigned int unknown_2c;
    unsigned int unknown_30;
    unsigned int unknown_34;
    unsigned int unknown_38;
    unsigned int unknown_3c;
    unsigned int unknown_40;
    unsigned int unknown_44;
    unsigned int unknown_48;
    unsigned int unknown_4c;
    unsigned int unknown_50;
    unsigned int unknown_54;
    unsigned int unknown_58;
    unsigned int unknown_5c;
    unsigned int unknown_60;
    unsigned int unknown_64;
    unsigned int unknown_68;
    unsigned int unknown_6c;
    unsigned int unknown_70;
    unsigned int unknown_74;
    unsigned int unknown_78;
    Collection_00861c60* collection;
    unsigned short FUN_00861c60(unsigned int value);
};
unsigned short FUN_00861c60_shell::FUN_00861c60(unsigned int value)
{
    unsigned int count = collection->FUN_0084e3a0();
    for (unsigned int index = 0; index < count; ++index) {
        unsigned int currentValue = *collection->FUN_00877a30(index);
        if (currentValue == value)
            return static_cast<unsigned short>(index);
    }
    return collection->FUN_00863d90(value);
}