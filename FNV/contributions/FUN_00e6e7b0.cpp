
struct RendererPool {
    unsigned int* slots;
    unsigned short flags;
    unsigned short count;
    unsigned short active;
    unsigned short extra;
    unsigned int reserved;

    void Reset() {
        for (unsigned short index = 0; index < count; ++index)
            slots[index] = 0;
        count = 0;
        active = 0;
    }
};
struct RendererPoolView : NiXenonRenderer { void FUN_00e6e7b0(); };
void RendererPoolView::FUN_00e6e7b0()
{
    RendererPool* pools =
        reinterpret_cast<RendererPool*>(reinterpret_cast<char*>(this) + 0xaf8);
    pools[0].Reset();
    pools[1].Reset();
}
