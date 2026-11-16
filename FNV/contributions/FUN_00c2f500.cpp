extern float DAT_011f426c;
extern float DAT_011f4270;
extern float DAT_011f4274;
extern float DAT_011a946c;
extern float DAT_011a9470;
extern float DAT_011a9474;
struct TmpVec3
{
    int x;
    int y;
    int z;
    void __thiscall FUN_004a0c10();
};
void AirTmp::FUN_00c2f500(void* param)
{
    int* p = (int*)param;
    int* a = (int*)((char*)this + 0x40);
    a[0] = p[0];
    a[1] = p[1];
    a[2] = p[2];
    TmpVec3* v = (TmpVec3*)((char*)this + 0x4c);
    v->x = p[0];
    v->y = p[1];
    v->z = p[2];
    v->FUN_004a0c10();
    if (*(float*)&v->x == DAT_011f426c && *(float*)&v->y == DAT_011f4270 && *(float*)&v->z == DAT_011f4274)
    {
        v->x = *(int*)&DAT_011a946c;
        v->y = *(int*)&DAT_011a9470;
        v->z = *(int*)&DAT_011a9474;
    }
}

