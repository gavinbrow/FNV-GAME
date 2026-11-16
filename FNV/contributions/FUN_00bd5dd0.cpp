struct ShaderSource { int x, y, z; };
struct ShaderFlags {
    int unk00, unk04, unk08, unk0c, unk10, unk14, unk18, unk1c, unk20;
    unsigned int flags;
    int unk28, unk2c, unk30, unk34;
    int associatedValue;
};
struct ShaderState {
    int unk00, unk04;
    ShaderFlags* controller;
    int unk0c, unk10, unk14;
    int x, y, z;
    void FUN_00bd5dd0(const ShaderSource* source);
};
void ShaderState::FUN_00bd5dd0(const ShaderSource* source) {
    if (source) {
        x = source->x;
        y = source->y;
        z = source->z;
    }
    ShaderFlags* state = controller;
    if (state->flags & 0x400)
        state->associatedValue = 0;
    *reinterpret_cast<volatile unsigned int*>(&state->flags) &= ~0x400u;
    state = controller;
    if (state->flags & 0x800)
        state->associatedValue = 0;
    *reinterpret_cast<volatile unsigned int*>(&state->flags) &= ~0x800u;
    state = controller;
    if (state->flags & 0x1000)
        state->associatedValue = 0;
    *reinterpret_cast<volatile unsigned int*>(&state->flags) &= ~0x1000u;
}