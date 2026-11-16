#include "h_c60f7efe3297.h"
struct ShaderLibrary {
    virtual void vf0();
    virtual void vf1();
    virtual void vf2();
    virtual void vf3();
    virtual void vf4();
    virtual void vf5();
    virtual void vf6();
    virtual void vf7();
    virtual void vf8();
    virtual void vf9();
    virtual void vf10();
    virtual void vf11();
    virtual void vf12();
    virtual void vf13();
    virtual void vf14();
    virtual void vf15();
    virtual void vf16();
    virtual void vf17();
    virtual bool IsDefault();
    virtual void vf19();
    virtual void vf20();
    virtual void vf21();
    virtual void vf22();
    virtual void vf23();
    virtual void vf24();
    virtual void vf25();
    virtual void vf26();
    virtual void vf27();
    virtual void vf28();
    virtual void vf29();
    virtual void vf30();
    virtual void vf31();
    virtual void vf32();
    virtual void vf33();
    virtual void vf34();
    virtual void vf35();
    virtual void vf36();
    virtual void vf37();
    virtual void vf38();
    virtual void vf39();
    virtual void vf40();
    virtual void vf41();
    virtual void vf42();
    virtual void vf43();
    virtual void vf44();
    virtual void vf45();
    virtual void vf46();
    virtual void vf47();
    virtual void vf48();
    virtual void vf49();
    virtual void vf50();
    virtual void vf51();
    virtual void ReleaseResources();

    void FUN_00e818d0(void* renderer);
};
struct LibraryMap {
    void* vtable;
    unsigned int count;
    ShaderLibrary** entries;
    __forceinline ShaderLibrary* GetFirst(unsigned int n) const {
        unsigned int i = 0;
        if (i < n) {
            ShaderLibrary** data = entries;
            ShaderLibrary** scan = data;
            do {
                if (*scan)
                    return data[i];
                ++i;
                ++scan;
            } while (i < n);
        }
        return 0;
    }
    void FUN_00b57f20(ShaderLibrary** current, void** position, ShaderLibrary** result);
};
struct ShaderRenderer {
    void FUN_00e752b0(ShaderLibrary* library);
};
struct ShaderFactoryShell : NiD3DShaderFactory {
    void FUN_00e92470();
};
void ShaderFactoryShell::FUN_00e92470() {
    if (m_pkRenderer && m_pkShaderMap) {
        LibraryMap* map = static_cast<LibraryMap*>(m_pkShaderMap);
        unsigned int size = map->count;
        ShaderLibrary* volatile shader = 0;
        ShaderLibrary* current = map->GetFirst(size);
        void* position;
        while (current) {
            static_cast<LibraryMap*>(m_pkShaderMap)->FUN_00b57f20(&current, &position, const_cast<ShaderLibrary**>(&shader));
            ShaderLibrary* activeShader = shader;
            if (activeShader) {
                ShaderLibrary& library = *activeShader;
                if (!library.IsDefault()) {
                    library.FUN_00e818d0(m_pkRenderer);
                    library.ReleaseResources();
                    static_cast<ShaderRenderer*>(m_pkRenderer)->FUN_00e752b0(&library);
                }
            }
        }
    }
}
