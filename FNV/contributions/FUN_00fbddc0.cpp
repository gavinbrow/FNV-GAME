struct RegistrationNode
{
    void* unknown0;
    void* unknown4;
    RegistrationNode* next;
};

extern RegistrationNode DAT_011b1c24;
extern RegistrationNode* DAT_01268790;

// @fnv 0x00fbddc0
void FUN_00fbddc0()
{
    DAT_011b1c24.next = DAT_01268790;
    DAT_01268790 = &DAT_011b1c24;
}
