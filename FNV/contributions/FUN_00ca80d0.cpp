extern float DAT_01016248;
struct Vector3 { float x, y, z; };
struct Output { unsigned int unk00, unk04, unk08, unk0c, unk10, unk14, unk18, unk1c, unk20, unk24, unk28, unk2c, unk30, unk34, unk38, unk3c, unk40, unk44, unk48; float value; };
inline float lowerPair(float left, float right) { return left < right ? left : right; }
inline float lowerPairReversed(float left, float right) { return left > right ? right : left; }
void __fastcall FUN_00ca80d0(const Vector3* values, Output* result) {
    float firstMinimum = lowerPair(values->x, values->y);
    float minimum = lowerPair(firstMinimum, values->z);
    if (DAT_01016248 > minimum) result->value = 0.2 * minimum;
    else result->value = 0.1f;
}


