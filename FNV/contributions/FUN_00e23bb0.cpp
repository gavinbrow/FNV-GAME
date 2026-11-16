struct Entry {
    Entry* next;
    int unk04;
    int unk08;
    int unk0c;
    int unk10;
    unsigned int links[3];
    unsigned int flags;
};

struct Ref {
    unsigned int value;
    unsigned int extra;
};

struct Tally {
    int good;
    int bad;
};

struct Scanner {
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
    Entry* head;
    bool FUN_00e23bb0();
    int Visit(Ref* ref);
};

bool Scanner::FUN_00e23bb0()
{
    Tally t;
    t.good = 0;
    t.bad = 0;
    for (Entry* e = head; e; e = e->next) {
        if (e->flags & 0x10) {
            Ref ref;
            Ref m;
            int i = 0;
            ref.value = (unsigned int)e;
            for (; i < 3; i++) {
                ref.extra = i;
                unsigned int link = e->links[i];
                if (link & 0xfffffffc) {
                    m.extra = link & 3;
                    m.value = e->links[i] & 0xfffffffc;
                    if (Visit(&ref)) {
                        t.good++;
                    } else if (Visit(&m)) {
                        t.bad++;
                    }
                } else {
                    if (Visit(&ref)) {
                        t.good++;
                    } else {
                        t.bad++;
                    }
                }
            }
        }
    }
    return t.good > t.bad;
}
