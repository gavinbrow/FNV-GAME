
extern char* DAT_0109b220;

struct SeqExt : FUN_00a33bf0_s {
    void FUN_00a328b0(float time, bool setControllerTimes);
};

void SeqExt::FUN_00a328b0(float time, bool setControllerTimes)
{
    float currentTime = time + m_fBeginKeyTime;
    if (setControllerTimes) {
        unsigned int index = 0;
        if (index < m_uiArraySize) {
            do {
                SeqIDTag& tag = m_pkIDTagArray[index];
                void* controller = m_pkInterpArray[index].m_spInterpCtlr;
                if (controller && tag.m_kCtlrType != DAT_0109b220 &&
                    (!tag.m_kCtlrType || tag.m_kCtlrType[2] != 'T' || tag.m_kCtlrType[7] != 'f')) {
                    *reinterpret_cast<float*>(static_cast<char*>(controller) + 0x10) = time;
                }
                ++index;
            } while (index < m_uiArraySize);
        }
    }
    *reinterpret_cast<float*>(&m_pad44[4]) = currentTime;
}
