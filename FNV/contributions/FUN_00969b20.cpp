// FUN_00969b20 (zai_04): store the Win32 tick count in seconds into a global.
// Packet flags: /MT /Od /Oy- /GS /EHsc /Gy — unoptimized EBP frame.
// Prologue homes the thiscall "this" at [ebp-4] (never used afterwards),
// calls kernel32 GetTickCount through the import table, performs an unsigned
// division of the returned tick count by 1000, and stores the quotient to a
// global counter.

extern "C" __declspec(dllimport) unsigned long __stdcall GetTickCount(void);

extern unsigned int DAT_011e07b4;

struct TimeRefresh {
    void FUN_00969b20();
};

void TimeRefresh::FUN_00969b20() {
    DAT_011e07b4 = GetTickCount() / 1000;
}
