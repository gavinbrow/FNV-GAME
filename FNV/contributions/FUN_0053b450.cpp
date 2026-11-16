extern float DAT_01017a3c;
struct FNv53b450_Point {
    float x;
    float y;
    float z;
    void FUN_006815c0();
};
struct FNv53b450_Source {
    int FUN_00533fd0();
    int FUN_00534010();
    FNv53b450_Point* FUN_0053b450(FNv53b450_Point* output, unsigned char flags, unsigned short cellIndex, const int* x, const int* y);
};
FNv53b450_Point* FNv53b450_Source::FUN_0053b450(FNv53b450_Point* output, unsigned char flags, unsigned short cellIndex, const int* x, const int* y) {
    FNv53b450_Point result;
    result.FUN_006815c0();
    result.x = DAT_01017a3c;
    result.y = DAT_01017a3c;
    result.x = float(x ? *x : FUN_00533fd0()) * result.x;
    result.y = float(y ? *y : FUN_00534010()) * result.y;
    result.x = float(((flags & 1) ? 2048 : 0)) + result.x;
    result.y = float(((flags & 2) ? 2048 : 0)) + result.y;
    result.x = float((cellIndex % 17) << 7) + result.x;
    result.y = float((cellIndex / 17) << 7) + result.y;
    result.z = 0.0f;
    *output = result;
    return output;
}