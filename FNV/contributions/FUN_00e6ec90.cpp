// Renderer resource setup: original C++ reconstructed from FUN_00e6ec90.
struct RendererStateSlot;
struct ResourceDescriptor { unsigned char unknown00; unsigned char format; };
struct RenderResource : RefObject {
    int unk08, unk0C, unk10, unk14, unk18, unk1C, unk20, unk24;
    int unk28, unk2C, unk30, unk34, unk38, unk3C, unk40, unk44;
    int unk48, unk4C;
    unsigned int dataOffset;
    unsigned int unk54, unk58;
    unsigned char** dataBase;
    RenderResource* FUN_00a7c190(int a, int b, ResourceDescriptor* d, int c, int e);
};
struct ResourceParameters {
    unsigned int count;
    unsigned int unk04;
    unsigned int unk08;
};
extern const char DAT_010edbb8[];
extern const char* DAT_0109b220;
void* __cdecl FUN_00aa13e0(unsigned int size);
const char* __cdecl FUN_00a5b690(const char* name);
RefObject* __cdecl FUN_00a5ff10(RenderResource* resource, const char* name, ResourceParameters* parameters);
struct RendererBridge {
    RendererStateSlot* State(unsigned int idx) {
        return reinterpret_cast<RendererStateSlot*>(reinterpret_cast<char*>(this) + 0x700 + 0x58 * idx);
    }
    ResourceDescriptor* Source() {
        return *reinterpret_cast<ResourceDescriptor**>(reinterpret_cast<char*>(this) + 0x860);
    }
    RefObject*& Target() {
        return *reinterpret_cast<RefObject**>(reinterpret_cast<char*>(this) + 0x8fc);
    }
    void FUN_00e6dfc0(RendererStateSlot* state, unsigned int type, unsigned int flags);
    void FUN_00e6c550();
    bool FUN_00e6ec90();
};
bool RendererBridge::FUN_00e6ec90() {
    FUN_00e6dfc0(State(0), 0, 3);
    FUN_00e6dfc0(State(1), 1, 3);
    FUN_00e6dfc0(State(2), 0, 5);
    FUN_00e6dfc0(State(3), 1, 5);
    FUN_00e6c550();

    ResourceDescriptor* source = Source();
    void* storage = FUN_00aa13e0(0x74);
    RenderResource* resource;
    if (storage != 0) resource = static_cast<RenderResource*>(storage)->FUN_00a7c190(2, 1, source, 1, 1);
    else resource = 0;
    if (resource) resource->IncRefCount();

    unsigned char* pixels = *resource->dataBase + resource->dataOffset;
    if (source->format == 16) {
        pixels[3] = 0xff;
        pixels[2] = 0xff;
        pixels[1] = 0;
        pixels[0] = 0;
    } else if (source->format == 32) {
        pixels[3] = 0;
        pixels[2] = 0;
        pixels[7] = 0xff;
        pixels[6] = 0xff;
        pixels[5] = 0xff;
        pixels[4] = 0xff;
        pixels[1] = 0;
        pixels[0] = 0;
    }

    ResourceParameters params;
    params.count = 6;
    params.unk08 = 0;
    params.unk04 = 0;
    const char* name = FUN_00a5b690(DAT_010edbb8);
    RefObject* selected = FUN_00a5ff10(resource, name, &params);
    if (Target() != selected) {
        if (Target()) Target()->DecRefCount();
        Target() = selected;
        if (selected) selected->IncRefCount();
    }
    if (name != DAT_0109b220) {
        InterlockedDecrement(reinterpret_cast<volatile long*>(const_cast<char*>(name) - 8));
    }
    resource->DecRefCount();
    return true;
}
