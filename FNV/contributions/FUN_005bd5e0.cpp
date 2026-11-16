extern "C" bool __cdecl FUN_005accb0(int,int,int,int,int,int,int,void*);
extern void __cdecl FUN_00703da0();
struct Player5bd { void __thiscall CenterOnCell(void* cell, int flag); };
extern Player5bd* g_thePlayer;
bool __cdecl FUN_005bd5e0(int a,int b,int c,int d,int e,int f,int unusedArg,int h) {
    char cellText[0x200];
    if (!FUN_005accb0(a,b,h,c,d,e,f,cellText))
        return false;
    FUN_00703da0();
    g_thePlayer->CenterOnCell(cellText,0);
    return true;
}
