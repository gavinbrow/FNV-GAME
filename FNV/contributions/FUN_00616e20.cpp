int __cdecl FUN_00406d50(char* destination, unsigned int capacity, const char* source);
extern const char DAT_01013444[];
extern const char DAT_01044c28[];

struct OutputStringDC {
    void FUN_00438390(const char* text);
};

struct FUN_00616e20_shell {
    bool FUN_00616e20(OutputStringDC* output, const char* first, const char* second, const char* third, const char* fourth, const char* fifth);
};

bool FUN_00616e20_shell::FUN_00616e20(OutputStringDC* output, const char* first, const char* second, const char* third, const char* fourth, const char* fifth)
{
    bool succeeded2;
    char buffer[260];
    char* destination = buffer;
    destination[0] = 0;
    FUN_00406d50(destination, 260, first);
    FUN_00406d50(destination, 260, DAT_01013444);
    FUN_00406d50(destination, 260, second);
    FUN_00406d50(destination, 260, DAT_01013444);
    FUN_00406d50(destination, 260, third);
    FUN_00406d50(destination, 260, DAT_01013444);
    FUN_00406d50(destination, 260, fourth);
    FUN_00406d50(destination, 260, DAT_01044c28);
    FUN_00406d50(destination, 260, fifth);
    succeeded2 = true;
    output->FUN_00438390(buffer);
    return succeeded2;
}
