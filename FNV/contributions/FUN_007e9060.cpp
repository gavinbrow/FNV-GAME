struct MenuValueField { char* __thiscall FUN_00408da0(); };
struct MenuStringReader {
    virtual void Read0(); virtual void Read1(); virtual void Read2(); virtual void Read3();
    virtual char* ReadString(int unused, unsigned int recordType);
};
struct MenuRecord {
    int unk00; int unk04; int unk08; int unk0c; int unk10; int unk14;
    MenuValueField value18; int unk1c; int unk20; MenuStringReader record24;
};
struct MenuTileField {
    void __thiscall FUN_00a01350(unsigned int property, char* text, int forceUpdate);
    void __thiscall FUN_00700320(unsigned int property, int matched);
    void __thiscall FUN_00a012d0(void* value, float fade, int flags);
};
extern char str_010702d8[];
extern "C" void* __cdecl FUN_00a00940(const char* descriptor, int index);
struct TutorialMenuView {
    int unk00; int unk04; int unk08; int unk0c; int unk10; int unk14; int unk18; int unk1c;
    int unk20; int unk24; MenuTileField* text28; int unk2c; int unk30; int unk34;
    MenuTileField* text38; int unk3c; MenuTileField* text40;
    void __thiscall FUN_007e9060(MenuRecord* record);
};
void TutorialMenuView::FUN_007e9060(MenuRecord* record)
{
    char* description;
    if (!record) return;
    if (text38 != 0) {
        text38->FUN_00a01350(0xFC4, record->value18.FUN_00408da0(), 1);
    }
    if (text28 != 0) {
        description = record->record24.ReadString(0, 0x43534544);
        if (description != 0) {
            text28->FUN_00700320(0xFBE, description[0] == '<');
            text28->FUN_00a01350(0xFC4, description, 1);
        }
    }
    if (text40 != 0) {
        text40->FUN_00a012d0(FUN_00a00940(str_010702d8, -1), 0.0f, 0);
    }
}
