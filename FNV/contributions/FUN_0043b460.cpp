extern "C" long __stdcall InterlockedCompareExchange(long volatile* Destination, long Exchange, long Comparand);

typedef long (__stdcall *InterlockedCompareExchange_t)(long volatile*, long, long);

InterlockedCompareExchange_t DAT_00fdf1bc = InterlockedCompareExchange;

void __cdecl FUN_0043b460(void* pDest, void* pSrc, unsigned int n)
{
    DAT_00fdf1bc(static_cast<long volatile*>(pDest), n, reinterpret_cast<long>(pSrc));
}