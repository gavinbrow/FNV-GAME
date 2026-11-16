struct Object {};
void __cdecl FUN_00cebdf0(float* source, float value, Object* destination);
void __cdecl FUN_00cebe50(float* source, float scale, Object* destination) {
    float result = *source * scale;
    FUN_00cebdf0(source, result, destination);
}
