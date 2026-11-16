struct TextureResource { unsigned int m_header00; unsigned int m_header04; unsigned int m_header08; unsigned int m_header0c; unsigned int m_state; };
struct SourcePixels {
    unsigned int m_unknown00;
    unsigned int m_unknown04;
    unsigned int m_unknown08;
    unsigned int m_unknown0c;
    unsigned int m_unknown10;
    unsigned int m_unknown14;
    unsigned int m_unknown18;
    unsigned int m_unknown1c;
    unsigned int m_unknown20;
    unsigned int m_unknown24;
    unsigned int m_unknown28;
    unsigned int m_unknown2c;
    unsigned int m_unknown30;
    unsigned int m_unknown34;
    unsigned int m_unknown38;
    unsigned int m_unknown3c;
    unsigned int m_unknown40;
    unsigned int m_unknown44;
    unsigned int m_unknown48;
    TextureResource* m_resource;
    unsigned int m_unknown50;
    unsigned int m_unknown54;
    unsigned int m_unknown58;
    unsigned int m_unknown5c;
    unsigned int m_unknown60;
    unsigned int m_unknown64;
    unsigned int m_revision;
};
struct TextureOwner {
    unsigned int m_unknown00;
    unsigned int m_unknown04;
    unsigned int m_unknown08;
    unsigned int m_unknown0c;
    unsigned int m_unknown10;
    unsigned int m_unknown14;
    unsigned int m_unknown18;
    unsigned int m_unknown1c;
    unsigned int m_unknown20;
    unsigned int m_unknown24;
    unsigned int m_unknown28;
    unsigned int m_unknown2c;
    unsigned int m_unknown30;
    unsigned int m_unknown34;
    unsigned int m_unknown38;
    SourcePixels* m_pixels;
};
struct CreatedTexture {
    virtual void v0();
    virtual void DeleteThis();
    volatile long m_uiRefCount;
};
struct TextureBuilder {
    virtual void v0();
    virtual void v1();
    virtual void v2();
    virtual void v3();
    virtual void v4();
    virtual CreatedTexture* Create(SourcePixels*, NiPixelFormat&, SourcePixels*, bool);
};
extern TextureBuilder* __cdecl FUN_00a76640();
struct TrackedResource {
    TextureResource* current;
    void FUN_00a5f860(TextureResource* resource);
};
struct TextureUpdate_00e689d0 : public NiDX9SourceCubeMapData_S {
    TrackedResource m_resource;
    unsigned int m_meta78;
    unsigned int m_revision7c;
    unsigned int m_state80;
    void FUN_00e68870(CreatedTexture* result);
    void FUN_00e689d0();
};
void TextureUpdate_00e689d0::FUN_00e689d0() {
    if (m_b6c) return;
    TextureOwner* owner = reinterpret_cast<TextureOwner*>(unk08);
    SourcePixels* pixels = owner->m_pixels;
    if (!pixels) return;
    TextureResource* resource = pixels->m_resource;
    bool changed = false;
    if (resource) {
        if (m_state80 != resource->m_state) changed = true;
        bool resourceChanged = m_resource.current != resource;
        m_state80 = resource->m_state;
        if (resourceChanged) {
            m_resource.FUN_00a5f860(resource);
            changed = true;
        }
    }
    if (pixels->m_revision == m_revision7c && !changed) return;
    CreatedTexture* result = FUN_00a76640()->Create(pixels, m_kPixelFormat, pixels, m_bMipmap);
    m_revision7c = pixels->m_revision;
    if (unk08) FUN_00e68870(result);
    if (result) {
        InterlockedIncrement(&result->m_uiRefCount);
        if (InterlockedDecrement(&result->m_uiRefCount) == 0) result->DeleteThis();
    }
}