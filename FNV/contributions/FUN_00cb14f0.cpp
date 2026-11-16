struct InputStream {
    virtual void v00();
    virtual void v04();
    virtual void v08();
    virtual void v0c();
    virtual int Read(void* destination, int size);
    int FUN_00cb14f0(int size);
};
int InputStream::FUN_00cb14f0(int size) {
    unsigned int buffer[128];
    int remaining = size;
    while (remaining) {
        int count = Read(buffer, remaining > 512 ? 512 : remaining);
        if (!count) break;
        remaining -= count;
    }
    return size - remaining;
}
