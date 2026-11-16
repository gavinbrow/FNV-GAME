struct FUN_00e05a80Class {
    virtual void first();
    virtual void second();
    virtual void third();
    virtual unsigned char* checkState(unsigned char* state);

    int m_04;
    unsigned char* m_08;
    int m_0c;
    int m_10;

    int __thiscall FUN_00e05a80(void* destination, int count);
};
extern "C" void __cdecl FUN_00cb1260(void* destination, const void* source, int count);

int __thiscall FUN_00e05a80Class::FUN_00e05a80(void* destination, int count) {
    unsigned char state;
    if (*checkState(&state)) {
        int remaining = m_10 - m_0c;
        int copied = count < remaining ? count : remaining;
        FUN_00cb1260(destination, m_08 + m_0c, copied);
        m_0c += copied;
        if (copied == 0 && count != 0)
            m_0c = m_10 + 1;
        return copied;
    }
    return 0;
}