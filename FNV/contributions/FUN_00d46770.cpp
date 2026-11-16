struct FNVBuffer { void* data; unsigned int used; unsigned int capacityAndFlags; };
struct FNVWriter {
    virtual void method00(); virtual void method04(); virtual void method08();
    virtual void method0c(); virtual void method10();
    virtual void method14(int operation, const void* globalData, void* bytes, unsigned int count, unsigned int limit);
    int unk04; int unk08; int unk0c; unsigned char allowRestricted;
};
extern int DAT_010cc460;
extern unsigned int __cdecl FUN_00d06f80(void*, unsigned int);
struct FUN_00d46770_cls { int unk00; int unk04; FNVBuffer* buffer; void FUN_00d46770(FNVWriter* writer, int unused); };
void FUN_00d46770_cls::FUN_00d46770(FNVWriter* writer, int unused) {
    FNVBuffer* b = buffer;
    if (b != 0) {
        unsigned int flags = b->capacityAndFlags;
        if ((flags & 0x80000000u) == 0 || writer->allowRestricted) {
            void* data = b->data;
            unsigned int limit = FUN_00d06f80(data, flags & 0x3fffffff);
            writer->method14(3, &DAT_010cc460, b->data, b->used, limit);
        }
    }
}