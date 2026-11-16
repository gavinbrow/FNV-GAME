struct NiPoint3Local { float x, y, z; };
struct hkVector4D90 {
    unsigned char m_packedComponents[16];
    void FUN_006815c0();
};
hkVector4D90* __cdecl FUN_004a3e00(hkVector4D90* destination, const NiPoint3Local* source);
class FUN_008c5d90_Class {
public:
    void FUN_008c5df0(hkVector4D90* converted);
    void FUN_008c5d90(const NiPoint3Local* source);
};
void FUN_008c5d90_Class::FUN_008c5d90(const NiPoint3Local* source)
{
    __declspec(align(16)) hkVector4D90 vector;
    vector.FUN_006815c0();
    FUN_008c5df0(FUN_004a3e00(&vector, source));
}