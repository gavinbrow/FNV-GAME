extern int DAT_010bc560;

struct TextureManager_9160 {
    void FUN_00b6da10(int texture);
};
extern int DAT_011f91a8;

struct TextureResource_9160 {
    virtual void Release(int releaseFlag);
};
struct TextureList_9160 {
    int m_version;
    TextureResource_9160** m_data;
    void FUN_00ba3aa0(unsigned int index, TextureResource_9160*& value);
};
struct TextureWrapper_9160 {
    int FUN_00ba3780();
    int FUN_00ba3770();
    void FUN_00ba38b0();
    void FUN_00ba3a00();
    ~TextureWrapper_9160() { FUN_00ba3a00(); }
};
struct __declspec(novtable) Base_9160 {
    virtual ~Base_9160() { FUN_00ba3d30(); }
    int m_04;
    int m_08;
    int m_0c;
    int m_10;
    int m_14;
    TextureList_9160 m_array;
    int m_20;
    int m_24;
    int m_28;
    int m_2c;
    int m_30;
    int m_34;
    int m_38;
    int m_3c;
    int m_40;
    int m_44;
    int m_48;
    int m_4c;
    int m_50;
    int m_54;
    void FUN_00ba3d30();
};
struct FUN_00bd9160 : Base_9160 {
    TextureWrapper_9160 m_texture;
    ~FUN_00bd9160();
};
FUN_00bd9160::~FUN_00bd9160()
{
    if (m_array.m_data[0]) {
        TextureResource_9160* entry = m_array.m_data[0];
        if (entry)
            entry->Release(1);
        TextureResource_9160* empty = 0;
        m_array.FUN_00ba3aa0(0, empty);
    }
    if (m_texture.FUN_00ba3780()) {
        TextureManager_9160* manager = reinterpret_cast<TextureManager_9160*>(DAT_011f91a8);
        manager->FUN_00b6da10(m_texture.FUN_00ba3770());
        m_texture.FUN_00ba38b0();
    }
}
