struct CellEffects;
struct NiPoint2 { float x; float y; };
struct WorldSpaceAccess : TESWorldSpace {
    CellEffects* __thiscall FUN_00585b30(int x, int y);
};
struct NodeEffects : NiNode {
    void __thiscall FUN_00535b90(bool value);
    void __thiscall FUN_0053fa40(unsigned char value);
    void __thiscall FUN_0053f440();
};
struct CellEffects : TESObjectCELL {
    void __thiscall FUN_00545cf0();
    NodeEffects* __thiscall FUN_00546fb0();
    NodeEffects* __thiscall FUN_00546fb0(NiPoint2* outPosition);
    bool __thiscall FUN_00451cd0();
    float __thiscall FUN_005471e0();
    void __thiscall FUN_00451250(bool value);
    bool __thiscall FUN_004518e0();
    void __thiscall FUN_00961f30(bool value);
};
struct GameWorld : TES {
    CellEffects* __thiscall FUN_00461330(int mode, int x, int y, WorldSpaceAccess* worldSpace);
};
extern GameWorld* DAT_011c3f2c;
extern FUN_00528790_shell* DAT_011dea10;
struct GlobalSettings {
    unsigned char* __thiscall FUN_00408d60();
};
extern GlobalSettings DAT_011c7adc;
void __cdecl FUN_0049c860(CellEffects* cell);
struct CellLoadData : EXTERIOR_CELL_DATA {
    WorldSpaceAccess* worldSpace;
    CellEffects* cell;
    bool loaded;
};
struct CellLoader {
    void __thiscall FUN_00528620(CellLoadData* data);
};
void CellLoader::FUN_00528620(CellLoadData* data)
{
    if (data != 0) {
        if (data->cell == 0)
            data->cell = data->worldSpace->FUN_00585b30(data->iX, data->iY);
        if (data->cell == 0)
            data->cell = DAT_011c3f2c->FUN_00461330(0, data->iX, data->iY, data->worldSpace);
        data->cell->FUN_00545cf0();
        NodeEffects* pNode = data->cell->FUN_00546fb0();
        if (pNode != 0) {
            pNode->FUN_00535b90(true);
            pNode->FUN_0053fa40(DAT_011dea10->FUN_00528790());
        }
        if (!data->cell->FUN_00451cd0()) {
            NiPoint2 position;
            data->cell->FUN_00546fb0(&position)->FUN_0053f440();
            data->cell->FUN_00451250(position.x < data->cell->FUN_005471e0());
            if (*DAT_011c7adc.FUN_00408d60() &&
                data->cell->FUN_004518e0() &&
                !data->cell->FUN_00451cd0()) {
                FUN_0049c860(data->cell);
            }
            data->cell->FUN_00961f30(true);
        }
        data->loaded = true;
    }
}