extern "C" __declspec(dllimport) int __stdcall CopyFileA(
    const char* lpExistingFileName,
    const char* lpNewFileName,
    unsigned char bFailIfExists);

int __cdecl FUN_00aff0d0(
    const char* lpExistingFileName,
    const char* lpNewFileName,
    unsigned char bFailIfExists)
{
    return CopyFileA(lpExistingFileName, lpNewFileName, bFailIfExists) ? 0 : 4;
}