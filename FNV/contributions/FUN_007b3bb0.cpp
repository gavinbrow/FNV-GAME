struct TempString_007b3bb0 {
    void* unk00; void* unk04;
    TempString_007b3bb0(); ~TempString_007b3bb0();
    const char* FUN_00559450(const char* format, unsigned int value);
};
extern const char DAT_01075b28[];
extern const char DAT_01075b10[];
void __cdecl FUN_00406f60(TempString_007b3bb0* result, const char* format, const char* input, int limit);
struct SelectedOption_007b3bb0 {
    int unk00; int unk04; int unk08; unsigned int value0c; int unk10; TGF* pTGF;
};
struct Menu_007b3bb0 {
    int unk00; int unk04; int unk08; int unk0c; int unk10; TGF* pTGF;
    int FUN_007b4650(const char* text, int flags);
    int FUN_007b3bb0(const char* input, SelectedOption_007b3bb0* selected);
};
int Menu_007b3bb0::FUN_007b3bb0(const char* input, SelectedOption_007b3bb0* selected) {
    TempString_007b3bb0 text;
    FUN_00406f60(&text, DAT_01075b28, input, 0x3e);
    selected->value0c = (unsigned int)pTGF->GetFloat(0x1004);
    return FUN_007b4650(text.FUN_00559450(DAT_01075b10, (unsigned int)selected->pTGF->GetFloat(0x1004)), 0);
}