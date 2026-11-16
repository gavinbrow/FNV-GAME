extern "C" void* __cdecl FUN_00aa13e0(unsigned int size);
__forceinline void* __cdecl operator new(unsigned int size) { return FUN_00aa13e0(size); }
struct ImageDescriptor { unsigned int format; unsigned int flags; unsigned short layerCount; };
struct ImageSource {
    ImageDescriptor* descriptor() const {
        return *reinterpret_cast<ImageDescriptor* const*>(reinterpret_cast<const char*>(this) + 0xb8);
    }
};
struct ImageBuffer {
    void* pixels;
    void* pixelFormat;
    unsigned int width, height, stride, sliceSize, layers, options, resourceId;
    void* owner;
    unsigned int referenceCount;
    ImageBuffer(unsigned int layerCount, bool allocateStorage);
    void __thiscall FUN_00a72ca0(bool enabled);
    void __thiscall FUN_00a72bb0(bool owned, void* input);
    void __thiscall FUN_00a726a0(unsigned int a, unsigned int b, unsigned int c,
                                 unsigned int d, unsigned int layers, unsigned int width, unsigned int height);
};
struct DataSize { unsigned int length; };
struct ImageProvider {
    typedef unsigned short (__thiscall *CountGetter)(ImageProvider*);
    typedef void* (__thiscall *DataGetter)(ImageProvider*, DataSize, unsigned int);
    unsigned short getMaxLayers() {
        return reinterpret_cast<CountGetter>((*reinterpret_cast<void***>(this))[0x124 / 4])(this);
    }
    void* getLayerData(unsigned int length, unsigned int first) {
        void** functions = *reinterpret_cast<void***>(this);
        DataSize size = {length};
        return reinterpret_cast<DataGetter>(functions[0x120 / 4])(this, size, first);
    }
    ImageBuffer* __thiscall FUN_00bb3280(ImageSource* source);
};
ImageBuffer* __thiscall ImageProvider::FUN_00bb3280(ImageSource* source) {
    if (source != 0) {
        const unsigned short requested = source->descriptor()->layerCount;
        if (requested <= getMaxLayers()) {
            const unsigned int actual = source->descriptor()->layerCount;
            ImageBuffer* buffer = new ImageBuffer(actual, true);
            buffer->FUN_00a72ca0(true);
            buffer->FUN_00a72bb0(false, getLayerData(static_cast<unsigned short>(actual) << 4, 0));
            buffer->FUN_00a726a0(0, 0, 0, 4, actual, 16, 16);
            return buffer;
        }
    }
    return 0;
}