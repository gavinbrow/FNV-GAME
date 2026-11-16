struct EventRecord {
    unsigned char type;
    unsigned char dispatchId;
    unsigned char unk02;
    unsigned char unk03;
    unsigned char unk04;
    unsigned char unk05;
    unsigned char unk06;
    unsigned char unk07;
    void* value08;
    void* unk0c;
    void* source10;
    void* target14;
    int unk18;
    int unk1c;
    void* data20;
    int unk24;
    int unk28;
    int unk2c;
    void* data30;
};
struct EventArrayEntry {
    EventRecord* record;
    unsigned int unk04;
};
struct EventArray {
    EventArrayEntry* data;
    int count;
    int capacity;
};
struct SourceObject {
    void __thiscall FUN_00d08260(EventArray* events);
};
struct EventSource {
    int unk00;
    int unk04;
    int unk08;
    int unk0c;
    SourceObject events;
};
struct DispatchContext {
    void* table;
};
typedef void (__cdecl *EventHandler)(void*, void*, void*, void*, void*, void*, void*);
struct MemoryAllocator {
    virtual void unk00();
    virtual void unk04();
    virtual void unk08();
    virtual void unk0c();
    virtual void Free(void* pointer, unsigned int bytes);
};
struct BSAudio {
    int unk00;
    int unk04;
    int unk08;
    int unk0c;
    MemoryAllocator* volatile allocator;
};
extern BSAudio* __cdecl FUN_00c85750();
void __cdecl FUN_00cc1190(EventSource* source, DispatchContext* context) {
    EventArray events;
    events.data = 0;
    events.count = 0;
    events.capacity = (int)0x80000000;
    source->events.FUN_00d08260(&events);
    int index = 0;
    if (events.count > 0) {
        do {
            EventRecord* event = events.data[index].record;
            unsigned char handlerIndex = event->dispatchId;
            EventHandler handler = *(EventHandler*)((char*)context->table + 0x16c8 + handlerIndex * 0x50);
            if (handler) {
                void* sourceObject = event->source10;
                void* target = event->target14;
                char sourceOffset = *((char*)sourceObject + 0x10);
                void* sourceField = (char*)sourceObject + sourceOffset;
                void* argument = *((char*)sourceField + 0xe8) == 5
                    ? *(void**)((char*)target + *((char*)target + 0x10) + 0xcc)
                    : *(void**)((char*)sourceField + 0xcc);
                void* eventData = event->type == 4 ? (char*)event + 0x30 : (char*)event + 0x20;
                handler(event, eventData, sourceObject, target, context, event->value08, argument);
            }
            ++index;
        } while (index < events.count);
    }
    BSAudio* audio = FUN_00c85750();
    MemoryAllocator* allocator = audio->allocator;
    events.count = 0;
    if (!(events.capacity & (int)0x80000000))
        allocator->Free(events.data, (events.capacity & 0x3fffffff) * 8);
}




