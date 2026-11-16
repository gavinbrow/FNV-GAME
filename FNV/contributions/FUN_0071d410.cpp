
struct ConsoleLine { const char* FUN_00559450(); };
struct ConsoleLines {
    void* head; void* tail; int count;
    void* FUN_00559450();
    void* FUN_007b52d0(void* node);
    ConsoleLine* FUN_006317a0(void* node);
};
struct ConsoleTextRenderer {
    void FUN_00a0f8b0(const char* text, float x, float y, int color, int state, float opacity, int alignment, int style);
};
ConsoleTextRenderer* __cdecl FUN_00a0d9e0(int mode);
extern float _DAT_01012054;
struct ConsoleDisplay {
    void* compiler;
    ConsoleLines strings, inputs;
    int iInputsPos, iNumStrings, iLastString, menuMode, iConsoleLineSpacing, iConsoleXPos, iConsoleYPos;
    void FUN_0071d410();
};
void ConsoleDisplay::FUN_0071d410() {
    void* node = strings.FUN_00559450();
    int lineY = iConsoleYPos - DAT_011d8cfc.Int()->i * iConsoleLineSpacing;
    int lastLine = iLastString;
    int lineIndex = lastLine - DAT_011d8cfc.Int()->i;
    while (lineIndex < 0) {
        FUN_00a0d9e0(1)->FUN_00a0f8b0(0, (float)iConsoleXPos, (float)lineY, 1, -1, _DAT_01012054, 0, 0);
        ++lineIndex;
        lineY += iConsoleLineSpacing;
    }
    for (int skipped = 0; skipped < lineIndex; ++skipped)
        node = strings.FUN_007b52d0(node);
    while (lineIndex < lastLine) {
        FUN_00a0d9e0(1)->FUN_00a0f8b0(strings.FUN_006317a0(node)->FUN_00559450(),
            (float)iConsoleXPos, (float)lineY, 1, -1, _DAT_01012054, DAT_011d8d38.Int()->i, 0);
        node = strings.FUN_007b52d0(node);
        ++lineIndex;
        lineY += iConsoleLineSpacing;
    }
}