#include <xmmintrin.h>
struct VertexBuffer {
    __m128* values;
    unsigned int count;
    unsigned int capacityFlags;
};
extern "C" void __cdecl FUN_00c908c0(unsigned int allocator, VertexBuffer* output, unsigned int capacity, unsigned int alignment);
struct BoundsWriter {
    unsigned int unk00;
    unsigned int unk04;
    unsigned int unk08;
    unsigned int unk0c;
    unsigned int unk10;
    unsigned int unk14;
    unsigned int unk18;
    unsigned int unk1c;
    unsigned int unk20;
    unsigned int unk24;
    unsigned int unk28;
    unsigned int unk2c;
    unsigned int unk30;
    unsigned int unk34;
    unsigned int unk38;
    unsigned int unk3c;
    unsigned int unk40;
    unsigned int unk44;
    unsigned int unk48;
    unsigned int unk4c;
    unsigned int unk50;
    unsigned int unk54;
    unsigned int unk58;
    unsigned int unk5c;
    float minX;
    float minY;
    float minZ;
    unsigned int unk6c;
    float maxX;
    float maxY;
    float maxZ;
    void FUN_00de1260(VertexBuffer* output, unsigned int allocator);
};
void BoundsWriter::FUN_00de1260(VertexBuffer* output, unsigned int allocator)
{
    int oldCapacity = output->capacityFlags & 0x3FFFFFFF;
    if (oldCapacity < 24) {
        int newCapacity = oldCapacity * 2;
        if (newCapacity <= 24)
            newCapacity = 24;
        FUN_00c908c0(allocator, output, newCapacity, 16);
    }
    output->count = 24;
    output->values[0] = _mm_setr_ps(this->minX, this->minY, this->minZ, 0.0f);
    output->values[1] = _mm_setr_ps(this->minX, this->maxY, this->minZ, 0.0f);
    output->values[2] = _mm_setr_ps(this->minX, this->minY, this->minZ, 0.0f);
    output->values[3] = _mm_setr_ps(this->minX, this->minY, this->maxZ, 0.0f);
    output->values[4] = _mm_setr_ps(this->minX, this->minY, this->minZ, 0.0f);
    output->values[5] = _mm_setr_ps(this->maxX, this->minY, this->minZ, 0.0f);
    output->values[6] = _mm_setr_ps(this->maxX, this->maxY, this->maxZ, 0.0f);
    output->values[7] = _mm_setr_ps(this->maxX, this->maxY, this->minZ, 0.0f);
    output->values[8] = _mm_setr_ps(this->maxX, this->maxY, this->maxZ, 0.0f);
    output->values[9] = _mm_setr_ps(this->minX, this->maxY, this->maxZ, 0.0f);
    output->values[10] = _mm_setr_ps(this->maxX, this->maxY, this->maxZ, 0.0f);
    output->values[11] = _mm_setr_ps(this->maxX, this->minY, this->maxZ, 0.0f);
    output->values[12] = _mm_setr_ps(this->minX, this->maxY, this->minZ, 0.0f);
    output->values[13] = _mm_setr_ps(this->maxX, this->maxY, this->minZ, 0.0f);
    output->values[14] = _mm_setr_ps(this->minX, this->maxY, this->minZ, 0.0f);
    output->values[15] = _mm_setr_ps(this->minX, this->maxY, this->maxZ, 0.0f);
    output->values[16] = _mm_setr_ps(this->maxX, this->maxY, this->minZ, 0.0f);
    output->values[17] = _mm_setr_ps(this->maxX, this->minY, this->minZ, 0.0f);
    output->values[18] = _mm_setr_ps(this->minX, this->maxY, this->maxZ, 0.0f);
    output->values[19] = _mm_setr_ps(this->minX, this->minY, this->maxZ, 0.0f);
    output->values[20] = _mm_setr_ps(this->minX, this->minY, this->maxZ, 0.0f);
    output->values[21] = _mm_setr_ps(this->maxX, this->minY, this->maxZ, 0.0f);
    output->values[22] = _mm_setr_ps(this->maxX, this->minY, this->maxZ, 0.0f);
    output->values[23] = _mm_setr_ps(this->maxX, this->minY, this->minZ, 0.0f);
}
