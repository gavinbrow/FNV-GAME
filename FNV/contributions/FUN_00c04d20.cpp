#include "h_74712c1d3c73.h"

extern "C" void __cdecl FUN_00ba4080();

extern unsigned char DAT_010bcae8;
extern char str_011ae684;
extern unsigned char DAT_011ae694;

struct FUN_00c04d20_class {
    void* m_vtbl;
    unsigned char pad04[0x54];
    unsigned char m_58;
    char* m_5c;
    unsigned char* m_60;
    unsigned int m_64;

    FUN_00c04d20_class();
};

FUN_00c04d20_class::FUN_00c04d20_class()
{
    FUN_00ba4080();
    m_58 = 0;
    m_64 = 0;
    m_vtbl = &DAT_010bcae8;
    m_5c = &str_011ae684;
    m_60 = &DAT_011ae694;
}