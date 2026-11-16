struct StreamCopyInfo {
    unsigned int format;
    unsigned short inputBytes;
    unsigned short unk06;
    unsigned short vertexCount;
    unsigned short unk0A;
    unsigned short* indices;
    unsigned char* source;
    unsigned int unk14;
    unsigned int sourceStride;
    unsigned int bytesPerVertex;
    unsigned int outputStride;
    unsigned int unk24;
    unsigned int unk28;
    unsigned char* destination;
};
void* __cdecl _fnv_zlib_memset(void*, int, unsigned int);

unsigned int __cdecl FUN_00e77010(StreamCopyInfo* stream)
{
    unsigned int bytesWritten = 0;
    const unsigned char* source = stream->source;
    unsigned char* destination = stream->destination;
    const unsigned short* indices = stream->indices;

    if (!source) {
        for (unsigned short vertex = 0; vertex < stream->vertexCount; ++vertex) {
            _fnv_zlib_memset(destination, 0, stream->bytesPerVertex);
            destination += stream->outputStride;
            bytesWritten += stream->bytesPerVertex;
        }
        return bytesWritten;
    }

    unsigned short availableComponents = stream->inputBytes - 8;
    unsigned short outputComponents = stream->format == 6 ? 2 : 4;
    unsigned short components = availableComponents > outputComponents
        ? outputComponents : availableComponents;

    if (indices) {
        unsigned short indexPosition = 0;
        for (unsigned short vertex = 0; vertex < stream->vertexCount; ++vertex) {
            const unsigned char* input = source + indices[indexPosition++] * stream->sourceStride;
            unsigned short* output = (unsigned short*)destination;
            unsigned short copied = 0;
            for (; copied < components; ++copied) {
                *output++ = *(const unsigned short*)input;
                input += 4;
            }
            for (; copied < outputComponents; ++copied)
                *output++ = 0;
            destination += stream->outputStride;
            bytesWritten += stream->bytesPerVertex;
        }
        return bytesWritten;
    }

    for (unsigned short vertex = 0; vertex < stream->vertexCount; ++vertex) {
        const unsigned char* input = source;
        unsigned short* output = (unsigned short*)destination;
        unsigned short copied = 0;
            for (; copied < components; ++copied) {
            *output++ = *(const unsigned short*)input;
            input += 4;
        }
        for (; copied < outputComponents; ++copied)
                *output++ = 0;
        source += stream->sourceStride;
        destination += stream->outputStride;
        bytesWritten += stream->bytesPerVertex;
    }
    return bytesWritten;
}