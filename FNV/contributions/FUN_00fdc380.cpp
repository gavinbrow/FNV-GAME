struct ReferenceCounted
{
    virtual ~ReferenceCounted();
    virtual void DeleteThis();
    volatile long referenceCount;
};

struct MyArchiveFile
{
    unsigned char archiveState[0x158];
    ReferenceCounted referenceOwner;
};

typedef long (__stdcall* InterlockedDecrementFunction)(volatile long* value);
extern InterlockedDecrementFunction DAT_00fdf1c4;
extern MyArchiveFile* DAT_011f8188;

// @fnv 0x00fdc380
void FUN_00fdc380()
{
    if (DAT_011f8188 != 0)
    {
        ReferenceCounted* owner = &DAT_011f8188->referenceOwner;
        if (DAT_00fdf1c4(&owner->referenceCount) == 0)
        {
            owner->DeleteThis();
        }
    }
}
