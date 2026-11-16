extern "C" __declspec(dllimport) int __stdcall VirtualFree(void*, unsigned int, unsigned int);
struct FUN_00aa6680_class {
    unsigned int unk00;
    void* allocation;
    void __thiscall FUN_00aa6680();
};
void FUN_00aa6680_class::FUN_00aa6680()
{
    VirtualFree(allocation, 0, 0x8000);
}
