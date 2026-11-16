extern "C" void* __cdecl memmove(void* destination, const void* source, unsigned int size);
unsigned int __cdecl _access_s(const void* buffer, unsigned int itemSize, unsigned int count, void* file);

class NiFile
{
    unsigned char m_padding[0x10];
    unsigned int m_bufferSize;
    unsigned int m_bufferEnd;
    unsigned int m_bufferPosition;
    unsigned int m_filePosition;
    unsigned char* m_buffer;
    void* m_file;
    unsigned char m_reserved[4];
    unsigned char m_isOpen;

protected:
    bool Flush();

public:
    unsigned int FUN_00aa1750(void* destination, unsigned int count);
};

// @fnv 0x00aa1750
unsigned int NiFile::FUN_00aa1750(void* destination, unsigned int count)
{
    if (m_isOpen != 0)
    {
        unsigned int available = m_bufferEnd - m_bufferPosition;
        unsigned int copied = 0;

        if (count > available)
        {
            if (available > 0)
            {
                memmove(destination, m_buffer + m_bufferPosition, available);
                destination = static_cast<unsigned char*>(destination) + available;
                count -= available;
                copied = available;
            }

            Flush();

            if (count > m_bufferSize)
            {
                unsigned int bytesRead = _access_s(destination, 1, count, m_file);
                m_filePosition += bytesRead;
                return bytesRead + copied;
            }

            unsigned char* refillBuffer = m_buffer;
            unsigned int bytesRead = _access_s(refillBuffer, 1, m_bufferSize, m_file);
            m_filePosition += bytesRead;
            m_bufferEnd = bytesRead;
            if (bytesRead < count)
            {
                count = bytesRead;
            }
        }

        memmove(destination, m_buffer + m_bufferPosition, count);
        m_bufferPosition += count;
        return copied + count;
    }

    return 0;
}
