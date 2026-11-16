struct FieldReadState;
typedef unsigned int (__cdecl *ReadFunction)(FieldReadState*, float*, unsigned int, unsigned int*, unsigned int);
struct FieldReadState {
    int unk00;
    unsigned int bytesRead;
    ReadFunction read;
    void ReadFloat(float* value) {
        unsigned int readSize = 4;
        bytesRead += read(this, value, 4, &readSize, 1);
    }
};
extern double DAT_01032980;
extern float DAT_01022958;
struct FUN_00c27700_class {
    int unk00, unk04, unk08, unk0c, unk10, unk14;
    int unk18, unk1c, unk20, unk24, unk28, unk2c;
    float m_value, m_inverse;
    void __thiscall FUN_00c32120(void* object);
    void __thiscall FUN_00c27700(void* object);
};
void __thiscall FUN_00c27700_class::FUN_00c27700(void* object)
{
    FUN_00c32120(object);
    FieldReadState* stream = *(FieldReadState**)((char*)object + 0x24c);
    stream->ReadFloat(&m_value);
    if (m_value < DAT_01032980)
        m_inverse = DAT_01022958;
    else
        m_inverse = 1.0f / m_value;
}
