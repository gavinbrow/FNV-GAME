struct FUN_00e60680_class {
    int unk00; int unk04; int unk08; int unk0c; int unk10;
    int capacity;
    int __thiscall FUN_00e60680(int index);
};
int __thiscall FUN_00e60680_class::FUN_00e60680(int index) {
    int next = index + 1;
    if (next < capacity) return next;
    return -1;
}
