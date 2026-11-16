extern char DAT_01029994;
extern void __fastcall FUN_0050e9f0(void*);

struct FUN_0050f7f0_shell
{
    void FUN_0050f7f0();
};

void FUN_0050f7f0_shell::FUN_0050f7f0()
{
    *reinterpret_cast<void**>(this) = reinterpret_cast<void*>(&DAT_01029994);
    FUN_0050e9f0(this);
}