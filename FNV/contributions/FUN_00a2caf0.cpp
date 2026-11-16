struct KeyframeElement {
    float time;
    float value;
    float inTangent;
    float outTangent;
    float tension;
    float continuity;
    float bias;
    ~KeyframeElement();
    void FUN_00a2c9d0(void* context);
    static void* operator new[](unsigned int bytes) {
        return ((P03MM*)&g_memoryManager)->Allocate(bytes);
    }
};
KeyframeElement* __cdecl FUN_00a2caf0(void* context, unsigned int count) {
    KeyframeElement* elements = new KeyframeElement[count];
    if (count > 0) {
        KeyframeElement* cursor = elements;
        do {
            cursor->FUN_00a2c9d0(context);
            ++cursor;
            --count;
        } while (count != 0);
    }
    return elements;
}