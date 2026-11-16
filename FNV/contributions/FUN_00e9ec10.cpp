struct MatchList
{
    int unk00;
    int unk04;
    void** entries;
    unsigned short unk0c;
    unsigned short count;
    unsigned short unk10;
    unsigned short unk12;
    unsigned int foundIndex;
};
bool __cdecl FUN_00e9ca50(float value, void* item, unsigned int arg3, unsigned int arg4, unsigned int arg5, unsigned int arg6, unsigned int arg7, unsigned int arg8, unsigned int arg9, unsigned int arg10, unsigned int arg11, unsigned int arg12);
bool __cdecl FUN_00e9ec10(float value, MatchList* list, unsigned int arg3, unsigned int arg4, unsigned int arg5, unsigned int arg6, unsigned int arg7, unsigned int arg8, unsigned int arg9, unsigned int arg10, unsigned int arg11, unsigned int arg12)
{
    for (unsigned int i = 0; i < list->count; ++i)
    {
        void* item = list->entries[i];
        if (FUN_00e9ca50(value, item, arg3, arg4, arg5, arg6, arg7, arg8, arg9, arg10, arg11, arg12))
        {
            list->foundIndex = i;
            return true;
        }
    }
    return false;
}
