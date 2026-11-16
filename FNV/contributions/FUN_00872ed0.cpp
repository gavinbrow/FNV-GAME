extern "C" __declspec(dllimport) void __stdcall DebugBreak();

struct FUN_00872ed0_shell
{
    void FUN_00872ed0(int param_1);
};

void FUN_00872ed0_shell::FUN_00872ed0(int param_1)
{
    DebugBreak();
}