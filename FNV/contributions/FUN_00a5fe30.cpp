extern void* __cdecl FUN_00aa13e0(unsigned int size);
extern char* __cdecl FUN_00a5b690(const char* text);
extern void __cdecl FUN_00a57500(void* fixed);
extern void __cdecl FUN_00a76960(void* fixed, void* out);
extern int DAT_0109b220;
extern unsigned char DAT_011a9594;
extern void (__stdcall* DAT_00fdf1c0)(void*);
extern void (__stdcall* DAT_00fdf1c4)(void*);

struct FnvSourceTexture {
    virtual void Delete(unsigned char);
    virtual void slot004();
    virtual void slot008();
    virtual void slot012();
    virtual void slot016();
    virtual void slot020();
    virtual void slot024();
    virtual void slot028();
    virtual void slot032();
    virtual void slot036();
    virtual void slot040();
    virtual void slot044();
    virtual void slot048();
    virtual void slot052();
    virtual void slot056();
    virtual void slot060();
    virtual void slot064();
    virtual void slot068();
    virtual void slot072();
    virtual void slot076();
    virtual void slot080();
    virtual void slot084();
    virtual void slot088();
    virtual void slot092();
    virtual void slot096();
    virtual void slot100();
    virtual void slot104();
    virtual void slot108();
    virtual void slot112();
    virtual void slot116();
    virtual void slot120();
    virtual void slot124();
    virtual void slot128();
    virtual void slot132();
    virtual void slot136();
    virtual void slot140();
    virtual void slot144();
    virtual void slot148();
    virtual void slot152();
    virtual void slot156();
    virtual void slot160();
    virtual void slot164();
    virtual void slot168();
    virtual bool IsLoaded();

    void* unk04;
    void* unk08;
    void* unk0c;
    void* unk10;
    void* unk14;
    int width;
    int height;
    int depth;
    int unk24;
    int unk28;
    int unk2c;
    char* filename;
    char* normalizedName;
    int unk38;
    int unk3c;
    unsigned char unk40;
    unsigned char flags;
    unsigned short unk42;
    int source;

    FnvSourceTexture* __thiscall FUN_00a5fc10();
};

FnvSourceTexture* __cdecl FUN_00a5fe30(int source, const char* name, const int* size, unsigned char flags)
{
    FnvSourceTexture* object = (FnvSourceTexture*)FUN_00aa13e0(0x48);
    if (object)
        object = object->FUN_00a5fc10();
    else
        object = 0;

    object->width = size[0];
    object->height = size[1];
    object->depth = size[2];
    object->flags = flags;
    object->source = source;

    if (name) {
        char* value = FUN_00a5b690(name);
        void (__stdcall* release)(void*) = DAT_00fdf1c4;
        char** fixed = &object->filename;
        if (*fixed != value) {
            if (value != (char*)DAT_0109b220)
                DAT_00fdf1c0(value - 8);
            if (*fixed != (char*)DAT_0109b220)
                release(*fixed - 8);
            *fixed = value;
        }
        FUN_00a57500(fixed);
        FUN_00a76960(fixed, &object->normalizedName);
        if (value != (char*)DAT_0109b220)
            release(value - 8);
    }
    if (DAT_011a9594 && !object->IsLoaded()) {
        object->Delete(1);
        return 0;
    }
    return object;
}