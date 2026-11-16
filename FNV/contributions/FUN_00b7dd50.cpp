struct RenderContext {
    void FUN_00e7eb00(int mode);
};
struct RenderNode {
    int unk00, unk04, unk08, unk0c, unk10;
    RenderContext* unk14;
};
struct RenderGlobals {
    int unk00, unk04, unk08, unk0c, unk10, unk14, unk18, unk1c, unk20;
    RenderNode* unk24;
    int unk28, unk2c, unk30, unk34, unk38, unk3c, unk40;
    void* unk44;
};
extern int DAT_0126f74c;
struct FeatureFlags {
    int unk00, unk04, unk08, unk0c, unk10, unk14, unk18, unk1c;
    int active20;
};
extern FeatureFlags* DAT_011febf0;
extern FeatureFlags* DAT_011fec38;
struct NiQuaternion { float w, x, y, z; };
struct NiMatrix3 { float m00,m01,m02,m10,m11,m12,m20,m21,m22; };
struct NiPoint3 { float x,y,z; };
struct NiTransform { NiMatrix3 rotate; NiPoint3 translate; float scale; };
struct RenderOutput { NiQuaternion orientation; NiTransform transform; };
struct Callback;
typedef void (__thiscall *RenderCallback)(Callback*,void*,int,int,int,int,int,int,NiTransform*,NiQuaternion*,int,int);
struct Callback {
    RenderCallback* vtable;
};
struct Renderer {
    int unk00, unk04, unk08, unk0c, unk10, unk14, unk18, unk1c, unk20, unk24, unk28, unk2c;
    Callback* target30;
    void FUN_00b7c3a0();
    void FUN_00b7c510();
    void FUN_00b7c580();
    void FUN_00b7c600();
    void FUN_00b7dd50();
};
void Renderer::FUN_00b7dd50()
{
    RenderOutput outputs;
    reinterpret_cast<RenderGlobals*>(DAT_0126f74c)->unk24->unk14->FUN_00e7eb00(0);
    FUN_00b7c3a0();
    DAT_011febf0->active20 = 1;
    DAT_011fec38->active20 = 1;
    FUN_00b7c510();
    FUN_00b7c580();
    FUN_00b7c600();
    Callback* callback = target30;
    if (callback && reinterpret_cast<RenderGlobals*>(DAT_0126f74c)->unk44)
        callback->vtable[30](callback, reinterpret_cast<RenderGlobals*>(DAT_0126f74c)->unk44, 0,0,0,0,0,0,
                             &outputs.transform, &outputs.orientation, 0,1);
}
