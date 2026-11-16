extern unsigned int DAT_011f4998;
extern unsigned int DAT_011f499c;
extern unsigned int DAT_011f49a0;
struct NiColorSource {
    unsigned int unk00; unsigned int unk04; unsigned int unk08;
    unsigned int unk0c; unsigned int unk10; unsigned int unk14; unsigned int unk18;
    unsigned int r; unsigned int g; unsigned int b;
    unsigned int embeddedR; unsigned int embeddedG; unsigned int embeddedB;
    unsigned int* color;
};
struct ColorHolder {
    unsigned int unk00; unsigned int unk04; unsigned int unk08; unsigned int unk0c;
    unsigned int unk10; unsigned int unk14; unsigned int unk18; unsigned int unk1c;
    unsigned int unk20; unsigned int unk24; unsigned int unk28;
    NiColorSource* source;
    unsigned int unk30; unsigned int unk34;
    unsigned short mode;
    void FUN_00a4b3c0(float* output);
};
void ColorHolder::FUN_00a4b3c0(float* output) {
    float red = 0.0f;
    float green = 0.0f;
    float blue = 0.0f;
    register unsigned int type = mode & 7;
    register NiColorSource* source = this->source;
    switch (type) {
    case 0:
    case 1:
        *(unsigned int*)&red = DAT_011f4998;
        *(unsigned int*)&green = DAT_011f499c;
        *(unsigned int*)&blue = DAT_011f49a0;
        break;
    case 2:
        *(unsigned int*)&red = source->r;
        *(unsigned int*)&green = source->g;
        *(unsigned int*)&blue = source->b;
        break;
    case 3: {
        unsigned int* selected = source->color ? source->color : &source->embeddedR;
        *(unsigned int*)&red = selected[0];
        *(unsigned int*)&green = selected[1];
        *(unsigned int*)&blue = selected[2];
        break;
    }
    }
    output[0] = red;
    output[1] = green;
    output[2] = blue;
}