extern float DAT_0104da48;
extern unsigned char DAT_010ce7fc;

struct FUN_00d44f90_Data
{
    unsigned int descriptor;
    float bound;
    unsigned int value;
};

struct FUN_00d44f90_Class
{
    void FUN_00d444f0(void* first, void* second, void* third, FUN_00d44f90_Data* data);
    void FUN_00d44f90(void* first, void* second, void* third, unsigned int value);
};

void FUN_00d44f90_Class::FUN_00d44f90(void* first, void* second, void* third, unsigned int value)
{
    FUN_00d44f90_Data data;
    data.value = value;
    data.bound = DAT_0104da48;
    data.descriptor = (unsigned int)&DAT_010ce7fc;
    FUN_00d444f0(second, first, third, &data);
}

