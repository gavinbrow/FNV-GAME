// Uses pack declarations already in scope: AVOwner_007927a0, Player_007927a0,
// g_thePlayer, Glob, DAT_011da2c8 (extern Glob*). GlobView below adds named
// fields at the offsets this function accesses; the pack's Glob stand-in cannot
// be redefined, so the global pointer is viewed through this layout.
struct GlobView_00795580 {
    char _pad[0x48];
    int m48;
    int m4c;
};

struct Entry_00795580 {
    void FUN_00450f90();
};
struct List_00795580 {
    Entry_00795580* FUN_00559450(int flag);
};
struct Menu_00795580 {
    char _0[8];
    List_00795580 m8;
    char _1[0x1b];
    int m24;
};

unsigned char FUN_004b71d0();

void __cdecl FUN_00795580(Menu_00795580* p) {
    int iVar1 = p->m24;
    if (iVar1 != -1) {
        if (g_thePlayer->avOwner.GetValue(iVar1) > 1)
            p->m8.FUN_00559450(0)->FUN_00450f90();
        else
            p->m8.FUN_00559450(1)->FUN_00450f90();
        if (FUN_004b71d0() && ((GlobView_00795580*)DAT_011da2c8)->m48 == 8
            && iVar1 != ((GlobView_00795580*)DAT_011da2c8)->m4c + 4)
            p->m8.FUN_00559450(1)->FUN_00450f90();
    }
}
