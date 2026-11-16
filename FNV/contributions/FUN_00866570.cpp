struct FUN_00866570_Input {
    unsigned char FUN_008a81c0();
    int FUN_008665b0();
    unsigned int FUN_0084e3a0();
    void* FUN_00726070();
};
struct FUN_00866570_Class : public FUN_008665d0_class {
    void FUN_00866570(FUN_00866570_Input* input);
};
void FUN_00866570_Class::FUN_00866570(FUN_00866570_Input* input) {
    FUN_008665d0(input->FUN_00726070(), input->FUN_0084e3a0(), input->FUN_008665b0(), input->FUN_008a81c0());
}