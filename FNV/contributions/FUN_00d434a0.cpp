struct CallData { void* descriptor; float bound; unsigned int value; };
extern unsigned char DAT_010ce7fc;
extern float DAT_0104da48;
struct Wrapper {
    void FUN_00d42de0(void*, void*, unsigned int, CallData*);
    void FUN_00d434a0(void*, void*, unsigned int, unsigned int);
};
void Wrapper::FUN_00d434a0(void* first, void* second, unsigned int third, unsigned int fourth) {
    CallData data;
    data.value = fourth;
    data.bound = DAT_0104da48;
    data.descriptor = &DAT_010ce7fc;
    FUN_00d42de0(second, first, third, &data);
}
