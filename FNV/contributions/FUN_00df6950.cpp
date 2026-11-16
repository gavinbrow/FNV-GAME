#include <windows.h>
#include <intrin.h>
struct ProfileEvent {
    const void* volatile label;
    unsigned int cycles;
    unsigned int extra;
};
struct ThreadProfile {
    void* owner;
    ProfileEvent* next;
    unsigned int capacity;
    ProfileEvent* end;
};
struct WorkItem {
    unsigned int unk00, unk04, unk08, unk0c;
    unsigned int unk10, unk14, unk18, unk1c;
    int remaining;
    unsigned int value;
    int processed;
    unsigned int unk2c;
};
struct WorkQueue {
    unsigned int unk00, unk04, unk08, unk0c;
    unsigned int unk10, unk14, unk18, unk1c;
    unsigned int unk20;
    WorkItem* tasks;
    int taskCount;
    int processorCount;
    void* processors[1];
};
struct ExecutionContext {
    void FUN_00d04e80(WorkQueue* source, WorkQueue* target, int flags);
};
extern unsigned long DAT_0126835c;
extern "C" const char str_010db918[];
extern "C" const char str_010c41f8[];
int __cdecl FUN_00d1b930(void* processor, WorkItem* item, unsigned int* value, int remaining);
void __cdecl FUN_00df6950(ExecutionContext* context, WorkQueue* queue) {
    ThreadProfile* trace = (ThreadProfile*)TlsGetValue(DAT_0126835c);
    ProfileEvent* entry = trace->next;
    if (entry < trace->end) {
        entry->label = str_010db918;
        _ReadWriteBarrier();
        volatile unsigned int ticks = (unsigned int)__rdtsc();
        entry->cycles = ticks;
        trace->next = entry + 1;
    }
    int count = queue->taskCount;
    WorkItem* item = queue->tasks;
    if (count > 0) {
        int work = count;
        do {
            unsigned int value = item->value;
            int remaining = item->remaining;
            int n = 0;
            item->processed = 0;
            if (queue->processorCount > 0) {
                do {
                    void* processor = queue->processors[n];
                    if (processor) {
                        int consumed = FUN_00d1b930(processor, item, &value, remaining);
                        item->processed += consumed;
                        remaining -= consumed;
                    }
                    ++n;
                } while (n < queue->processorCount);
            }
            ++item;
        } while (--work != 0);
    }
    trace = (ThreadProfile*)TlsGetValue(DAT_0126835c);
    entry = trace->next;
    if (entry < trace->end) {
        entry->label = str_010c41f8;
        _ReadWriteBarrier();
        volatile unsigned int ticks = (unsigned int)__rdtsc();
        entry->cycles = ticks;
        trace->next = entry + 1;
    }
    context->FUN_00d04e80(queue, queue, 0);
}
