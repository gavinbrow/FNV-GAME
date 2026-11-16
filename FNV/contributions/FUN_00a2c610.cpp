struct ShapeValues {
    float initial;
    float start;
    float intermediateA;
    float intermediateB;
    float intermediateC;
    float end;
    float extent;
};
extern "C" float __cdecl func_0x00a42070(float input, float leftStart, float leftExtent, float rightStart, float rightEnd);

void __cdecl FUN_00a2c610(float input, const ShapeValues* left, const ShapeValues* right, float* result) {
    const float rightStart = right->start;
    const float leftStart = left->start;
    *result = func_0x00a42070(input, leftStart, left->extent, rightStart, right->end);
}