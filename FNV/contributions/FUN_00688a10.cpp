struct GlobalRuntime {
    bool __thiscall FUN_00862110();
    char* __thiscall FUN_004fd3e0();
};

struct FeatureState {
    unsigned char* __thiscall FUN_00408d60();
};

extern GlobalRuntime* DAT_011de45c;
extern FeatureState DAT_011de4e8;
extern char str_01012c78;
extern char str_01012cb0;
extern char str_01069ba0;

void* __cdecl FUN_004839c0(void* object);
void __cdecl FUN_0040fbe0(const char* format, ...);

typedef unsigned int (__fastcall *VirtualQuery)(void* object);

struct RuntimeController {
    unsigned short FUN_00688a10();
};

unsigned short RuntimeController::FUN_00688a10()
{
    unsigned short currentFlags = 0;
    unsigned short savedFlags = currentFlags;

    if (DAT_011de45c->FUN_00862110()) {
        currentFlags += 4;
        currentFlags += 2;
    }

    if (*DAT_011de4e8.FUN_00408d60()) {
        char* current = DAT_011de45c->FUN_004fd3e0();
        if (current) {
            void* related = FUN_004839c0(*reinterpret_cast<void**>(current));
            FUN_0040fbe0(&str_01012cb0, currentFlags - savedFlags,
                *reinterpret_cast<void**>(current),
                reinterpret_cast<VirtualQuery>(
                    (*reinterpret_cast<void***>(related))[0x4c])(related),
                *reinterpret_cast<unsigned int*>(current + 5),
                0x72f, &str_01069ba0);
        } else {
            FUN_0040fbe0(&str_01012c78, currentFlags - savedFlags, 0x72f,
                &str_01069ba0);
        }
    }
    return currentFlags;
}
