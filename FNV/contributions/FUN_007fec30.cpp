struct FloatSource {
    float* Get();
};

struct IntSource {
    int* Get();
};

extern FloatSource g_floatSource;
extern IntSource g_intSource;
extern const double g_epsilon;
int __cdecl FUN_00ecadb8();

struct Timer {
    char pad[0x158];
    bool unk158;
    float unk15c;
    float unk160;
    float unk164;
    float unk168;
    void FUN_007fec30(float now);
};

void Timer::FUN_007fec30(float now)
{
    float delta = now - unk15c;
    unk160 = delta / unk164;
    if (*g_floatSource.Get() + g_epsilon < unk160) {
        unk158 = false;
        unk168 = (float)(FUN_00ecadb8() % *g_intSource.Get()) + now;
    }
}
