extern int DAT_0119bdec;
extern int DAT_0119bdc8;
void* __cdecl operator new(unsigned int size);
struct PackageRecord {
    int unk00;
    void* location04;
};
PackageRecord* __cdecl FUN_00ec43fb(int id, int flags, const int* name, const int* type, int option);
struct AmbushLocation {
    int unk00, unk04, unk08;
    AmbushLocation();
    void* FUN_00670b30(int release);
    void FUN_0067f4d0(void* source, int flags);
};
struct PackageOwner {
    int unk00;
    AmbushLocation* location04;
    void FUN_0067ae50(int id);
};
void PackageOwner::FUN_0067ae50(int id)
{
    PackageRecord* record = FUN_00ec43fb(id, 0, &DAT_0119bdec, &DAT_0119bdc8, 0);
    if (record)
    {
        if (location04)
        {
            AmbushLocation* oldLocation = location04;
            AmbushLocation* oldObject = oldLocation;
            oldObject ? oldObject->FUN_00670b30(1) : 0;
            location04 = 0;
        }
        if (record->location04)
        {
            location04 = new AmbushLocation();
            location04->FUN_0067f4d0(record->location04, 0);
        }
    }
}
