struct RenderState {
    void FUN_00e6fe30(void* geometry, void* context, int flags, int mode, int reserved);
    void FUN_00e6fda0(void* geometry, void* info, void* context);
    void FUN_00e6fbb0(void* context, int enabled);
};
struct IndexController {
    virtual void vfn_00(); virtual void vfn_04(); virtual void vfn_08();
    virtual void vfn_0c(); virtual void vfn_10(); virtual void vfn_14();
    virtual void vfn_18(); virtual void vfn_1c(); virtual void vfn_20();
    virtual void vfn_24(); virtual void vfn_28();
    virtual void vfn_2c(unsigned int index);
};
struct FUN_00e807d0_shell {
    int FUN_00e807d0(void* unusedFirst, void* geometry, void* info, void* unusedFourth, void* unusedFifth, void* unusedSixth, void* context, void* unusedEighth);
};
int FUN_00e807d0_shell::FUN_00e807d0(void* unusedFirst, void* geometry, void* info, void* unusedFourth, void* unusedFifth, void* unusedSixth, void* context, void* unusedEighth) {
    if (info != 0) {
        if (*reinterpret_cast<unsigned int*>(reinterpret_cast<char*>(this)+0x38) == 0) {
            reinterpret_cast<RenderState*>(*reinterpret_cast<void**>(reinterpret_cast<char*>(this)+0x18))->FUN_00e6fe30(geometry, context, 0, 4, 0);
        }
        reinterpret_cast<IndexController*>(*reinterpret_cast<void**>(reinterpret_cast<char*>(this)+0x1c))->vfn_2c(*reinterpret_cast<unsigned short*>(reinterpret_cast<char*>(info)+0x24));
        reinterpret_cast<RenderState*>(*reinterpret_cast<void**>(reinterpret_cast<char*>(this)+0x18))->FUN_00e6fda0(geometry, info, context);
    } else if (*reinterpret_cast<unsigned int*>(reinterpret_cast<char*>(this)+0x38) == 0 || *reinterpret_cast<unsigned char*>(reinterpret_cast<char*>(*reinterpret_cast<void**>(reinterpret_cast<char*>(this)+0x18))+0x209) != 0) {
        reinterpret_cast<IndexController*>(*reinterpret_cast<void**>(reinterpret_cast<char*>(this)+0x1c))->vfn_2c(0);
        reinterpret_cast<RenderState*>(*reinterpret_cast<void**>(reinterpret_cast<char*>(this)+0x18))->FUN_00e6fbb0(context, 1);
    }
    return 0;
}