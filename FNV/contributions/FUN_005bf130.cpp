// Reconstructed by GPT-6 from the FUN_005bf130 packet, no prior source supplied.
struct SCRIPT_PARAMETER;
struct TESObjectREFR;
struct Script;
struct ScriptLocals;
struct QuestEffect;
struct FormIterator;
struct SelectedEntry;
struct GameState;
struct StateComponent;

extern bool __cdecl FUN_005accb0(const SCRIPT_PARAMETER*, const char*, unsigned int*, TESObjectREFR*, TESObjectREFR*, Script*, ScriptLocals*, char*);
extern void __cdecl FUN_00b4f450(int);
extern void __cdecl FUN_005bf7f0(int);
extern int __cdecl FUN_0044a670(char*);
extern int __cdecl FUN_004dc060(int);
extern bool __cdecl FUN_005bf7b0();
extern void __cdecl FUN_005bf770(int);
extern int __cdecl FUN_004bc3e0();
extern void __cdecl FUN_004bc3d0(unsigned short);
extern int __cdecl FUN_004a8f20(int, int);
extern int __cdecl FUN_00647b70(int,int);
extern void __cdecl FUN_00b557d0();
extern void __cdecl FUN_005bf840(int);
extern void __cdecl FUN_00451570(int);
extern int __cdecl FUN_00ec7ec0(const char*, const char*, unsigned int);
extern int __cdecl FUN_00eca6d3(const char*);
extern FormIterator* __cdecl FUN_00450b80(int);
extern unsigned int DAT_011f91b0;
extern unsigned char DAT_011f9441;
extern unsigned char DAT_011ad80d;
extern int DAT_011ad828;
extern const char DAT_0103a478[];
extern const char DAT_0103a470[];
extern const char DAT_0103a46c[];
extern const char DAT_0103a468[];
extern const char DAT_0103a464[];
extern const char DAT_0103a460[];
extern const char DAT_0103a45c[];
extern const char DAT_0103a454[];

struct SelectedEntry {
    int FUN_005bf820();
    bool FUN_008d8220();
    void FUN_005bf800(bool);
};
struct FormIterator {
    SelectedEntry* FUN_00b5afc0();
    SelectedEntry* FUN_00b5b010();
};
struct StateComponent {
    void FUN_004baf10();
};
struct GameState {
    StateComponent* FUN_0044ddc0();
};
typedef int (__thiscall *GetRefValueFn)(TESObjectREFR*);

bool __cdecl FUN_005bf130(
    const SCRIPT_PARAMETER* parameters, const char* scriptData,
    TESObjectREFR* reference, TESObjectREFR* container,
    Script* script, ScriptLocals* locals, double* result,
    unsigned int* opcodeOffset)
{
    char extracted[512];
    if (!FUN_005accb0(parameters, scriptData, opcodeOffset, reference,
                      container, script, locals, extracted))
        return false;
    char* command = extracted;
    unsigned short flags = 0;
    if (command && command[0] == '1') {
        flags |= 1;
        FUN_00b4f450(0);
        FUN_005bf7f0(0);
        if (FUN_0044a670(extracted) == 1) {
            flags |= 2;
            flags |= 4;
            flags |= 8;
            flags |= ((FUN_004dc060(0) < 2) - 1) & 0x20;
        }
    } else if (command && command[0] == '2') {
        flags = 1;
        FUN_005bf7f0(1);
    } else if (command && command[0] == '3') {
        flags = 1;
        FUN_005bf7f0(2);
    } else if (command && command[0] == '4') {
        flags |= 1;
        FUN_00b4f450(3);
        FUN_005bf7f0(0);
        if (FUN_0044a670(extracted) == 1) {
            flags |= 2;
            flags |= 4;
            flags |= 8;
            flags |= ((FUN_004dc060(0) < 2) - 1) & 0x20;
        }
    } else if (command && command[0] == '5') {
    } else if (FUN_00ec7ec0(DAT_0103a478, command, 3) == 0) {
        flags = 1;
        FUN_005bf7f0(4);
    } else if (FUN_00ec7ec0(DAT_0103a470, command, 7) == 0) {
        flags = 1;
        FUN_005bf7f0(5);
    } else if (FUN_00ec7ec0(DAT_0103a46c, command, 2) == 0) {
        if (command[2] == '\0') {
            bool enabled = FUN_005bf7b0();
            FUN_005bf770(!enabled);
            flags = FUN_004bc3e0();
            if ((flags & 0x80) == 0)
                flags |= 0x80;
            else
                flags &= ~0x80;
        } else {
            int state = int(command[2]) - '0';
            if (state == 1 || state == 2)
                state = 3;
            DAT_011f91b0 = FUN_00647b70(0, FUN_004a8f20(3, state));
            FUN_00b557d0();
            flags = FUN_004bc3e0();
            flags |= 0x80;
        }
    } else if (FUN_00ec7ec0(DAT_0103a468, command, 2) == 0) {
        unsigned char priorToggle = DAT_011f9441;
        DAT_011f9441 = priorToggle ? 0 : 1;
        flags = FUN_004bc3e0();
    } else if (FUN_00ec7ec0(DAT_0103a464, command, 2) == 0) {
        bool isEnabled = (FUN_004bc3e0() & 0x20) > 0;
        if (!isEnabled) {
            FUN_005bf840(1);
            ((GameState*)DAT_011dea10)->FUN_0044ddc0()->FUN_004baf10();
            unsigned short activeFlags = FUN_004bc3e0();
            activeFlags |= 0x20;
            FUN_004bc3d0(activeFlags);
        } else {
            FUN_005bf840(0);
            FUN_00451570(0);
            unsigned short activeFlags = FUN_004bc3e0();
            activeFlags &= ~0x20;
            FUN_004bc3d0(activeFlags);
        }
        return true;
    } else if (command[0] == 't') {
        int parsedTime = FUN_00eca6d3(command + 1);
        DAT_011ad828 = parsedTime;
    } else if (FUN_00ec7ec0(DAT_0103a460, command, 3) == 0) {
        if (reference) {
            FormIterator* iterator = FUN_00450b80(0);
            SelectedEntry* current = iterator->FUN_00b5afc0();
            while (current) {
                if (current->FUN_005bf820() == ((GetRefValueFn*)(*(void***)reference))[116](reference))
                    current->FUN_005bf800(!current->FUN_008d8220());
                current = iterator->FUN_00b5b010();
            }
        }
        return true;
    } else if (FUN_00ec7ec0(DAT_0103a45c, command, 3) == 0) {
        DAT_011ad80d = DAT_011ad80d ? 0 : 1;
        flags = FUN_004bc3e0();
        flags |= 0x100;
    } else if (FUN_00ec7ec0(DAT_0103a454, command, 5) == 0) {
        return true;
    }

    ++command;
    if (command && command[0] == '1')
        flags |= 2;
    ++command;
    if (command && command[0] == '1')
        flags |= 4;
    ++command;
    if (command && command[0] == '1')
        flags |= 8;
    if (FUN_004dc060(0) >= 2) {
        ++command;
        if (!command || command[0] != '0')
            flags |= 0x20;
    }
    FUN_004bc3d0(flags);
    return true;
}