#include "h_74712c1d3c73.h"
struct BDBF60_Shader {
    int unk00; int unk04; int unk08; int unk0C; int unk10;
    int unk14; int unk18; int unk1C; int unk20; int unk24;
    int unk28; int unk2C; int unk30; int unk34; int unk38;
    BSShaderProperty::RenderPassArray* pPasses;
    int __thiscall FUN_00bdbf60(NiGeometry* geom, ShadowSceneLight* light,
       ShadowSceneLight* alternateLight, unsigned short* count,
       unsigned char type, bool* enabled, bool sharedPass,
       bool useAlternatePass, bool useSpecialPass);
};
int __thiscall BDBF60_Shader::FUN_00bdbf60(NiGeometry* geom, ShadowSceneLight* light,
       ShadowSceneLight* alternateLight, unsigned short* count,
       unsigned char type, bool* enabled, bool sharedPass,
       bool useAlternatePass, bool useSpecialPass)
{
    if (!sharedPass) {
        if (type == 1) {
            unsigned short pass;
            if (useAlternatePass) pass = 0x24B;
            else if (!useSpecialPass) pass = 0x248;
            else {
                pPasses->Add(geom, 0x24A, *enabled, 0, 0, 0, 0, 0);
                return 0;
            }
            if (alternateLight) {
                pPasses->Add(geom, pass, *enabled, 1, alternateLight, 0, 0, 0);
            } else {
                pPasses->Add(geom, pass, *enabled, 1, light, 0, 0, 0);
            }
            return 0;
        }
    } else if (type == 1) {
        if (alternateLight) {
            pPasses->Add(geom, 0x249, *enabled, 1, alternateLight, 0, 0, 0);
            return 0;
        }
        pPasses->Add(geom, 0x249, *enabled, 1, light, 0, 0, 0);
        return 0;
    }
    ++*count;
    return 0;
}