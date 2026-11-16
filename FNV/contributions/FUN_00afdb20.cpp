int __cdecl FUN_00ec3bad(int value);
struct Marker { char b; };
struct FUN_00afdb20_Class {
    int unk00;
    int unk04;
    int m_08;
    int m_0c;
    void FUN_00afdb20();
};
void FUN_00afdb20_Class::FUN_00afdb20() {
    Marker c0 = {};
    Marker f0 = c0;
    int* ptr0 = &m_08;
    *ptr0 = FUN_00ec3bad(*ptr0);
    Marker e0 = {};
    Marker f1 = e0;
    int* ptr1 = &m_0c;
    *ptr1 = FUN_00ec3bad(*ptr1);
}
