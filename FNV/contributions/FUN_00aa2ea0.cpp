struct NiBinaryStream {};
struct NiMemStream : NiBinaryStream
{
    void __thiscall FUN_00aa2d70(int iNumBytes);
};
void* __cdecl _NiMalloc(unsigned int size);
void __cdecl _NiFreeAlias(void* p);
void* __cdecl _memmove(void* dst, const void* src, unsigned int count);
unsigned int __fastcall FUN_00aa2dd0(NiMemStream* pThis, void* unused, const void* data, unsigned int numBytes);
int __cdecl FUN_00aa1de0(void*, unsigned int, void*, void*);
unsigned int __cdecl FUN_00aa2ec0(NiMemStream* pStream, void* pData, unsigned int uLen, void* pA, void* pB);
int __cdecl FUN_00aa1de0(void*, unsigned int, void*, void*);
struct S_00aa2dd0 { unsigned int __thiscall FUN_00aa2dd0(const void*, unsigned int); };
unsigned int __cdecl FUN_00aa2f20(NiMemStream* pStream, const void* pSrc, unsigned int uSize, void* pA, void* pB);

void __cdecl FUN_00aa2ea0(S_00aa2dd0* pThis, const void* pData, unsigned int uLen)
{
    pThis->FUN_00aa2dd0(pData, uLen);
}