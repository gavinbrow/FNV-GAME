struct CpuObject {
    unsigned int unk00;
    unsigned int unk04;
    unsigned int unk08;
    unsigned int unk0c;
    unsigned int unk10;
    unsigned int unk14;
    unsigned int unk18;
    unsigned int unk1c;
    unsigned int unk20;
    int value;
    void FUN_00eea560(int value);
};
void CpuObject::FUN_00eea560(int value)
{
    this->value = value;
}
