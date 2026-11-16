
bool __cdecl FUN_00401500();
void __cdecl FUN_00485990(unsigned int record, const void* data, unsigned int bytes);
struct Record {
    unsigned char field0;
    unsigned char field1;
    unsigned char field2;
    void __thiscall FUN_00483710();
};
struct FUN_005e9620_class {
    unsigned int unk00;
    unsigned char unk04;
    unsigned char unk05;
    void __thiscall FUN_005e9620(unsigned char value);
};
void __thiscall FUN_005e9620_class::FUN_005e9620(unsigned char value) {
    Record data;
    data.field2 = unk05;
    data.field1 = unk04;
    data.field0 = value;
    if (FUN_00401500()) {
        data.FUN_00483710();
    }
    FUN_00485990(0x454b5250, &data, 3);
    if (FUN_00401500()) {
        data.FUN_00483710();
    }
}
