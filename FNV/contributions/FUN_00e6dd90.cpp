
struct LockedRect {
    int pitch;
    void* bits;
};
struct Texture {
    virtual void Unused00();
    virtual void Unused01();
    virtual void Unused02();
    virtual void Unused03();
    virtual void Unused04();
    virtual void Unused05();
    virtual void Unused06();
    virtual void Unused07();
    virtual void Unused08();
    virtual void Unused09();
    virtual void Unused10();
    virtual void Unused11();
    virtual void Unused12();
    virtual void Unused13();
    virtual void Unused14();
    virtual void Unused15();
    virtual void Unused16();
    virtual void Unused17();
    virtual void Unused18();
    virtual long __stdcall LockRect(unsigned int level, LockedRect* rectangle, const void* area, unsigned int flags);
};
struct RenderSource {
    virtual void Unused00();
    virtual void Unused01();
    virtual void Unused02();
    virtual void Unused03();
    virtual void Unused04();
    virtual void Unused05();
    virtual void Unused06();
    virtual void Unused07();
    virtual void Unused08();
    virtual void Unused09();
    virtual void Unused10();
    virtual void Unused11();
    virtual void Unused12();
    virtual void Unused13();
    virtual void Unused14();
    virtual void Unused15();
    virtual void Unused16();
    virtual void Unused17();
    virtual void Unused18();
    virtual void Unused19();
    virtual void Unused20();
    virtual void Unused21();
    virtual void Unused22();
    virtual void Unused23();
    virtual void Unused24();
    virtual void Unused25();
    virtual void Unused26();
    virtual void Unused27();
    virtual void Unused28();
    virtual void Unused29();
    virtual void Unused30();
    virtual void Unused31();
    virtual void Unused32();
    virtual void Unused33();
    virtual void Unused34();
    virtual void Unused35();
    virtual void Unused36();
    virtual void Unused37();
    virtual void Unused38();
    virtual Texture* GetDiscardTexture();
    virtual void Unused39();
    virtual void Unused40();
    virtual void Unused41();
    virtual void Unused42();
    virtual void Unused43();
    virtual Texture* GetRegularTexture();
    virtual bool IsLocked();
    virtual void SetLocked(bool locked);
};
struct SourceManager {
    virtual void Unused00();
    virtual void Unused01();
    virtual void Unused02();
    virtual void Unused03();
    virtual void Unused04();
    virtual void Unused05();
    virtual void Unused06();
    virtual void Unused07();
    virtual void Unused08();
    virtual void Unused09();
    virtual void Unused10();
    virtual void Unused11();
    virtual void Unused12();
    virtual void Unused13();
    virtual void Unused14();
    virtual void Unused15();
    virtual void Unused16();
    virtual void Unused17();
    virtual void Unused18();
    virtual void Unused19();
    virtual void Unused20();
    virtual void Unused21();
    virtual void Unused22();
    virtual void Unused23();
    virtual void Unused24();
    virtual void Unused25();
    virtual void Unused26();
    virtual void Unused27();
    virtual void Unused28();
    virtual void Unused29();
    virtual void Unused30();
    virtual void Unused31();
    virtual void Unused32();
    virtual void Unused33();
    virtual void Unused34();
    virtual void Unused35();
    virtual void Unused36();
    virtual void Unused37();
    virtual void Unused38();
    virtual void Unused39();
    virtual void Unused40();
    virtual void Unused41();
    virtual void Unused42();
    virtual RenderSource* GetRenderSource();
};
extern const char DAT_010ed96c[];
char* __cdecl NiXenonErrorString(unsigned int status);
void __cdecl FUN_00a29680(const char* format, const char* message);
struct Renderer {
    void* __thiscall FUN_00e6dd90(SourceManager* manager, int* pitch);
};
void* Renderer::FUN_00e6dd90(SourceManager* manager, int* pitch)
{
    *pitch = 0;
    if (!manager) return 0;
    RenderSource* source = manager->GetRenderSource();
    if (!source) return 0;
    if (source->IsLocked()) return 0;
    unsigned int lockFlags = 0;
    Texture* texture;
    if (reinterpret_cast<const unsigned char*>(this)[0x6f5]) {
        texture = source->GetDiscardTexture();
        lockFlags = 0x2000;
    } else {
        texture = source->GetRegularTexture();
    }
    if (texture) {
        LockedRect rect;
        long result = texture->LockRect(0, &rect, 0, lockFlags);
        if (result < 0) {
            FUN_00a29680(DAT_010ed96c, NiXenonErrorString(result));
        } else {
            void* bits = rect.bits;
            *pitch = rect.pitch;
            source->SetLocked(true);
            return bits;
        }
    }
    return 0;
}
