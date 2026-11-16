extern "C" void* __cdecl FUN_00ec61c0(void*, int, unsigned int);
struct ByteVertexConversion {
    unsigned int format;
    unsigned short sourceType;
    unsigned short unk06;
    unsigned short count;
    unsigned short unk0A;
    const unsigned short* indices;
    const unsigned char* source;
    unsigned int unk14;
    unsigned int sourceStride;
    unsigned int destinationSize;
    unsigned int destinationStride;
    unsigned int unk24;
    unsigned int unk28;
    unsigned char* destination;
};
unsigned int __cdecl FUN_00e77770(ByteVertexConversion* info) {
    unsigned int written = 0;
    const unsigned char* source = info->source;
    const unsigned short* indices = info->indices;
    unsigned char* destination = info->destination;
    if (!source) {
        for (unsigned short i = 0; i < info->count; i++) {
            FUN_00ec61c0(destination, 0, info->destinationSize);
            destination += info->destinationStride;
            written += info->destinationSize;
        }
        return written;
    }
    unsigned short supplied = info->sourceType - 24;
    unsigned short components = info->format == 6 ? 2 : 4;
    unsigned short copied = supplied > components ? components : supplied;
    if (indices) {
        unsigned short index = 0;
        for (unsigned short i = 0; i < info->count; i++) {
            const unsigned char* input = source + indices[index++] * info->sourceStride;
            unsigned short* output = reinterpret_cast<unsigned short*>(destination);
            unsigned short j;
            for (j = 0; j < copied; j++) *output++ = *input++;
            for (; j < components; j++) *output++ = 0;
            written += info->destinationSize;
            destination += info->destinationStride;
        }
    } else {
        for (unsigned short i = 0; i < info->count; i++) {
            const unsigned char* input = source;
            unsigned short* output = reinterpret_cast<unsigned short*>(destination);
            unsigned short j;
            for (j = 0; j < copied; j++) *output++ = *input++;
            for (; j < components; j++) *output++ = 0;
            written += info->destinationSize;
            source += info->sourceStride;
            destination += info->destinationStride;
        }
    }
    return written;
}