
struct ScriptCommandView {
    const char* longName;
    const char* shortName;
    unsigned int opcode;
    const char* helpText;
    unsigned int commandFlags;
    void* parameters;
    void* execute;
    void* parse;
    void* evaluate;
    void* reserved;
};
struct ScriptWordView {
    char text[0x200];
    unsigned int referencedObjectIndex;
    char variableType;
    unsigned int functionCode;
};
extern ScriptCommandView DAT_0118cb50[];
int __cdecl FUN_00404dc0(const char*, const char*);

bool __cdecl FUN_005b1910(ScriptWordView* word)
{
    int index;
    for (index = 0; index < 16; ++index) {
        if (FUN_00404dc0(DAT_0118cb50[index].longName, word->text) == 0 ||
            FUN_00404dc0(DAT_0118cb50[index].shortName, word->text) == 0) {
            word->variableType = 'X';
            word->functionCode = DAT_0118cb50[index].opcode;
            return true;
        }
    }
    for (index = 0; index < 640; ++index) {
        if (FUN_00404dc0(word->text, reinterpret_cast<ScriptCommandView*>(g_scriptCommands)[index].longName) == 0 ||
            FUN_00404dc0(word->text, reinterpret_cast<ScriptCommandView*>(g_scriptCommands)[index].shortName) == 0) {
            word->variableType = 'X';
            word->functionCode = reinterpret_cast<ScriptCommandView*>(g_scriptCommands)[index].opcode;
            return true;
        }
    }
    for (index = 0; index < 205; ++index) {
        if (FUN_00404dc0(word->text, reinterpret_cast<ScriptCommandView*>(DAT_0118e8e0)[index].longName) == 0 ||
            FUN_00404dc0(word->text, reinterpret_cast<ScriptCommandView*>(DAT_0118e8e0)[index].shortName) == 0) {
            word->variableType = 'X';
            word->functionCode = reinterpret_cast<ScriptCommandView*>(DAT_0118e8e0)[index].opcode;
            return true;
        }
    }
    return false;
}
