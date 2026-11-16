extern "C" char str_01070244[];
int __cdecl FUN_00a00940(const char* name, int fallback);
struct Tile_721c60 {
    bool __thiscall FUN_00a01230(int trait);
};
struct Class_721c60 {
    int unk00;
    int unk04;
    int unk08;
    Tile_721c60* m_pScrollBar;
    bool __thiscall FUN_00724a00();
};
bool __thiscall Class_721c60::FUN_00724a00()
{
    static int enabledTrait = FUN_00a00940(str_01070244, -1);
    return m_pScrollBar && m_pScrollBar->FUN_00a01230(enabledTrait);
}