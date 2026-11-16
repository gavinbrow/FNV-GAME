struct BufferedStreamDestination {
    virtual void vfn_0000();
    virtual void vfn_0004();
    virtual void vfn_0008();
    virtual void vfn_000c();
    virtual int Write(const void* source, int bytes);
};
struct StreamBufferD27210 {
    void* unk00;
    void* unk04;
    BufferedStreamDestination* m_destination;
    char* m_buffer;
    int m_position;
    int m_end;
    int FUN_00d27210();
};
int StreamBufferD27210::FUN_00d27210()
{
    if (m_destination != 0) {
        int written = 0;
        int remaining = m_position;
        while (written < remaining) {
            int count = m_destination->Write(m_buffer + written, remaining - written);
            written += count;
            if (count == 0)
                return written;
        }
        m_position = 0;
        return written;
    }
    return 0;
}
