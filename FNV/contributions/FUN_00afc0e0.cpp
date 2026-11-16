#include <string.h>
int __cdecl FUN_00b44000(z_stream_s* state, int flush);
int __cdecl FUN_00b45db0(z_stream_s* state);
struct DecompReadFile : public CompressedArchiveFile {
    void FUN_00aa15a0();
    unsigned int FUN_00afb7a0(void* buffer, unsigned int size, int mode);
    unsigned int FUN_00afc0e0(char* buffer, unsigned int size);
};
unsigned int DecompReadFile::FUN_00afc0e0(char* buffer, unsigned int size)
{
    unsigned int bytesToRead = size;
    unsigned int nRead = 0;
    z_stream_s* state = (z_stream_s*)pZStream;
    unsigned int available = iUncompressedBufferReadSize - iUncompressedBufferPos;

    if (bytesToRead > available) {
        if (available > 0) {
            if (buffer != 0) {
                char* copyFrom = pUncompressedBuffer + iUncompressedBufferPos;
                memcpy(buffer, copyFrom, available);
                buffer += available;
            }
            bytesToRead -= available;
            nRead = available;
        }
        iUncompressedBufferPos = 0;
        iUncompressedBufferReadSize = 0;

        int status;
        while (bytesToRead > 0) {
            state->avail_out = iUncompressedBufferSize;
            state->next_out = (unsigned char*)pUncompressedBuffer;

            while (state->avail_out != 0) {
                available = m_uiBufferReadSize - m_uiPos;
                state->avail_in = available;
                state->next_in = (unsigned char*)(m_pBuffer + m_uiPos);

                if (available != 0) {
                    status = FUN_00b44000(state, 2);
                    if (status == -2 || status == 2 || status == -3 || status == -4) {
                        FUN_00b45db0(state);
                        bytesToRead = 0;
                        break;
                    }
                    if (status == 1)
                        break;
                }
                m_uiPos += available - state->avail_in;
                iTrueFilePos += available - state->avail_in;
                if (state->avail_in == 0) {
                    FUN_00aa15a0();
                    m_uiBufferReadSize = FUN_00afb7a0(m_pBuffer, m_uiBufferAllocSize, 0);
                }
            }

            iUncompressedBufferReadSize = iUncompressedBufferSize - state->avail_out;
            if (iUncompressedBufferReadSize == 0) {
                break;
            } else {
            if (bytesToRead > iUncompressedBufferReadSize) {
                bytesToRead -= iUncompressedBufferReadSize;
                nRead += iUncompressedBufferReadSize;
                if (buffer != 0) {
                    unsigned int amount = iUncompressedBufferReadSize;
                    char* copyFrom = pUncompressedBuffer;
                    memcpy(buffer, copyFrom, amount);
                    buffer += iUncompressedBufferReadSize;
                }
            } else {
                if (buffer != 0) {
                    char* copyFrom = pUncompressedBuffer;
                    memcpy(buffer, copyFrom, bytesToRead);
                }
                iUncompressedBufferPos += bytesToRead;
                nRead += bytesToRead;
                bytesToRead = 0;
            }
            }
        }
    } else {
        if (buffer != 0) {
            char* copyFrom = pUncompressedBuffer + iUncompressedBufferPos;
            memcpy(buffer, copyFrom, bytesToRead);
        }
        iUncompressedBufferPos += bytesToRead;
        nRead += bytesToRead;
    }
    return nRead;
}