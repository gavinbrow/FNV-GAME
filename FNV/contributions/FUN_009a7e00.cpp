struct Vec3 {
    float x;
    float y;
    float z;
    Vec3 FUN_00439ef0(const Vec3& b) const;
    float FUN_00589850() const;
    float FUN_00457990() const;
};

struct GlobalSetting {
    float* FUN_00403e20();
};
extern GlobalSetting g_011cfb78;

struct ShotActor {
    float FUN_0069ef80();
    float FUN_00966980();
};

float __cdecl FUN_009a7e00(ShotActor* actor, Vec3 from, Vec3 to, bool flag, float speed)
{
    Vec3 vDelta = from.FUN_00439ef0(to);
    float fVel = speed;
    if (speed == DAT_01012060) {
        fVel = actor->FUN_0069ef80();
    }
    if (actor->FUN_00966980() != DAT_01012060) {
        if (flag && speed == DAT_01012060) {
            speed = speed * *g_011cfb78.FUN_00403e20();
        }
        float fAngle = vDelta.z;
        float fGravity = vDelta.FUN_00589850();
        float fHeight = FUN_009a7c60(fGravity, fAngle, speed, actor->FUN_00966980() * DAT_011f1c00, false);
        return FUN_009a7dd0(fGravity, fHeight, fVel);
    }
    return vDelta.FUN_00457990() / speed;
}
