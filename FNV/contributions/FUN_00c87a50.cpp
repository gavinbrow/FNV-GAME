struct FUN_00c87a50_t {
    void* unk00;
    void* unk04;
    void* unk08;
    void* FUN_00c87a50();
};

void* FUN_00c87a50_t::FUN_00c87a50()
{
    if (this && unk08) {
        return *(void**)((char*)unk08 + 8);
    }
    return 0;
}