struct State {
    int unk00; int unk04; int unk08; int unk0c; int unk10; int unk14;
    int unk18; int unk1c; int unk20; int unk24; int unk28;
    float threshold; float upper; int count;
};
extern State* DAT_011f8bf4;
struct GlobalObject_00b3f100 { float FUN_00b3f130(float, float); };
extern GlobalObject_00b3f100 g_011f8c05;
struct Link { Link* next; float value; };
struct Owner { bool FUN_00b13b50(Link* link, float input); };
bool Owner::FUN_00b13b50(Link* link, float input) {
    bool result = false;
    {
        float value = input;
        if (DAT_011f8bf4->count == 0) {
            int current = 1;
            Link* index = link;
            Link* next;
            while (index != 0 && (next = index->next) != 0 && current < DAT_011f8bf4->count) {
                index = index->next;
                ++current;
            }
            if (index != 0)
                value = index->value;
        }
        if (value > DAT_011f8bf4->threshold) {
            if (g_011f8c05.FUN_00b3f130(0.0f, 1.0f) <= DAT_011f8bf4->upper)
                result = true;
        }
    }
    return result;
}
