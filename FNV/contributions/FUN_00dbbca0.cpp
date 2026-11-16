
struct FUN_00dbbca0_class {
 int m_00,m_04,m_08,m_0c;
 char* m_10;
 int m_14, m_18, m_1c;
 float FUN_00dbbca0(int index);
};
float FUN_00dbbca0_class::FUN_00dbbca0(int index) {
 volatile float& slot = *reinterpret_cast<volatile float*>(&index);
 if (m_1c != 11) {
    if (m_1c != 32) {
       slot = 0.0f;
       return slot;
    }
    index = int(*reinterpret_cast<short*>(m_10 + m_18 * index)) << 16;
    return slot;
 }
 slot = *reinterpret_cast<float*>(m_10 + m_18 * index);
 return slot;
}
