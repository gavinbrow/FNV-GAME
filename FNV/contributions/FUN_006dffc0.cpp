
struct FUN_00559450_shell { unsigned int FUN_00559450(); };
struct FUN_0044ddc0_shell { unsigned int FUN_0044ddc0(); };
struct FUN_00865db0_shell { void FUN_00865db0(unsigned int value, unsigned int flags); };
struct FUN_00865f60_shell { void FUN_00865f60(unsigned int value); };
struct FUN_006df9c0_shell { void FUN_006df9c0(FUN_00865db0_shell* buf); };
struct FUN_006dffc0_Class {
    int unk00;
    int unk04;
    int unk08;
    int unk0c;
    FUN_00559450_shell* m_ref;
    void FUN_006dffc0(FUN_00865db0_shell* buffer);
};
void FUN_006dffc0_Class::FUN_006dffc0(FUN_00865db0_shell* buffer)
{
    buffer->FUN_00865db0(m_ref ? m_ref->FUN_00559450() : 0, 0);
    unsigned int count = this ? ((FUN_0044ddc0_shell*)this)->FUN_0044ddc0() : 0;
    ((FUN_00865f60_shell*)buffer)->FUN_00865f60(count);
    for (unsigned int index = 0; index < count; ++index) {
        unsigned int* item = &((FUN_006a7ad0_shell*)this)->FUN_006a7ad0(index);
        ((FUN_006df9c0_shell*)*item)->FUN_006df9c0(buffer);
    }
}
