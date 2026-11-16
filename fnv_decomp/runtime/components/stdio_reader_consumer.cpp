// Original owner/consumer for the separately retained source-built read method.
// No game implementation, copied game data, manual entry or original address.
#include <windows.h>
#include <stddef.h>
#include <stdio.h>
#include <stdlib.h>

// Exact source declaration of the selected method's receiver. The selected
// method implementation is supplied only by the reviewed retained component.
struct FUN_00d2bcd0_class
{
    void* m_00;
    void* m_04;
    void* m_08;
    void* m_0c;
    char m_10;
    void __thiscall ReadOrMarkFailed(void* buffer, unsigned int count);
};

typedef char PointerWidth[(sizeof(void*) == 4 && sizeof(size_t) == 4) ? 1 : -1];
typedef char IntegerWidths[(sizeof(unsigned int) == 4 && sizeof(long) == 4) ? 1 : -1];
typedef char ReceiverLayout[(offsetof(FUN_00d2bcd0_class, m_0c) == 12 &&
                            offsetof(FUN_00d2bcd0_class, m_10) == 16 &&
                            sizeof(FUN_00d2bcd0_class) == 20) ? 1 : -1];

static const char input_text[] = "FNV source-owned reader input.\n";

int ExerciseStdioReader(FILE* stream)
{
    const long length = sizeof(input_text) - 1;
    if (fseek(stream, 0, SEEK_END) || ftell(stream) != length || fseek(stream, 0, SEEK_SET))
        return 20;
    int prefix0 = 11, prefix1 = 22, prefix2 = 33;
    FUN_00d2bcd0_class reader = {&prefix0, &prefix1, &prefix2, stream, 1};
    unsigned char buffer[16] = {0};

    reader.ReadOrMarkFailed(buffer, 4);
    if (reader.m_10 != 1 || ftell(stream) != 4 || feof(stream) || ferror(stream)) return 21;
    for (unsigned i = 0; i != 4; ++i)
        if (buffer[i] != (unsigned char)input_text[i]) return 22;

    if (fseek(stream, length - 2, SEEK_SET)) return 23;
    reader.m_10 = 1;
    reader.ReadOrMarkFailed(buffer, 8);
    if (reader.m_10 != 1 || ftell(stream) != length || !feof(stream) || ferror(stream) ||
        buffer[0] != (unsigned char)input_text[length - 2] ||
        buffer[1] != (unsigned char)input_text[length - 1]) return 24;

    reader.m_10 = 1;
    reader.ReadOrMarkFailed(buffer, 4);
    if (reader.m_10 != 0 || ftell(stream) != length || !feof(stream) || ferror(stream)) return 25;

    clearerr(stream);
    if (fseek(stream, 0, SEEK_SET)) return 26;
    reader.m_10 = 1;
    reader.ReadOrMarkFailed(buffer, 0);
    if (reader.m_10 != 0 || ftell(stream) != 0 || feof(stream) || ferror(stream)) return 27;
    if (reader.m_00 != &prefix0 || reader.m_04 != &prefix1 || reader.m_08 != &prefix2 ||
        reader.m_0c != stream || prefix0 != 11 || prefix1 != 22 || prefix2 != 33) return 28;
    return 0;
}

int main(int argc, char** argv)
{
    SetErrorMode(SEM_FAILCRITICALERRORS | SEM_NOGPFAULTERRORBOX | SEM_NOOPENFILEERRORBOX);
    _set_error_mode(_OUT_TO_STDERR);
    if (argc != 2) return 10;
    FILE* stream = fopen(argv[1], "rb");
    if (!stream) return 11;
    const int result = ExerciseStdioReader(stream);
    const int closed = fclose(stream);
    if (result) return result;
    if (closed) return 12;
    return printf("{\"component\":\"source_stdio_reader\",\"calls\":4,\"cases\":4,\"closed\":true}\n") < 0 ? 13 : 0;
}
