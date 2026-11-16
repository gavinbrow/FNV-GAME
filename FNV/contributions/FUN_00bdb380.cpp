
struct Key {
    unsigned int first, second, third;
    bool FUN_00439090(const Key* other);
};
extern "C" Key DAT_011f4998;
struct AllocationManager {
    void* FUN_00aa3e40(unsigned int count);
};
extern "C" AllocationManager DAT_011f6238;
struct RenderPass {
    void SetEnabled() { *reinterpret_cast<unsigned char*>(reinterpret_cast<char*>(this) + 8) = 1; }
};
struct RenderPassStack {
    unsigned int field00;
    RenderPass** passes;
    unsigned int field08;
    unsigned int field0c;
    unsigned int count;
    RenderPass* Last() const { return passes[count - 1]; }
};
struct Message {
    unsigned int type;
    unsigned int actor;
    unsigned int data;
    unsigned int state;
    __cdecl Message(void* actor, unsigned int code, int first, int second, int third, ...);
    static void* operator new(unsigned int count) {
        return DAT_011f6238.FUN_00aa3e40(count);
    }
};
struct Shader {
    Message* FUN_00bdb380(void* actor, unsigned short* missed, unsigned char passType,
                           unsigned char useAlternate, unsigned int context);
};
Message* Shader::FUN_00bdb380(void* actor, unsigned short* missed, unsigned char passType,
                              unsigned char useAlternate, unsigned int context) {
    Message* result = 0;
    void* resource = *reinterpret_cast<void**>(reinterpret_cast<char*>(actor) + 0xa4);
    if (resource) {
        Key* key = *reinterpret_cast<Key**>(reinterpret_cast<char*>(resource) + 0x34);
        if (!key) key = reinterpret_cast<Key*>(reinterpret_cast<char*>(resource) + 0x28);
        if (Key(*key).FUN_00439090(&DAT_011f4998)) {
            RenderPassStack* stack =
                *reinterpret_cast<RenderPassStack**>(reinterpret_cast<char*>(this) + 0x3c);
            RenderPass* last = stack->Last();
            if (last) last->SetEnabled();
            if (!useAlternate) {
                if (passType == 1) {
                    result = new Message(actor, 0x2d6, 0, 0, 0);
                } else {
                    ++*missed;
                }
            } else {
                if (passType == 1) {
                    result = new Message(actor, 0x2d7, 0, 0, 0);
                } else {
                    ++*missed;
                }
            }
        }
    }
    return result;
}
