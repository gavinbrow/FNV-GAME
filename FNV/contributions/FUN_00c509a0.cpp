struct FUN_00c509a0_Class {
    void* __thiscall FUN_00c50f30(int);
    void __thiscall FUN_00c51700(void*);
    void __thiscall FUN_00c509a0(int);
};

extern "C" char DAT_010c2580;
extern "C" void __cdecl FUN_005b5e40(void*, int);

void FUN_00c509a0_Class::FUN_00c509a0(int a)
{
    int local1;
    int local2;
    int local3;
    void* p = this->FUN_00c50f30(a);

    if (p != 0) {
        this->FUN_00c51700(p);
    } else {
        FUN_005b5e40(&DAT_010c2580, a);
    }
}