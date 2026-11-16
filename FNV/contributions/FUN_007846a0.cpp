
struct ItemListBoxCalls {
    virtual void Method0();
    virtual void Method1();
    virtual void Method2();
    virtual void Method3();
    virtual void Method4();
    virtual void Method5();
    virtual void Method6();
    virtual void Method7();
};
struct TileActionCalls {
    void __thiscall FUN_00a07dc0(int);
    void __thiscall FUN_00700320(int,int);
};
extern "C" int DAT_011d9f58;

void __cdecl FUN_007846a0() {
    reinterpret_cast<ItemListBoxCalls*>(&static_cast<ItemModMenu*>(DAT_011d9f54)->lbItemModList)->Method7();
    DAT_011d9f58 = 0;
    DAT_011d9f54->HandleMouseoverTileAlt(0x0f, 0);
    reinterpret_cast<TileActionCalls*>(static_cast<ItemModMenu*>(DAT_011d9f54)->pTiles[8])->FUN_00a07dc0(0xfa9);
    reinterpret_cast<TileActionCalls*>(static_cast<ItemModMenu*>(DAT_011d9f54)->pTiles[8])->FUN_00700320(0xfa3, 0);
}
