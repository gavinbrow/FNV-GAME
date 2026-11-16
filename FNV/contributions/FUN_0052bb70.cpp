namespace Real {
struct InterpolatorBase {
    unsigned int referenceCount;
    unsigned int flags;
    float lastTime;
    float currentTime;
    float startTime;
    float endTime;
    void* controller;
    ~InterpolatorBase();
};
struct ColorDataReference {
    void* colorData;
    ~ColorDataReference();
};
struct FUN_0052bb70 : InterpolatorBase {
    ColorDataReference colorData;
    ~FUN_0052bb70();
};
FUN_0052bb70::~FUN_0052bb70() {}
}