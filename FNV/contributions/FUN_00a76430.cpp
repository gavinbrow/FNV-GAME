#include "h_2c784344dbed.h"

class NiStream {
public:
    void* m_vtable;
    void* m_pBase;
    unsigned short m_usMaxSize;
    unsigned short m_usSize;
    unsigned short m_usESize;
    unsigned short m_usGrowBy;
    void FUN_0096ad30(unsigned int size);
    void FUN_0096ae90(unsigned int index, const unsigned int* value);
};

extern "C" const NiRTTI DAT_011f4a70;
extern "C" const char str_0109d984[];
extern "C" const char str_0109d970[];
extern "C" const char str_0109d960[];
unsigned int FUN_00a7d330(const NiRTTI*);
unsigned int FUN_00a7d490(const void*, unsigned short);
unsigned int FUN_00a7d5a0(const void*, const void*);

struct NiTriStripsSerializer : NiTriStripsData {
    void FUN_00a76430(NiStream& stream);
    void FUN_00a8aab0(NiStream& stream);
};

void NiTriStripsSerializer::FUN_00a76430(NiStream& stream)
{
    FUN_00a8aab0(stream);
    unsigned int entry = FUN_00a7d330(*reinterpret_cast<const NiRTTI* const*>(&DAT_011f4a70));
    unsigned int count = stream.m_usSize;
    if (count >= (unsigned int)stream.m_usMaxSize) {
        stream.FUN_0096ad30(count + stream.m_usGrowBy);
    }
    stream.FUN_0096ae90(count, &entry);

    entry = FUN_00a7d490(str_0109d984, m_usStrips);
    count = stream.m_usSize;
    if (count >= (unsigned int)stream.m_usMaxSize) {
        stream.FUN_0096ad30(count + stream.m_usGrowBy);
    }
    stream.FUN_0096ae90(count, &entry);

    entry = FUN_00a7d5a0(str_0109d970, m_pusStripLengths);
    count = stream.m_usSize;
    if (count >= (unsigned int)stream.m_usMaxSize) {
        stream.FUN_0096ad30(count + stream.m_usGrowBy);
    }
    stream.FUN_0096ae90(count, &entry);

    entry = FUN_00a7d5a0(str_0109d960, m_pusStripLists);
    count = stream.m_usSize;
    if (count >= (unsigned int)stream.m_usMaxSize) {
        stream.FUN_0096ad30(count + stream.m_usGrowBy);
    }
    stream.FUN_0096ae90(count, &entry);
}