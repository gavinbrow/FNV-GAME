extern "C" double __cdecl sqrt(double);
extern "C" double __cdecl acos(double);

extern double DAT_0101a6b0;
extern float DAT_0109c9c4;
static const float epsilon = 0.001f;

struct FUN_00a6de50_shell {
    float m_fW, m_fX, m_fY, m_fZ;
    void FUN_00a6de50(float* angle, float* axis);
};

void FUN_00a6de50_shell::FUN_00a6de50(float* angle, float* axis) {
    float sq = m_fX*m_fX + m_fY*m_fY + m_fZ*m_fZ;
    volatile float root = (float)sqrt(sq);
    float length = root;

    if (length < epsilon) {
        *angle = 0;
        axis[0] = 0;
        axis[1] = 0;
        axis[2] = 0;
        return;
    }

    float w = m_fW;
    float anglePart;
    if (w > DAT_0101a6b0) {
        if (w < 1.0f) {
            volatile float acosRoot = (float)acos(w);
            anglePart = acosRoot;
        } else {
            anglePart = 0;
        }
    } else {
        anglePart = DAT_0109c9c4;
    }

    *angle = anglePart + anglePart;
    float invLength = 1.0f / length;
    axis[0] = invLength * m_fX;
    axis[1] = invLength * m_fY;
    axis[2] = invLength * m_fZ;
}