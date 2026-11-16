extern double DAT_01021928;
extern double DAT_01011590;
void __cdecl FUN_00a27d60(float t, TCBKeyS* key, unsigned int type, Vec3S* result)
{
    const float scaled = static_cast<float>(DAT_01021928 * t);
    Vec3S fromScaled = {key->extra[3] * scaled, key->extra[4] * scaled, key->extra[5] * scaled};
    Vec3S fromDefault = {static_cast<float>(DAT_01011590 * key->extra[0]),
                         static_cast<float>(DAT_01011590 * key->extra[1]),
                         static_cast<float>(DAT_01011590 * key->extra[2])};
    Vec3S direction = {fromScaled.x + fromDefault.x, fromScaled.y + fromDefault.y, fromScaled.z + fromDefault.z};
    Vec3S offset = {t * direction.x, t * direction.y, t * direction.z};
    Vec3S translated = {key->out.x + offset.x, key->out.y + offset.y, key->out.z + offset.z};
    *result = translated;
}