typedef int (__cdecl *StreamIoFn)(void*, void*, unsigned int, unsigned int*, unsigned int);
struct StreamFor87520 {
    unsigned int unk00;
    unsigned int bytes;
    unsigned int unk08;
    StreamIoFn io;
};
void __stdcall FUN_00a71d10(void* owner);
struct FUN_00a87520_shell : Target {
    void FUN_00a87520(void* owner);
};
void FUN_00a87520_shell::FUN_00a87520(void* owner) {
    FUN_00a71d10(owner);
    StreamFor87520* stream = *(StreamFor87520**)((char*)owner + 0x250);
    {
        unsigned int countBytes = 4;
        stream->bytes += stream->io(stream, &unkC8, 4, &countBytes, 1);
    }
    unsigned int index = 0;
    if ((unsigned int)unkC8 <= 0u)
        return;
    unsigned int offset = 0;
    do {
        {
            unsigned char flag = 0;
            stream = *(StreamFor87520**)((char*)owner + 0x250);
            {
                unsigned int readBytes = 1;
                stream->bytes += stream->io(stream, &flag, 1, &readBytes, 1);
            }
        }
        stream = *(StreamFor87520**)((char*)owner + 0x250);
        {
            void* firstField = (char*)entries + offset;
            unsigned int fieldBytes = 4;
            stream->bytes += stream->io(stream, firstField, 4, &fieldBytes, 1);
        }
        stream = *(StreamFor87520**)((char*)owner + 0x250);
        {
            void* secondField = (char*)entries + offset + 4;
            unsigned int otherFieldBytes = 4;
            stream->bytes += stream->io(stream, secondField, 4, &otherFieldBytes, 1);
        }
        ++index;
        offset += 0x14;
    } while (index < (unsigned int)unkC8);
}