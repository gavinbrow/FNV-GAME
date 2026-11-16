struct Format { bool* FUN_00d470f0(unsigned int*); };
struct Destination {
    virtual void v00(); virtual void v04(); virtual void v08();
    virtual void WriteDirect(void*, unsigned int, int);
    virtual void WriteFormatted(Format*, void*, unsigned int, int);
};
void __cdecl FUN_00cf6030(void* data, unsigned int size, Format* format, Destination* destination) {
    unsigned int originalSize = size;
    if (originalSize) {
        if (*format->FUN_00d470f0(&size))
            destination->WriteDirect(data, originalSize, 0);
        else
            destination->WriteFormatted(format, data, originalSize, 0);
    }
}
