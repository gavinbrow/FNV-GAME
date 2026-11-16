extern __declspec(thread) int g_tls_2b4;
struct FUN_00b8cc20_class {
    void __thiscall FUN_00b8cc20(int mode, int component, const float* values, float scale);
};
void __thiscall FUN_00b8cc20_class::FUN_00b8cc20(int mode, int component, const float* values, float scale)
{
    int previousContext = g_tls_2b4;
    g_tls_2b4 = 39;
    int index = 0;
    float* destination = (float*)((char*)this + component * 4 + 0xb4);
    do {
        switch (mode) {
            case 0: destination[15] += values[index] * scale; break;
            case 1: destination[0] += values[index] * scale; break;
            case 3: destination[25] += values[index] * scale; break;
        }
        ++index;
        destination += 38;
    } while (index < 2);
    g_tls_2b4 = previousContext;
}