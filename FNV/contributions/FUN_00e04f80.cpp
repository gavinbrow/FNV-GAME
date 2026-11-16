struct Resource_00e04f80
{
    const char* FUN_00d46d40();
    unsigned int FUN_00d470d0();
};

struct Referenced_00e04f80
{
    void FUN_00c905b0();
};

struct ListenerVTable_00e04f80;
struct Listener_00e04f80
{
    ListenerVTable_00e04f80* methods;
};
typedef void (Listener_00e04f80::*ResourceCallback_00e04f80)(Referenced_00e04f80*, const char*);
struct ListenerVTable_00e04f80
{
    ResourceCallback_00e04f80 vfunc00;
    ResourceCallback_00e04f80 vfunc04;
    ResourceCallback_00e04f80 vfunc08;
    ResourceCallback_00e04f80 vfunc0c;
    ResourceCallback_00e04f80 vfunc10;
    ResourceCallback_00e04f80 onResourceRemoved;
};

struct Manager_00e04f80
{
    virtual void vfunc00();
    virtual void vfunc04();
    virtual void removeResource(Referenced_00e04f80* owner, unsigned int resourceId);
};

struct Router_00e04f80
{
    unsigned int unk00;
    unsigned int unk04;
    unsigned int unk08;
    unsigned int unk0c;
    Manager_00e04f80* manager;
};

struct Registry_00e04f80
{
    char* FUN_00d46d80(char* status, Resource_00e04f80* resource);
};

extern Registry_00e04f80 DAT_01268748;
extern char DAT_010ea4dc;
extern char DAT_0102e388;
extern Router_00e04f80* __cdecl FUN_00c85750();

struct FUN_00e04f80_class
{
    void* vtable;
    unsigned short resourceId;
    unsigned short unk06;
    Referenced_00e04f80* owner;
    Resource_00e04f80* resource;
    Referenced_00e04f80* context;
    Listener_00e04f80* listener;

    void FUN_00e04f80();
};

void FUN_00e04f80_class::FUN_00e04f80()
{
    Resource_00e04f80* oldResource = resource;
    vtable = &DAT_010ea4dc;
    if (oldResource) {
        char status;
        if (*DAT_01268748.FUN_00d46d80(&status, oldResource)) {
            owner->FUN_00c905b0();
        } else {
            Listener_00e04f80* handler = listener;
            if (handler)
                {
                    ListenerVTable_00e04f80* methods = handler->methods;
                    ResourceCallback_00e04f80* callbackSlot = &methods->onResourceRemoved;
                    const char* name = resource->FUN_00d46d40();
                    (handler->**callbackSlot)(owner, name);
                }

            unsigned int identifier = resource->FUN_00d470d0();
            Referenced_00e04f80* savedOwner = owner;
            Router_00e04f80* router = FUN_00c85750();
            router->manager->removeResource(savedOwner, identifier);
        }
    }

    if (listener)
        ((Referenced_00e04f80*)listener)->FUN_00c905b0();
    ((volatile FUN_00e04f80_class*)this)->listener = 0;

    Referenced_00e04f80* remaining = ((volatile FUN_00e04f80_class*)this)->context;
    if (remaining)
        remaining->FUN_00c905b0();
    ((volatile FUN_00e04f80_class*)this)->context = 0;
    ((volatile FUN_00e04f80_class*)this)->vtable = &DAT_0102e388;
}
