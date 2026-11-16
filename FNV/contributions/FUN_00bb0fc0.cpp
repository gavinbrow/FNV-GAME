
extern "C" __declspec(thread) unsigned int gShaderThreadMarker;

struct ShaderThreadMarkerScope {
    unsigned int previous;
    ShaderThreadMarkerScope() : previous(gShaderThreadMarker) {
        gShaderThreadMarker = 0x29;
    }
    ~ShaderThreadMarkerScope() {
        gShaderThreadMarker = previous;
    }
};

struct ShaderRenderCommand {
    int unk00;
    int unk04;
    int unk08;
    int unk0c;
    int dirty;
    void __thiscall FUN_00ba9ee0(void* source, unsigned int code, int active,
                                  int a, int b, int c, int d, int e);
};

struct ShaderRenderState {
    int unk00; int unk04; int unk08; int unk0c;
    int unk10; int unk14; int unk18; int unk1c;
    int unk20; int unk24; int unk28; int unk2c;
    int unk30; int unk34;
    unsigned int packedVersion;
    ShaderRenderCommand* command;

    void __thiscall FUN_00ba95e0(int enable);
    ShaderRenderCommand* __thiscall FUN_00bb0fc0(
        void* data, unsigned int version, int unused1,
        unsigned int variant, int unused2, int unused3);
};

ShaderRenderCommand* __thiscall ShaderRenderState::FUN_00bb0fc0(
    void* data, unsigned int version, int unused1,
    unsigned int variant, int unused2, int unused3)
{
    ShaderThreadMarkerScope marker;
    if (packedVersion != version) {
        FUN_00ba95e0(1);
        command->dirty = 0;
        command->FUN_00ba9ee0(data, 0x2cf, 1, 0, 0, 0, 0, 0);
        packedVersion = (variant << 8) | version;
    }
    return command;
}
