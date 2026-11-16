struct FUN_00d07180_s {
    int unk00;
    int unk04;
    int unk08;
    int unk0c;
    int unk10;
    int unk14;
    int FUN_00d07180(FUN_00d07180_s* other);
};
int FUN_00d07180_s::FUN_00d07180(FUN_00d07180_s* other) {
    int incoming = other->unk08;
    int current = unk08;
    if (current > incoming)
        incoming = current;
    unk08 = incoming;
    unk0c += other->unk0c;
    unk10 += other->unk10;
    int last = other->unk14;
    unk14 += last;
    return last;
}
