struct NiPoint3
{
    float x;
    float y;
    float z;

    void FUN_00416870(float xValue, float yValue, float zValue);
};

extern NiPoint3 DAT_011ca35c;
extern const float DAT_01016248;

// @fnv 0x00f4bda0
void FUN_00f4bda0()
{
    DAT_011ca35c.FUN_00416870(1.0f, DAT_01016248, 0.0f);
}
