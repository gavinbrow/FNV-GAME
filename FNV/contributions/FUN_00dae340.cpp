void __fastcall FUN_00dae220(int unused, S_00dad640_Set* set);

void __cdecl FUN_00dae340(S_00dad640_Set* set, unsigned int index)
{
    unsigned int n = set->count;
    unsigned int last = n - 1;
    set->count = (unsigned char)last;
    unsigned int* dst = (unsigned int*)&set->entries[last];
    set->entries[index] = set->entries[last];
    unsigned int* src = (unsigned int*)&set->entries[n];
    int k = ((int)set->unk1 + (int)set->unk0 - 1) >> 1;
    unsigned int* baseDst = dst;
    for (; k >= 0; k--) {
        *dst = *(unsigned int*)((char*)src + ((char*)dst - (char*)baseDst));
        ++dst;
    }
    FUN_00dae220(k, set);
}
