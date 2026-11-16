struct ConsoleOutput {
    void FUN_00456b10(char* buffer);
};
extern ConsoleOutput* DAT_011dea10;
bool __cdecl FUN_005accb0(const void* parameters, const char* scriptText, unsigned int& offset, void* subject, void* target, void* script, void* locals, char* message);
bool __cdecl FUN_005b9300(const void* parameters, const char* scriptText, void* subject, void* target, void* script, void* locals, double& result, unsigned int& offset) {
    char message[512];
    if (!FUN_005accb0(parameters, scriptText, offset, subject, target, script, locals, message)) {
        return false;
    }
    DAT_011dea10->FUN_00456b10(message);
    return true;
}