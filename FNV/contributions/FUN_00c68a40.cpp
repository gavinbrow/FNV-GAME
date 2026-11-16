extern __declspec(thread) unsigned int g_havokThreadState[174];

struct ScopedHavokThreadMode {
    unsigned int oldMode;
    ScopedHavokThreadMode() : oldMode(g_havokThreadState[173]) {
        g_havokThreadState[173] = 16;
    }
    ~ScopedHavokThreadMode() {
        g_havokThreadState[173] = oldMode;
    }
};

struct FUN_00c674d0_Call {
    void __thiscall FUN_00c674d0(unsigned int resource, unsigned int count);
};

void FUN_00c68a40_Class::FUN_00c68a40() {
    ScopedHavokThreadMode threadMode;
    unsigned int& count = *reinterpret_cast<unsigned int*>(reinterpret_cast<char*>(this) + 0x30);
    if (count > 0) {
        if (count >= 3000)
            count = 3000;
        reinterpret_cast<FUN_00c674d0_Call*>(this)->FUN_00c674d0(
            *reinterpret_cast<unsigned int*>(reinterpret_cast<char*>(this) + 0x2c), count);
        count = 0;
    }
}