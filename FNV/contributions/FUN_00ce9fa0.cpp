struct Item { int unk00[11]; int unk2c; };
struct Container { int unk00[2]; Item** items; int unk0c; int unk10; int unk14; int unk18; };
struct Counter { int unk00[12]; int unk30; };
extern "C" void __cdecl FUN_00d74b70(int, int, int);
void __cdecl FUN_00ce9fa0(Container* c, int value, Counter* counter) {
    for (int i = 0; i < c->unk0c; ++i)
        c->items[i]->unk2c = value;
    int count = ++counter->unk30;
    FUN_00d74b70(c->unk14, c->unk18, count);
}
