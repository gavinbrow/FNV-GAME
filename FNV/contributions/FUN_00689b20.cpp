struct DataModel {
    void* __thiscall FUN_0043b230();
};
struct DataHandle {
    DataModel* __thiscall FUN_00559450();
};
struct GlobalState {
    bool __thiscall FUN_00862110();
    void* __thiscall FUN_004fd3e0();
};
struct LoggingFlag {
    unsigned char* __thiscall FUN_00408d60();
};
struct LoggingObject {
    void** vtable;
};
struct ParticleEffect {
    unsigned int m_a;
    unsigned int m_b;
    unsigned int m_c;
    unsigned int m_d;
    unsigned int m_e;
    unsigned int m_f;
    DataHandle handle;
    char const* filename;
    unsigned short __thiscall FUN_006828e0();
    unsigned short __thiscall FUN_00689b20();
};
extern GlobalState* DAT_011de45c;
extern LoggingFlag DAT_011de4e8;
extern char DAT_01012c78[];
extern char DAT_01012cb0[];
extern char DAT_01069d20[];
extern "C" int __cdecl FUN_0044a670(char const*);
extern "C" void* __cdecl FUN_00653270(void*, void*);
extern "C" unsigned short __cdecl FUN_0055fdb0(void*);
extern "C" LoggingObject* __cdecl FUN_004839c0(void*);
extern "C" void __cdecl FUN_0040fbe0(char const*, ...);
typedef void* (__thiscall *LogMethod)(LoggingObject*);
unsigned short ParticleEffect::FUN_00689b20() {
    unsigned short previous = 0;
    unsigned short total = previous;
    if (DAT_011de45c->FUN_00862110()) {
        previous += 4;
        previous += 2;
    }
    previous += FUN_006828e0();
    previous += 1;
    previous += FUN_0044a670(filename);
    previous += 0x10;
    previous += 0xc;
    previous += 4;
    previous += 2;
    void* active = FUN_00653270(&DAT_011f36ac, handle.FUN_00559450()->FUN_0043b230());
    if (active != 0) {
        previous += FUN_0055fdb0(active);
    }
    if (*DAT_011de4e8.FUN_00408d60()) {
        void* entry = DAT_011de45c->FUN_004fd3e0();
        if (entry) {
            LoggingObject* writer = FUN_004839c0(*(void**)entry);
            FUN_0040fbe0(DAT_01012cb0, previous - total, *(void**)entry,
                         ((LogMethod*)writer->vtable)[76](writer),
                         *(void**)((char*)entry + 5), 0x174, DAT_01069d20);
        } else {
            FUN_0040fbe0(DAT_01012c78, previous - total, 0x174, DAT_01069d20);
        }
    }
    return previous;
}