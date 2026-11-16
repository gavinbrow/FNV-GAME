struct Point3 { float x; float y; float z; };
struct EntryList { void** entries; int count; };
struct Node
{
    int unk00;
    int unk04;
    int unk08;
    int unk0c;
    int unk10;
    int unk14;
    int unk18;
    int unk1c;
    int unk20;
    int unk24;
    int unk28;
    int unk2c;
    int unk30;
    int unk34;
    int unk38;
    int unk3c;
    int unk40;
    int unk44;
    EntryList entries;
};
struct Query
{
    int unk00;
    int unk04;
    int unk08;
    int unk0c;
    Point3 direction;
    int unk1c;
    Node* direct;
    int unk24;
    Node** groups;
    int groupCount;
};
struct BaseHelper { void FUN_00d68030(void* entry, int mode); };
int __cdecl FUN_00d679c0(float* direction);
struct Context { void FUN_00d68130(Query* query); };
void Context::FUN_00d68130(Query* query)
{
    int mode = FUN_00d679c0(&query->direction.x);
    for (int groupIndex = 0; groupIndex < query->groupCount; ++groupIndex)
    {
        EntryList* list = &query->groups[groupIndex]->entries;
        for (int entryIndex = 0; entryIndex < list->count; ++entryIndex)
            ((BaseHelper*)((char*)this - 0x2c))->FUN_00d68030(list->entries[entryIndex], mode);
    }
    EntryList* list = &query->direct->entries;
    for (int entryIndex = 0; entryIndex < list->count; ++entryIndex)
        ((BaseHelper*)((char*)this - 0x2c))->FUN_00d68030(list->entries[entryIndex], mode);
}
