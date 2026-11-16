struct hkObjectE02;
struct hkLoaderE02 {
    int Get(char const* name, hkObjectE02** out);
};
struct Router {
    int a;
    int b;
    int c;
    int d;
    int e;
    int f;
    int g;
    int h;
    int i;
    int j;
};
Router* __cdecl _FNV_e03300_arena();
struct Sink {
    void FUN_00cb1870(void*, int, int);
};
struct FUN_00d08940_shell {
    unsigned int unk00;
    unsigned int unk04;
    unsigned int unk08;
    unsigned int unk0c;
    unsigned int unk10;
    unsigned int unk14;
    unsigned int unk18;
    unsigned int unk1c;
    unsigned int unk20;
    unsigned int unk24;
    unsigned int unk28;
    unsigned int unk2c;
    unsigned int unk30;
    unsigned int unk34;
    unsigned int unk38;
    unsigned int unk3c;
    unsigned int unk40;
    unsigned int unk44;
    unsigned int unk48;
    unsigned int unk4c;
    hkLoaderE02 loader;
    void FUN_00d08940(char const* name);
};
void FUN_00d08940_shell::FUN_00d08940(char const* name)
{
    hkObjectE02* obj;
    if (loader.Get(name, &obj)) {
        Router* router = _FNV_e03300_arena();
        reinterpret_cast<Sink*>(reinterpret_cast<char*>(this) + 0x50)->FUN_00cb1870(
            reinterpret_cast<void*>(router->e), reinterpret_cast<int>(name), 1);
    }
}
