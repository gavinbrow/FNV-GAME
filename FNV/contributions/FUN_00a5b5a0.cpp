#include <intrin.h>

extern "C" volatile unsigned long _tls_index;
extern unsigned int DAT_011f42c8;
extern unsigned int DAT_011f42c4;

struct ThreadedTableEntry
{
    void __thiscall FUN_00a5b4b0(const char** key);
};

struct ThreadedTable
{
    unsigned int __thiscall FUN_00a5b270(const char* key, unsigned int flags);
    void __thiscall FUN_00a5b5a0(const char** key, unsigned int flags);
};

void __thiscall ThreadedTable::FUN_00a5b5a0(const char** key, unsigned int flags)
{
    unsigned int tlsIndex = _tls_index;
    unsigned char* threadData =
        reinterpret_cast<unsigned char**>(__readfsdword(0x2c))[tlsIndex];
    const unsigned int previousMode =
        *reinterpret_cast<unsigned int*>(threadData + 0x2b4);
    *reinterpret_cast<unsigned int*>(threadData + 0x2b4) = 8;

    unsigned int index = FUN_00a5b270(*key, flags);
    CRITICAL_SECTION_STUB* criticalSection =
        reinterpret_cast<CRITICAL_SECTION_STUB*>(reinterpret_cast<char*>(this) + 0x2080);
    EnterCriticalSection(criticalSection);

    const unsigned int entryOffset = index << 4;
    if (*reinterpret_cast<short*>(
            reinterpret_cast<char*>(this) + entryOffset + 0x0c) != 0)
        ++DAT_011f42c8;

    reinterpret_cast<ThreadedTableEntry*>(
        reinterpret_cast<char*>(this) + entryOffset)->FUN_00a5b4b0(key);
    ++DAT_011f42c4;
    LeaveCriticalSection(criticalSection);
    *reinterpret_cast<unsigned int*>(threadData + 0x2b4) = previousMode;
}