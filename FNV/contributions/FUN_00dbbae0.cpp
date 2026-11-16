
struct FUN_00d871a0_Data {
    int memberData;
    int key;
    void FUN_00d871a0(void* value, int argument);
    const char* FUN_00d871e0(const int* argument);
};
struct FUN_00dbbae0_Class {
    int unk00;
    int unk04;
    int unk08;
    int unk0C;
    int FUN_00dbbae0(int argument);
};
int FUN_00dbbae0_Class::FUN_00dbbae0(int argument) {
    FUN_00d871a0_Data lookup;
    lookup.FUN_00d871a0(&unk0C, argument);
    return *lookup.FUN_00d871e0(&argument) != 0;
}
