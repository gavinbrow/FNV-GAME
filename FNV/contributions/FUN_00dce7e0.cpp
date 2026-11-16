void __cdecl FUN_00dcea10(int, int, int, void*);
int __cdecl FUN_00c85750();
struct FUN_00dce7e0_local {
    int unk00; int unk04; int unk08; int unk0c;
    void __thiscall FUN_00dce840(void*, void*);
    void __thiscall FUN_00cb1a90(int);
    void __thiscall FUN_00a29680();
};
void __cdecl FUN_00dce7e0(int a, int b, int* p, int d)
{
    FUN_00dce7e0_local local;
    int value = *(int*)(*p + 8);
    local.FUN_00dce840(p, (void*)d);
    FUN_00dcea10(a, b, value, &local);
    int object = FUN_00c85750();
    ((FUN_00dce7e0_local*)((char*)&local + 4))->FUN_00cb1a90(*(int*)(object + 0x10));
    ((FUN_00dce7e0_local*)((char*)&local + 4))->FUN_00a29680();
}
