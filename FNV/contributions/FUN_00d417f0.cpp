struct Slot {
    unsigned short id;
    unsigned short unk02;
    unsigned short unk04;
    unsigned short unk06;
};

struct Table {
    int unk00;
    int unk04;
    int unk08;
    unsigned short unk0C;
    unsigned char count;
    unsigned char unk0F;
    unsigned short unk10;
    Slot slots[1];
};

void __cdecl FUN_00d417f0(int a, Table* table, unsigned short value)
{
    int i;
    for (i = 0; i < table->count; i++) {
        if (table->slots[i].id == 0xffff) {
            table->slots[i].id = value;
            return;
        }
    }
}
