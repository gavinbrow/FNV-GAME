struct PriorityKey {
    unsigned int unk00;
    unsigned int unk04;
    unsigned int unk08;
    unsigned int unk0c;
    unsigned __int64 key;
    void __thiscall FUN_004405d0(unsigned char priority);
};

void PriorityKey::FUN_004405d0(unsigned char priority) {
    key = (key & 0xffffffffff00ffffui64) +
          ((__int64)priority << 16);
}