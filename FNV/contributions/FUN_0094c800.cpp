struct MagicCasterShell
{
    bool __thiscall FUN_008c45e0(void* effect, void* context, int* failureCode, bool immediate);
    bool __thiscall FUN_0094c800(void* effect, void* context, int* errorOut, bool immediate);
};
bool __cdecl FUN_009526b0();

bool MagicCasterShell::FUN_0094c800(void* effect, void* context, int* errorOut, bool immediate)
{
    int failureCode = 0;
    bool succeeded = FUN_008c45e0(effect, context, &failureCode, immediate);
    if (errorOut != 0)
    {
        *errorOut = failureCode;
    }
    if (!succeeded && failureCode == 5)
    {
        return false;
    }
    else
    {
        return FUN_009526b0() ? true : succeeded;
    }
}
