#include <windows.h>
#include <intrin.h>
extern DWORD DAT_0126835c;
extern const char str_010cd380[];
extern const char str_010cd378[];
extern const char str_010cd36c[];
extern const char str_01076f38[];
extern void __cdecl FUN_00cb6f30(void*);
struct TraceBuffer { int unk00; unsigned char* current; int unk08; unsigned char* end; };
struct TraceEntry16 { volatile unsigned int type; volatile unsigned int timestamp; unsigned int unk08; volatile unsigned int detail; };
struct TraceEntry12 { volatile unsigned int type; volatile unsigned int timestamp; unsigned int unk08; };
struct FUN_00d0b280_cls {
    int unk00; int unk04; int unk08; float unk0c;
    void FUN_00d0b280(float* first, float* second);
    void FUN_00d0b3e0(float* first, float* second);
};
void FUN_00d0b280_cls::FUN_00d0b280(float* first, float* second) {
    TraceBuffer* buffer = (TraceBuffer*)TlsGetValue(DAT_0126835c);
    unsigned char* current = buffer->current;
    if (current < buffer->end) {
        volatile TraceEntry16* entry = (volatile TraceEntry16*)current;
        entry->type = (unsigned int)str_010cd380;
        entry->detail = (unsigned int)str_010cd378;
        _ReadWriteBarrier();
        volatile unsigned int timestamp = (unsigned int)__rdtsc();
        entry->timestamp = timestamp;
        current += 16;
        buffer->current = current;
    }
    FUN_00cb6f30(first);
    if (*second >= unk0c) {
        buffer = (TraceBuffer*)TlsGetValue(DAT_0126835c);
        current = buffer->current;
        if (current < buffer->end) {
            volatile TraceEntry12* entry = (volatile TraceEntry12*)current;
            entry->type = (unsigned int)str_010cd36c;
            _ReadWriteBarrier();
            volatile unsigned int timestamp = (unsigned int)__rdtsc();
            entry->timestamp = timestamp;
            current += 12;
            buffer->current = current;
        }
        FUN_00d0b3e0(first, second);
    }
    buffer = (TraceBuffer*)TlsGetValue(DAT_0126835c);
    current = buffer->current;
    if (current < buffer->end) {
        volatile TraceEntry12* entry = (volatile TraceEntry12*)current;
        entry->type = (unsigned int)str_01076f38;
        _ReadWriteBarrier();
        volatile unsigned int timestamp = (unsigned int)__rdtsc();
        entry->timestamp = timestamp;
        current += 12;
        buffer->current = current;
    }
}
