#include <windows.h>

extern const char* DAT_0109b220;
const char* __cdecl FUN_00a5b690(const char* text);

class NiFixedString
{
public:
    const char* m_data;

    NiFixedString& operator=(const char* text)
    {
        if (m_data != text)
        {
            const char* previous = m_data;
            m_data = FUN_00a5b690(text);
            if (previous != DAT_0109b220)
                InterlockedDecrement(
                    reinterpret_cast<volatile LONG*>(
                        const_cast<char*>(previous) - 8));
        }
        return *this;
    }

    NiFixedString& operator=(const NiFixedString& other)
    {
        if (m_data != other.m_data)
        {
            const char* replacement = other.m_data;
            if (replacement != DAT_0109b220)
                InterlockedIncrement(
                    reinterpret_cast<volatile LONG*>(
                        const_cast<char*>(replacement) - 8));
            if (m_data != DAT_0109b220)
                InterlockedDecrement(
                    reinterpret_cast<volatile LONG*>(
                        const_cast<char*>(m_data) - 8));
            m_data = replacement;
        }
        return *this;
    }
};

struct BinaryStream
{
    unsigned int unk00;
    unsigned int bytesRead;
    unsigned int (__cdecl *read)(BinaryStream*, void*, unsigned int,
                                 const unsigned int*, unsigned int);

    void Read(void* buffer, unsigned int bytes)
    {
        unsigned int componentSize = bytes;
        bytesRead += read(this, buffer, bytes, &componentSize, 1);
    }
};

class NiObject;
class FUN_00a64df0_Stream
{
public:
    virtual void vfn_00();
    virtual void vfn_04();
    virtual void vfn_08();
    virtual void vfn_0c();
    virtual void vfn_10();
    virtual void vfn_14();
    virtual void vfn_18();
    virtual void vfn_1c();
    virtual void vfn_20();
    virtual void vfn_24();
    virtual void vfn_28();
    virtual unsigned int vfn_2c(const NiObject* object);
    void SaveLinkID(const NiObject* object);
    unsigned int unk004;
    unsigned int unk008;
    unsigned int unk00c;
    unsigned int unk010;
    unsigned int unk014;
    unsigned int unk018;
    unsigned int unk01c;
    unsigned int unk020;
    unsigned int unk024;
    unsigned int unk028;
    unsigned int unk02c;
    unsigned int unk030;
    unsigned int unk034;
    unsigned int unk038;
    unsigned int unk03c;
    unsigned int unk040;
    unsigned int unk044;
    unsigned int unk048;
    unsigned int unk04c;
    unsigned int unk050;
    unsigned int unk054;
    unsigned int unk058;
    unsigned int unk05c;
    unsigned int unk060;
    unsigned int unk064;
    unsigned int unk068;
    unsigned int unk06c;
    unsigned int unk070;
    unsigned int unk074;
    unsigned int unk078;
    unsigned int unk07c;
    unsigned int unk080;
    unsigned int unk084;
    unsigned int unk088;
    unsigned int unk08c;
    unsigned int unk090;
    unsigned int unk094;
    unsigned int unk098;
    unsigned int unk09c;
    unsigned int unk0a0;
    unsigned int unk0a4;
    unsigned int unk0a8;
    unsigned int unk0ac;
    unsigned int unk0b0;
    unsigned int unk0b4;
    unsigned int unk0b8;
    unsigned int unk0bc;
    unsigned int unk0c0;
    unsigned int unk0c4;
    unsigned int unk0c8;
    unsigned int unk0cc;
    unsigned int unk0d0;
    unsigned int unk0d4;
    unsigned int unk0d8;
    unsigned int unk0dc;
    unsigned int unk0e0;
    unsigned int unk0e4;
    unsigned int unk0e8;
    unsigned int unk0ec;
    unsigned int unk0f0;
    unsigned int unk0f4;
    unsigned int unk0f8;
    unsigned int unk0fc;
    unsigned int unk100;
    unsigned int unk104;
    unsigned int unk108;
    unsigned int unk10c;
    unsigned int unk110;
    unsigned int unk114;
    unsigned int unk118;
    unsigned int unk11c;
    unsigned int unk120;
    unsigned int unk124;
    unsigned int unk128;
    unsigned int unk12c;
    unsigned int unk130;
    unsigned int unk134;
    unsigned int unk138;
    unsigned int unk13c;
    unsigned int unk140;
    unsigned int unk144;
    unsigned int unk148;
    unsigned int unk14c;
    unsigned int unk150;
    unsigned int unk154;
    unsigned int unk158;
    unsigned int unk15c;
    unsigned int unk160;
    unsigned int unk164;
    unsigned int unk168;
    unsigned int unk16c;
    unsigned int unk170;
    unsigned int unk174;
    unsigned int unk178;
    unsigned int unk17c;
    unsigned int unk180;
    unsigned int unk184;
    unsigned int unk188;
    unsigned int unk18c;
    unsigned int unk190;
    unsigned int unk194;
    unsigned int unk198;
    unsigned int unk19c;
    unsigned int unk1a0;
    unsigned int unk1a4;
    unsigned int unk1a8;
    unsigned int unk1ac;
    unsigned int unk1b0;
    unsigned int unk1b4;
    unsigned int unk1b8;
    unsigned int unk1bc;
    unsigned int unk1c0;
    unsigned int unk1c4;
    unsigned int unk1c8;
    unsigned int unk1cc;
    unsigned int unk1d0;
    unsigned int unk1d4;
    unsigned int unk1d8;
    unsigned int unk1dc;
    unsigned int unk1e0;
    unsigned int unk1e4;
    unsigned int unk1e8;
    unsigned int unk1ec;
    unsigned int unk1f0;
    unsigned int unk1f4;
    unsigned int unk1f8;
    unsigned int unk1fc;
    unsigned int unk200;
    unsigned int unk204;
    unsigned int unk208;
    unsigned int unk20c;
    unsigned int unk210;
    unsigned int unk214;
    unsigned int unk218;
    unsigned int unk21c;
    unsigned int unk220;
    unsigned int unk224;
    unsigned int unk228;
    unsigned int unk22c;
    unsigned int unk230;
    unsigned int unk234;
    NiFixedString* strings;
    unsigned int unk23c;
    unsigned int unk240;
    unsigned int unk244;
    unsigned int unk248;
    BinaryStream* input;
    void __thiscall FUN_00a64df0(NiFixedString& result);
};

void FUN_00a64df0_Stream::FUN_00a64df0(NiFixedString& result)
{
    unsigned int id;
    input->Read(&id, 4);
    if (id == 0xffffffffu)
        result = static_cast<const char*>(0);
    else
        result = strings[id];
}
