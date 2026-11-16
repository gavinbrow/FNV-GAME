struct Vec3Ops {
    float x;
    float y;
    float z;
    Vec3Ops* __thiscall Sub(Vec3Ops* result, const Vec3Ops& rhs) const;
    Vec3Ops* __thiscall Add(Vec3Ops* result, const Vec3Ops& rhs) const;
};
Vec3Ops* __cdecl FUN_004a3760(Vec3Ops* result, float amount, const Vec3Ops& value);
extern double DAT_01012060;

bool __cdecl FUN_006ba100(const NiPoint3* param_1,
                          const NiPoint3* param_2,
                          const NiPoint3* param_3,
                          const NiPoint3* param_4,
                          NiPoint3* param_5)
{
    float fStack_8 = (param_1->x - param_4->x) * (param_2->y - param_4->y)
                   - (param_1->y - param_4->y) * (param_2->x - param_4->x);
    float fStack_c = (param_1->x - param_3->x) * (param_2->y - param_3->y)
                   - (param_1->y - param_3->y) * (param_2->x - param_3->x);
    if (fStack_8 * fStack_c <= DAT_01012060) {
        float fStack_14 = (param_3->x - param_1->x) * (param_4->y - param_1->y)
                        - (param_3->y - param_1->y) * (param_4->x - param_1->x);
        float fStack_10 = (fStack_14 + fStack_c) - fStack_8;
        if (fStack_14 * fStack_10 < DAT_01012060) {
            float fStack5 = fStack_14 / (fStack_14 - fStack_10);
            Vec3Ops temp4;
            Vec3Ops temp2c4;
            Vec3Ops temp38;
            *param_5 = *reinterpret_cast<const NiPoint3*>(
                reinterpret_cast<const Vec3Ops&>(*param_1).Add(&temp38,
                    *reinterpret_cast<const Vec3Ops*>(FUN_004a3760(&temp2c4, fStack5,
                        *reinterpret_cast<const Vec3Ops*>(reinterpret_cast<const Vec3Ops&>(*param_2).Sub(
                            &temp4, reinterpret_cast<const Vec3Ops&>(*param_1)))))));
            return true;
        }
    }
    return false;
}

