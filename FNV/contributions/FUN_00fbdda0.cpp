struct RegistrationNode
{
    void* unknown0;
    void* unknown4;
    RegistrationNode* next;
};

extern RegistrationNode DAT_011b1c14;
extern RegistrationNode* DAT_01268790;

// @fnv 0x00fbdda0
void FUN_00fbdda0()
{
    DAT_011b1c14.next = DAT_01268790;
    DAT_01268790 = &DAT_011b1c14;
}
