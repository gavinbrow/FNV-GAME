struct Vector4 {
    float x, y, z, w;
    void __thiscall FUN_004b4db0(const Vector4*);
};
struct InnerData {
    float unk00, unk04, unk08, unk0c, unk10, unk14, unk18, unk1c;
    Vector4 q20;
    Vector4 q30;
    float x40, y44, z48, w4c;
};
struct OutputData {
    unsigned int unk00, unk04, unk08, unk0c;
    Vector4 a10;
    Vector4 b20;
    float x30, y34, z38, w3c;
};
void __stdcall FUN_00c867d0(OutputData*);
struct FUN_00c86d20_Class {
    int unk00, unk04;
    InnerData* inner;
    void __thiscall FUN_00c86d20(OutputData* dest);
};
void FUN_00c86d20_Class::FUN_00c86d20(OutputData* dest) {
    FUN_00c867d0(dest);
    dest->x30 = (this && inner) ? inner->x40 : 0.0f;
    dest->y34 = (this && inner) ? inner->y44 : 0.0f;
    dest->w3c = (this && inner) ? inner->w4c : 0.0f;
    if (this) {
        InnerData* current = inner;
        if (current) {
            dest->a10.FUN_004b4db0(&current->q20);
            dest->b20.FUN_004b4db0(&current->q30);
            dest->z38 = current->z48;
            return;
        }
    }
    dest->a10.x=0.0f; dest->a10.y=0.0f; dest->a10.z=0.0f; dest->a10.w=0.0f;
    dest->b20.x=0.0f; dest->b20.y=0.0f; dest->b20.z=0.0f; dest->b20.w=0.0f;
    dest->z38=0.0f;
}