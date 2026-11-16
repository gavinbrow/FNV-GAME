void* __cdecl FUN_0056d280(unsigned int size);

void* __cdecl FUN_00401460(void* destination, const void* source, unsigned int size);



struct Buffer538c00

{

    unsigned int m00;

    unsigned int m04;

    void __thiscall FUN_00540750(unsigned int size);

    void* __thiscall FUN_00559450();

};



struct Output538c00

{

    virtual ~Output538c00();

    unsigned int m04;

    unsigned int m08;

    unsigned int m0c;

    unsigned int m10;

    unsigned int m14;

    unsigned int m18;

    unsigned int m1c;

    Buffer538c00 buffer;

    unsigned int m28;

    unsigned int m2c;

    Output538c00();
    static void* operator new(unsigned int bytes) { return FUN_0056d280(bytes); }

};



struct FUN_00538c00_Class

{

    char __thiscall FUN_00538c00(const void* source, unsigned int size, Output538c00** result);

};



char __thiscall FUN_00538c00_Class::FUN_00538c00(
    const void* source, unsigned int size, Output538c00** result)
{
    unsigned char success = 0;
    if (source && size && result)
    {
        Output538c00* object = new Output538c00;
        *result = object;

        const char* remainingSize = static_cast<const char*>(source);
        unsigned int readPosition = size;
        unsigned int fixedHeaderSize = 0x10;
        if (readPosition > fixedHeaderSize)
        {
            FUN_00401460(&object->m10, remainingSize, fixedHeaderSize);
            readPosition = readPosition - fixedHeaderSize;
            remainingSize = remainingSize + fixedHeaderSize;
            if (readPosition > 0)
            {
                object->buffer.FUN_00540750(readPosition);
                void* bufferData = object->buffer.FUN_00559450();
                FUN_00401460(bufferData, remainingSize, readPosition);
                success = 1;
            }
        }
        if (!success)
        {
            delete object;
            *result = 0;
        }
    }
    return success;
}