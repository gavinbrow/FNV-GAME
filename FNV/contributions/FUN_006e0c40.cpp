
struct LoadBufferEx {
    unsigned int __thiscall FUN_00865f20();
    void __thiscall FUN_00865db0(unsigned int key, unsigned int flags);
    void __thiscall FUN_00865ff0(unsigned int writtenCount, unsigned int offset);
    void __thiscall FUN_00865e50(void* value, unsigned int size, unsigned int flags);
};
struct PathingCell {
    void __thiscall FUN_006dffc0(LoadBufferEx* buffer);
};
struct CellMap {
    unsigned int unk00;
    unsigned int unk04;
    unsigned int unk08;
    unsigned int unk0c;
    void* __thiscall FUN_004b9ba0();
    void __thiscall FUN_006b7f20(void*& position, unsigned int& key, PathingCell*& value);
};
struct CellData {
    virtual void LoadGame(LoadBufferEx* buffer);
    unsigned int unk04, unk08, unk0c, unk10, unk14;
    unsigned int unk18, unk1c, unk20, unk24;
};
struct PathingGrid {
    unsigned int unk00;
    unsigned int unk04;
    CellMap cells;
    unsigned int unk18;
    CellData metadata;
    unsigned int unk44;
    unsigned int unk48;

    void FUN_006e0c40(LoadBufferEx* buffer);
};
void PathingGrid::FUN_006e0c40(LoadBufferEx* buffer)
{
    unsigned int writtenCount = 0;
    unsigned int startOffset = buffer->FUN_00865f20();
    void* position = cells.FUN_004b9ba0();
    while (position != 0) {
        PathingCell* cell = 0;
        unsigned int key;
        cells.FUN_006b7f20(position, key, cell);
        if (cell != 0) {
            buffer->FUN_00865db0(key, 0);
            cell->FUN_006dffc0(buffer);
            writtenCount++;
        }
    }
    buffer->FUN_00865ff0(writtenCount, startOffset);
    buffer->FUN_00865e50(&unk18, 4, 0);
    buffer->FUN_00865e50(&unk44, 4, 0);
    buffer->FUN_00865e50(&unk48, 4, 0);
    metadata.LoadGame(buffer);
}
