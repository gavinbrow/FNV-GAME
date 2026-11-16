struct VectorA {
    float x;
    float y;
    float z;
    float w;
    float v4;
    float v5;
};
struct VectorB {
    float unk00;
    float y;
    float z;
};
struct Result { float unk00; float unk04; float unk08; float value; };
struct Buffer { float* cursor; };
void __cdecl FUN_00dd03c0(VectorA* a, VectorB* b, Result* out, Buffer* buffer) {
    out->value = a->x * b->z;
    float* cursor = buffer->cursor;
    *cursor += 0.00000011920928955078125;
    *(unsigned char*)cursor = 10;
    cursor = (float*)((char*)cursor + 0x50);
    buffer->cursor = cursor;
    cursor[-8] = a->z * b->y;
    cursor[-7] = a->w * b->y;
    cursor[-6] = a->y;
    cursor[-5] = a->v4;
    cursor[-4] = a->v5;
}
