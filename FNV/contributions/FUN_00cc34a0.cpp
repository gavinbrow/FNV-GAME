#include <intrin.h>
struct PacketReader {
    void __thiscall FUN_00c868b0(void* context);
    void __thiscall FUN_00cc34a0(void* context);
};
typedef unsigned int* (__thiscall *GetPacketBlock)(PacketReader*, unsigned char*);
void __thiscall PacketReader::FUN_00cc34a0(void* context) {
    unsigned char format;
    volatile unsigned int* words = ((GetPacketBlock*)*(void**)this)[45](this, &format);
    if (((unsigned char*)context)[0x1E4] != 1) {
        words[4] = _byteswap_ulong(words[4]);
        words[5] = _byteswap_ulong(words[5]);
        words[6] = _byteswap_ulong(words[6]);
        words[7] = _byteswap_ulong(words[7]);
        words[8] = _byteswap_ulong(words[8]);
        words[9] = _byteswap_ulong(words[9]);
    }
    FUN_00c868b0(context);
    if (((unsigned char*)context)[0x1E4] != 1) {
        words[4] = _byteswap_ulong(words[4]);
        words[5] = _byteswap_ulong(words[5]);
        words[6] = _byteswap_ulong(words[6]);
        words[7] = _byteswap_ulong(words[7]);
        words[8] = _byteswap_ulong(words[8]);
        words[9] = _byteswap_ulong(words[9]);
    }
}