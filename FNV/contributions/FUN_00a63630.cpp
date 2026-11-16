extern "C" int __cdecl strcpy_s(char* destination, unsigned int size, const char* source);
extern "C" char* __cdecl strtok_s(char* text, const char* delimiters, char** context);
extern long __cdecl FUN_00eca6d3(const char* text);

unsigned int __cdecl FUN_00a63630(const char* text)
{
    char buffer[16];
    char* context;

    strcpy_s(buffer, 16, text);
    int shift = 24;
    unsigned int value = 0;
    char* token = strtok_s(buffer, ".", &context);
    while (token)
    {
        value |= (unsigned int)(FUN_00eca6d3(token) << shift);
        shift -= 8;
        token = strtok_s(0, ".", &context);
    }
    return value;
}
