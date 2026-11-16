
struct NumericArray {
    unsigned int FUN_0084e3a0();
    unsigned int* FUN_00877a30(unsigned int index);
    unsigned int FUN_00863d90(const unsigned int& value);
};
struct FUN_00861b70_Class {
    unsigned int FUN_00861b70(unsigned int value);
};
unsigned int FUN_00861b70_Class::FUN_00861b70(unsigned int value) {
    if (::g_dataHandler->IsFormIDCreated(value)) {
        return value;
    }
    unsigned int count = (*(NumericArray**)((char*)this + 0x78))->FUN_0084e3a0();
    for (unsigned int index = 0; index < count; ++index) {
        unsigned int current = *(*(NumericArray**)((char*)this + 0x78))->FUN_00877a30(index);
        if (current == value) {
            return index;
        }
    }
    return (*(NumericArray**)((char*)this + 0x78))->FUN_00863d90(value);
}
