struct SampleField {
    int FUN_00e587a0();
    float* FUN_00e58780(int index, int component);
    void FUN_00e58820(float* value);
    float FUN_00e587c0(int index, int component);
};
struct FUN_00e58a20_cls {
    float* m_00;
    int m_04;
    int unk08;
    int* m_0c;
    int unk10;
    int unk14;
    int* m_18;
    void FUN_00e58a20(SampleField* volatile input, SampleField* weights, SampleField* output);
};
void FUN_00e58a20_cls::FUN_00e58a20(SampleField* volatile input,
                                      SampleField* weights,
                                      SampleField* output) {
    float initial = 0.0f;
    output->FUN_00e58820(&initial);
    int component = 0;
    if (input->FUN_00e587a0() > 0) {
        int elementCount = m_04;
        do {
            int index = 0;
            if (elementCount > 0) {
                do {
                    float* destination = output->FUN_00e58780(m_0c[index], component);
                    *destination = weights->FUN_00e587c0(m_18[index], component) * m_00[index] + *destination;
                    ++index;
                    elementCount = m_04;
                } while (index < elementCount);
            }
            ++component;
        } while (component < input->FUN_00e587a0());
    }
    component = 0;
    if (input->FUN_00e587a0() > 0) {
        int elementCount = m_04;
        do {
            int index = 0;
            if (elementCount > 0) {
                do {
                    float* destination = input->FUN_00e58780(m_18[index], component);
                    float* src = output->FUN_00e58780(m_0c[index], component);
                    *destination = m_00[index] * *src + *destination;
                    ++index;
                    elementCount = m_04;
                } while (index < elementCount);
            }
            ++component;
        } while (component < input->FUN_00e587a0());
    }
}