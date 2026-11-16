struct Buffer { unsigned short* data; unsigned int byteSize; };
void __cdecl FUN_00e31800(unsigned int, Buffer*);
void __cdecl FUN_00e31ad0(unsigned short value, Buffer* buffer) {
    FUN_00e31800(2, buffer);
    *(unsigned short*)((char*)buffer->data + buffer->byteSize - 2) = value;
}

