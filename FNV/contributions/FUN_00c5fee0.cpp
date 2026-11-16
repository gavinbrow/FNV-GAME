void* __cdecl FUN_00aa13e0(unsigned int);
struct PositionModifierInstance {
    FUN_00c5fd30 modifier;
    void* name;
    unsigned int order;
    void* target;
    bool active;
    float lastTime;
    void* next;
    static __forceinline void* operator new(unsigned int amount) {
        return FUN_00aa13e0(amount);
    }
};
FUN_00c5fd30* __cdecl FUN_00c5fee0() {
    PositionModifierInstance* instance = new PositionModifierInstance;
    return &instance->modifier;
}