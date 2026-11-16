extern float DAT_01017d00;
extern bool __cdecl FUN_0040eb10(float a, float b, float c);
struct PointObject;
struct RegionNode {
    bool FUN_004f70b0(PointObject* obj);
};
struct PointObject {
    int unk00, unk04;
    float position;
    bool FUN_004f7620(RegionNode* region, float value);
};
bool PointObject::FUN_004f7620(RegionNode* region, float value) {
    if (region == 0)
        return false;
    if (FUN_0040eb10(value, position, DAT_01017d00)) {
        if (region->FUN_004f70b0(this))
            return true;
    }
    return false;
}
