struct ScriptVariableValue {
    unsigned int id;
    unsigned int unknown04;
    double value;
    bool isInteger;
};
struct ScriptLocalList {
    ScriptVariableValue** FUN_006815c0();
    ScriptLocalList* FUN_00726070();
};
struct GlobalGameState {
    bool FUN_00862110();
    void* FUN_004fd3e0();
};
struct FlagManager {
    unsigned char* FUN_00408d60();
};
struct MessageProducer {
    void* unk00;
};
struct Formatter {
    unsigned int getItem(int item, unsigned int line, const char* text) {
        typedef unsigned int (__thiscall* Callback)(Formatter*, int, unsigned int, const char*);
        Callback fn = *(Callback*)(*(char**)this + 0x130);
        return fn(this,item,line,text);
    }
};
extern GlobalGameState* DAT_011de45c;
extern FlagManager DAT_011de4e8;
extern const char DAT_01036d58;
extern const char DAT_01012cb0;
extern const char DAT_01012c78;
extern Formatter* __cdecl FUN_004839c0(void* item);
extern void __cdecl FUN_0040fbe0(const char* message, ...);
struct ScriptLocalsExt : ScriptLocals { bool FUN_005a9480(unsigned int id); };
unsigned short __fastcall FUN_005a94f0(ScriptLocals* self) {
    unsigned short bytes = 0;
    unsigned short original = bytes;
    if (DAT_011de45c->FUN_00862110()) {
        bytes += 4;
        bytes += 2;
    }
    bytes += 2;
    ScriptLocalList* entry = (ScriptLocalList*)self->m_pLocalList;
    while (entry) {
        ScriptVariableValue* value = *entry->FUN_006815c0();
        if (value && value->value != 0.0) {
            if (((ScriptLocalsExt*)self)->FUN_005a9480(value->id))
                bytes += 8;
            else
                bytes += 12;
        }
        entry = entry->FUN_00726070();
    }
    bytes += 1;
    if (self->m_pScriptEffectData)
        bytes += 8;
    if (*DAT_011de4e8.FUN_00408d60()) {
        void* info = DAT_011de45c->FUN_004fd3e0();
        if (info) {
            Formatter* formatter = FUN_004839c0(*(void**)info);
            FUN_0040fbe0(&DAT_01012cb0, (unsigned int)bytes - (unsigned int)original, *(void**)info, ((TESForm*)formatter)->GetName(), *(int*)((char*)info + 5), 638, &DAT_01036d58);
        } else {
            FUN_0040fbe0(&DAT_01012c78, (unsigned int)bytes - (unsigned int)original, 638, &DAT_01036d58);
        }
    }
    return bytes;
}