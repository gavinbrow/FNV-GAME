extern void __cdecl FUN_00ec7c56();

struct FUN_00b10490_class {
    int first;
    int second;
    bool __thiscall FUN_00b10490(const FUN_00b10490_class* rhs);
};

bool __thiscall FUN_00b10490_class::FUN_00b10490(const FUN_00b10490_class* rhs) {
    if (!((unsigned char)(int)(first != 0) && (unsigned char)(int)(first == rhs->first))) {
        FUN_00ec7c56();
    }
    do {
    } while (false);
    return !((unsigned char)(int)(second == rhs->second));
}
