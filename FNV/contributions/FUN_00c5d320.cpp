
extern float DAT_01204360;
extern const double DAT_01012060;
extern int DAT_01203b58[];
extern float DAT_01203350[];
extern int DAT_01203f58[];
extern float DAT_01203750[];
extern const double DAT_010231d8;
extern const double DAT_01017a10;
extern const double DAT_01012070;
extern "C" int __cdecl rand(void);
float __cdecl FUN_00c5d2b0(float value);
void __cdecl FUN_00c5d300(float blend, float a, float b);

void __cdecl FUN_00c5d320(float input)
{
    int nIndex;
    if (DAT_01204360 == DAT_01012060) {
        for (nIndex = 0; nIndex < 256; ++nIndex) {
            DAT_01203b58[nIndex] = nIndex;
            DAT_01203350[nIndex] = float((rand() % 512) - 256) / DAT_010231d8;
        }

        while (--nIndex) {
            int saved = DAT_01203b58[nIndex];
            int other = rand() % 256;
            DAT_01203b58[nIndex] = DAT_01203b58[other];
            DAT_01203b58[other] = saved;
        }

        for (nIndex = 0; nIndex < 258; ++nIndex) {
            DAT_01203f58[nIndex] = DAT_01203b58[nIndex];
            DAT_01203750[nIndex] = DAT_01203350[nIndex];
        }
        DAT_01204360 = 1.0f;
    }

    float localValue = float(input + DAT_01017a10);
    int baseIndex = (int(localValue)) & 255;
    int second = (baseIndex + 1) & 255;
    float frac = localValue - int(localValue);
    float fractionMinusOne = frac - DAT_01012070;
    float left = FUN_00c5d2b0(frac);
    float right = frac * DAT_01203350[DAT_01203b58[baseIndex]];
    float weight = fractionMinusOne * DAT_01203350[DAT_01203b58[second]];
    FUN_00c5d300(left, right, weight);
}
