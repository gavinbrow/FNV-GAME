extern int DAT_01019a34;
extern void* __cdecl FUN_0096afc0(unsigned int count);
struct ResourceDescriptor {
    void* vtable;
    void* resource;
    unsigned int count;
    unsigned int capacity;
    void* manager;
    unsigned int options;

    ResourceDescriptor* __thiscall FUN_004705e0(unsigned int initialCount, unsigned int initialOptions);
};
ResourceDescriptor* ResourceDescriptor::FUN_004705e0(unsigned int initialCount, unsigned int initialOptions) {
    vtable = &DAT_01019a34;
    count = initialCount;
    options = initialOptions;
    capacity = 0;
    manager = 0;
    if (count > 0) {
        resource = FUN_0096afc0(count);
    } else {
        resource = 0;
    }
    return this;
}