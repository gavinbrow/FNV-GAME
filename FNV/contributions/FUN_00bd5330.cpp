
struct FUN_00be0f10 {
    virtual ~FUN_00be0f10();
};
struct FUN_00b79930 {
    unsigned int member;
    ~FUN_00b79930();
};
struct FUN_00b66f20 {
    NiRefObject* m_pObject;
    ~FUN_00b66f20();
};
struct MM_011f6238 {
    void FUN_00aa4060(void* ptr);
};
extern MM_011f6238 DAT_011f6238;
struct FUN_00bd5330 : FUN_00be0f10 {
    unsigned int unknown04;
    unsigned int unknown08;
    unsigned int unknown0c;
    unsigned int unknown10;
    unsigned int unknown14;
    unsigned int unknown18;
    unsigned int unknown1c;
    unsigned int unknown20;
    unsigned int unknown24;
    unsigned int unknown28;
    unsigned int unknown2c;
    unsigned int unknown30;
    unsigned int unknown34;
    unsigned int unknown38;
    unsigned int unknown3c;
    unsigned int unknown40;
    unsigned int unknown44;
    unsigned int unknown48;
    unsigned int unknown4c;
    unsigned int unknown50;
    unsigned int unknown54;
    unsigned int unknown58;
    unsigned int unknown5c;
    unsigned int unknown60;
    unsigned int unknown64;
    unsigned int unknown68;
    FUN_00b79930 table6c[1];
    unsigned int unknown70;
    unsigned int unknown74;
    unsigned int unknown78;
    FUN_00b66f20 maps7c[4];
    FUN_00b66f20 maps8c[2];
    void* instance94;
    unsigned int count98;
    virtual ~FUN_00bd5330();
};
FUN_00bd5330::~FUN_00bd5330() {
    for (unsigned int i = 0; i < 4; ++i) {
        NiRefObject* obj = maps7c[i].m_pObject;
        if (obj) {
            obj->DecRefCount();
            maps7c[i].m_pObject = 0;
        }
    }
    for (unsigned int i = 0; i < 2; ++i) {
        NiRefObject* obj = maps8c[i].m_pObject;
        if (obj) {
            obj->DecRefCount();
            maps8c[i].m_pObject = 0;
        }
    }
    void* allocated = instance94;
    count98 = 0;
    DAT_011f6238.FUN_00aa4060(allocated);
}
