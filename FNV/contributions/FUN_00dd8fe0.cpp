struct DD8FE0_Writer {
    virtual void v0();
    virtual void v1();
    virtual void v2();
    virtual void v3();
    virtual void Write(void* buffer, int bytes);
};
struct DD8FE0_Stream {
    int m_00;
    int m_04;
    DD8FE0_Writer* m_writer;
    unsigned char m_swapByteOrder;
    void FUN_00dd8fe0(void* data, int itemSize, int itemCount);
};
static __forceinline void swapByte(unsigned char& low, unsigned char& high) { unsigned char temp = low; low = high; high = temp; }
void DD8FE0_Stream::FUN_00dd8fe0(void* data, int itemSize, int itemCount) {
    m_writer->Write(data, itemSize * itemCount);
    if (m_swapByteOrder) {
        unsigned char* buffer = static_cast<unsigned char*>(data);
        switch (itemSize) {
        case 2:
            if (itemCount > 0) do {
                swapByte(buffer[0], buffer[1]);
                buffer += 2;
            } while (--itemCount);
            break;
        case 4:
            if (itemCount > 0) {
                unsigned char* p = buffer + 2;
                do {
                    swapByte(p[-2], p[1]);
                    swapByte(p[-1], p[0]);
                    p += 4;
                } while (--itemCount);
            }
            break;
        case 8:
            if (itemCount > 0) {
                unsigned char* p = buffer + 6;
                do {
                    swapByte(p[-6], p[1]);
                    swapByte(p[-5], p[0]);
                    swapByte(p[-4], p[-1]);
                    swapByte(p[-3], p[-2]);
                    p += 8;
                } while (--itemCount);
            }
            break;
        }
    }
}
