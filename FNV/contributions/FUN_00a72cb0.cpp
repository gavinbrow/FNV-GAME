struct StreamWriter {
    void* vtable;
    unsigned int bytesWritten;
    unsigned int (__cdecl *write)(StreamWriter*, const void*, unsigned int,
                                  const unsigned int*, int);
};

struct BinaryStream {
    StreamWriter* Writer() {
        return *reinterpret_cast<StreamWriter**>(reinterpret_cast<char*>(this) + 0x24c);
    }
};

struct ColorState {
    unsigned char format;
    unsigned char flags;
    unsigned short reserved;
    unsigned int red;
    unsigned int green;
    unsigned int blue;
    unsigned int alpha;
    unsigned int threshold;
    unsigned int blendMode;

    void FUN_00a72cb0(BinaryStream* stream);
};

void ColorState::FUN_00a72cb0(BinaryStream* stream) {
    StreamWriter* __restrict writer = stream->Writer();
    {
    unsigned int elementWidth = 4;
    writer->bytesWritten += writer->write(writer, &red, 4, &elementWidth, 1);

    writer = stream->Writer();
    elementWidth = 4;
    writer->bytesWritten += writer->write(writer, &green, 4, &elementWidth, 1);

    writer = stream->Writer();
    elementWidth = 4;
    writer->bytesWritten += writer->write(writer, &blue, 4, &elementWidth, 1);

    writer = stream->Writer();
    elementWidth = 4;
    writer->bytesWritten += writer->write(writer, &alpha, 4, &elementWidth, 1);

    writer = stream->Writer();
    elementWidth = 4;
    writer->bytesWritten += writer->write(writer, &threshold, 4, &elementWidth, 1);

    writer = stream->Writer();
    elementWidth = 4;
    writer->bytesWritten += writer->write(writer, &blendMode, 4, &elementWidth, 1);

    writer = stream->Writer();
    elementWidth = 1;
    writer->bytesWritten += writer->write(writer, this, 1, &elementWidth, 1);
    }
}