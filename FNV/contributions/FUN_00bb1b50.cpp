union FogSlots_00bb1b50 { float f[8]; unsigned int u[8]; };
void __stdcall FUN_00bb1b50(int unused)
{
    FogInfo* src = FUN_00b55520(DAT_011f91c4);
    if (src != 0) {
        FogSlots_00bb1b50 t;
        t.f[0] = src->farDistance;
        t.u[1] = *(unsigned int*)&src->color.r;
        t.u[2] = *(unsigned int*)&src->color.g;
        t.u[3] = *(unsigned int*)&src->color.b;
        t.f[4] = t.f[0];
        t.f[5] = t.f[4] - src->nearDistance;
        t.f[6] = src->density;
        t.f[7] = 0.0f;
        DAT_011fa280 = *(FogVector4*)&t.f[4];
        t.f[4] = t.f[1];
        t.f[5] = t.f[2];
        t.f[6] = t.f[3];
        t.f[7] = 0.0f;
        DAT_011fa290 = *(FogVector4*)&t.f[4];
    }
}