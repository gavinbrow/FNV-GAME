extern "C" __declspec(dllimport) int __stdcall QueryPerformanceFrequency(__int64* frequency);
extern double DAT_01017b70;
extern float DAT_011ac39c;

void __cdecl FUN_00aa4d50(void)
{
    __int64 frequency;
    QueryPerformanceFrequency(&frequency);
    DAT_011ac39c = static_cast<float>(frequency / DAT_01017b70);
}