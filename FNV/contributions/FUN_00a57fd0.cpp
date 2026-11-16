extern "C" __declspec(dllimport) long __stdcall InterlockedDecrement(volatile long*);
extern "C" __declspec(dllimport) long __stdcall InterlockedIncrement(volatile long*);

struct FUN_00a57fd0_ref {
    virtual void Unknown();
    virtual void Delete();
    volatile long references;
    FUN_00a57fd0_ref* FUN_00a5d3f0(FUN_00a50110_proc&);
};
struct FUN_00a57fd0_fields {
    void* vtable;
    unsigned int state04;
    unsigned int state08;
    volatile float value0c;
    float value10;
    FUN_00a57fd0_ref* object14;
    FUN_00a57fd0_ref* object18;
    void FUN_00aa1000(FUN_00a50110_obj*, FUN_00a50110_proc&);
};

void FUN_00a50110_obj::FUN_00a57fd0(FUN_00a50110_obj* destination,
                                    FUN_00a50110_proc& cloning)
{
    FUN_00a57fd0_fields* source = reinterpret_cast<FUN_00a57fd0_fields*>(this);
    FUN_00a57fd0_fields* target = reinterpret_cast<FUN_00a57fd0_fields*>(destination);
    source->FUN_00aa1000(destination, cloning);
    target->value10 = source->value10;
    target->value0c = source->value0c;

    FUN_00a57fd0_ref* previous = *reinterpret_cast<FUN_00a57fd0_ref* volatile*>(&target->object14);
    if (previous != source->object14) {
        if (previous && InterlockedDecrement(&previous->references) == 0)
            previous->Delete();
        target->object14 = source->object14;
        if (target->object14)
            InterlockedIncrement(&target->object14->references);
    }

    if (source->object18) {
        FUN_00a57fd0_ref* clone = source->object18->FUN_00a5d3f0(cloning);
        FUN_00a57fd0_ref* existing = target->object18;
        if (existing != clone) {
            if (existing && InterlockedDecrement(&existing->references) == 0)
                existing->Delete();
            target->object18 = clone;
            if (clone)
                InterlockedIncrement(&clone->references);
        }
    }
}