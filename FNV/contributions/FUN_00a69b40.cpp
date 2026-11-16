struct FUN_00a69b40_Class {
    void __thiscall FUN_00a69b40(int param_2);
};

void FUN_00a69b40_Class::FUN_00a69b40(int param_2)
{
    bool found = param_2 != 0;
    if (!found) {
        unsigned int count = *(unsigned short*)((char*)this + 0x26);
        unsigned int index = 1;
        if (index < count) {
            int* value = *(int**)((char*)this + 0x20) + 1;
            do {
                if (*value != 0) {
                    found = true;
                    break;
                }
                ++value;
                ++index;
            } while (index < count);
        }
    }

    if (found) {
        *(unsigned short*)((char*)this + 0x18) |= 1;
    } else {
        *(unsigned short*)((char*)this + 0x18) &= 0xfffe;
    }
}