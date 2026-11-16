struct _iobuf;

extern "C" void* __cdecl memmove(void* destination, const void* source, unsigned int count);

// The field offsets are supported by the neighbouring NiFile read draft.
class NiFile
{
public:
    unsigned int FUN_00aa1810(const char* source, unsigned int count);

protected:
    bool Flush();
    static unsigned int __cdecl WriteBytesToFile(
        const void* source, unsigned int elementSize,
        unsigned int elementCount, _iobuf* stream);

    unsigned int unknown00;
    unsigned int unknown04;
    unsigned int unknown08;
    unsigned int unknown0c;
    unsigned int bufferCapacity;
    unsigned int bufferSize;
    unsigned int bufferPosition;
    unsigned int filePosition;
    char* buffer;
    _iobuf* stream;
    unsigned int mode;
    bool good;
};

// @fnv 0x00aa1810
unsigned int NiFile::FUN_00aa1810(const char* source, unsigned int count)
{
    if (good)
    {
        unsigned int available = bufferCapacity - bufferPosition;
        unsigned int copied = 0;
        if (count > available)
        {
            if (available > 0)
            {
                memmove(buffer + bufferPosition, source, available);
                source += available;
                count -= available;
                copied = available;
                bufferPosition = bufferCapacity;
            }
    
            if (!Flush())
            {
                return 0;
            }
    
            if (count >= bufferCapacity)
            {
                unsigned int written = WriteBytesToFile(source, 1, count, stream);
                return copied + written;
            }
        }
    
        memmove(buffer + bufferPosition, source, count);
        bufferPosition += count;
        return copied + count;
    }
    return 0;
}
