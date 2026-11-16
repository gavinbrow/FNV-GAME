struct FUN_00d617d0_cls {
    char* m_p00;
    int m_i04;
    void FUN_00d617d0(int count);
};
void FUN_00d617d0_cls::FUN_00d617d0(int count)
{
    if (count > 0) {
        m_i04 -= count;
        int remaining = m_i04;
        char* destination = m_p00;
        char* source = destination + count;
        if (remaining > 0) {
            for (int i = 0; i < remaining; ++i) {
                destination[i] = source[i];
            }
        }
    }
}