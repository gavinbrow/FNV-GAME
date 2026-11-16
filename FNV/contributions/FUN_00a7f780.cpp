struct StringList {
    int unk00;
    void** items;
    unsigned short capacity;
    unsigned short count;
    unsigned short unk0C;
    unsigned short growth;
    void FUN_0096ad30(unsigned int);
    void FUN_0096ae90(unsigned int, void*);
};
struct Owner {
    int unk00; int unk04; int unk08; int unk0C;
    int unk10; int unk14; int unk18; int unk1C;
    int unk20; int unk24; int unk28;
    const char* name;
    void FUN_00a73e40(StringList*);
    void FUN_00a7f780(StringList*);
};
extern "C" const char* g_011f4aac;
extern const char str_0109deec[];
extern char* __cdecl FUN_00a7d330(const char*);
extern char* __cdecl FUN_00a7d510(const char*, const char*);
void Owner::FUN_00a7f780(StringList* list)
{
    char* text;
    unsigned int index;
    FUN_00a73e40(list);
    text = FUN_00a7d330(g_011f4aac);
    index = list->count;
    if (index >= list->capacity)
        list->FUN_0096ad30(list->growth + index);
    list->FUN_0096ae90(index, &text);
    text = FUN_00a7d510(str_0109deec, name);
    index = list->count;
    if (index >= list->capacity)
        list->FUN_0096ad30(list->growth + index);
    list->FUN_0096ae90(index, &text);
}