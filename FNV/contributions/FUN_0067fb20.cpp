int __cdecl FUN_004839c0(int value);

struct FUN_0067fb20_holder {
    signed char status;
    unsigned char flags1;
    unsigned short flags2;
    unsigned int metadata;
    int storedValue;
    void FUN_0067fb20();
};

void FUN_0067fb20_holder::FUN_0067fb20() {
    switch (status) {
    case 0:
    case 1:
    case 2:
    case 3:
    case 4: {
        int originalValue = storedValue;
        storedValue = FUN_004839c0(originalValue);
        break;
    }
    default:
        break;
    }
}