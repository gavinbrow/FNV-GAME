struct ViewerBase_c851c0 {
    void FUN_00c878c0(BCA05B0StringArray* strings);
};
struct CollisionShape_c851c0 {
    unsigned int unk00;
    unsigned int unk04;
    unsigned int unk08;
    unsigned int unk0c;
    unsigned int collisionFlags;
    __forceinline unsigned int GetLayer() const {
        return collisionFlags & 0x1f;
    }
};
extern const char DAT_010c59cc[];
char* __cdecl FUN_00a7d4d0(const char* format, unsigned int filter);
void FUN_00ca05b0_cls::FUN_00c851c0(BCA05B0StringArray* strings) {
    TlsGuard_ca0090 memoryContext;
    ((ViewerBase_c851c0*)this)->FUN_00c878c0(strings);
    char* line = FUN_00a7d330(g_pcCA05B0Name);
    strings->Add(line);
    line = FUN_00a7d4d0(DAT_010c59cc, ((CollisionShape_c851c0*)this)->GetLayer());
    strings->Add(line);
}