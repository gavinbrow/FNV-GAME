struct NiGeometry;
struct ShadowSceneLight;
struct RenderPassArray {
    int unk00;
    int unk04;
    int unk08;
    int unk0c;
    int unk10;
    void __thiscall FUN_00ba9ee0(NiGeometry* geometry, unsigned short pass, bool enabled,
       unsigned char lightCount, ShadowSceneLight* light0, ShadowSceneLight* light1,
       ShadowSceneLight* light2, ShadowSceneLight* light3);
};
struct ShaderPassController {
    int unk00, unk04, unk08, unk0c, unk10, unk14, unk18, unk1c;
    int unk20, unk24, unk28, unk2c, unk30, unk34, unk38, unk3c;
    int unk40, unk44;
    RenderPassArray* passes;
    void __thiscall FUN_00bde170(NiGeometry* geometry, bool alternate, bool enabled);
};
void ShaderPassController::FUN_00bde170(NiGeometry* geometry, bool alternate, bool enabled) {
    RenderPassArray* array = passes;
    if (array->unk10 != 0)
        return;
    if (enabled)
        array->FUN_00ba9ee0(geometry, 0x1ee, true, 0, 0, 0, 0, 0);
    else if (!alternate)
        array->FUN_00ba9ee0(geometry, 0x1ec, true, 0, 0, 0, 0, 0);
    else
        array->FUN_00ba9ee0(geometry, 0x1ed, true, 0, 0, 0, 0, 0);
}