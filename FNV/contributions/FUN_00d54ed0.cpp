extern char* DAT_01268f90;
char* __cdecl FUN_00a7d330(char*);
struct FUN_00d54ed0_Obj {
    unsigned int unk00,unk04;
    unsigned short unk08,unk0A,unk0C,unk0E;
    void __thiscall FUN_0096ad30(unsigned int);
    void __thiscall FUN_0096ae90(unsigned int,char**);
};
struct FNVMemoryManager {
    void __thiscall FUN_00c851c0(FUN_00d54ed0_Obj*);
    void __thiscall FUN_00d54ed0(FUN_00d54ed0_Obj*);
};
void __thiscall FNVMemoryManager::FUN_00d54ed0(FUN_00d54ed0_Obj* object) {
    MemoryContextScope scope;
    this->FUN_00c851c0(object);
    char* result=FUN_00a7d330(DAT_01268f90);
    unsigned int n=object->unk0A;
    if(n>=object->unk08) object->FUN_0096ad30(object->unk0E+n);
    object->FUN_0096ae90(n,&result);
}