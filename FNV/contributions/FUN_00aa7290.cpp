struct MemoryPool {
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
    void FUN_0040fbf0(char*);
    void FUN_00aa7260();
};

extern MemoryPool* DAT_011f67b8[];
extern char DAT_010a2850;

void FUN_00aa7290(int idx)
{
    int pad0;
    int pad1;
    int* pool;
    if (DAT_011f67b8[idx]) {
        ((MemoryPool*)((char*)DAT_011f67b8[idx] + 0x20))->FUN_0040fbf0(&DAT_010a2850);
        DAT_011f67b8[idx]->FUN_00aa7260();
        pool = (int*)((char*)DAT_011f67b8[idx] + 0x20);
        pool[1] = pool[1] - 1;
        if (pool[1] == 0) {
            pool[0] = 0;
        }
    }
}