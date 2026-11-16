extern "C" __m128 _mm_setr_ps(float, float, float, float);
union hkVec4 { __m128 m_quad; char m_bytes[16]; }; 
struct BytePair { char a; char b; };
struct EntityCinfo {
    int unk00, unk04, unk08, unk0C;
    float m_position[4];
    float m_rotation[4];
    float unk30, unk34, unk38;
    char unk3C, unk3D;
};
struct EntityObj {
    int unk00;
    unsigned short m_memSizeAndFlags;
    short unk06;
    int unk08, unk0C, unk10, unk14, unk18, unk1C, unk20, unk24;
    int unk28, unk2C, unk30, unk34, unk38, unk3C, unk40, unk44;
    int unk48, unk4C;
    float unk50, unk54, unk58;
    char unk5C, unk5D;
    static void* operator new(unsigned int nbytes) {
        EntityObj* p=(EntityObj*)FUN_00c85750()->heap().allocateChunk(nbytes);
        p->m_memSizeAndFlags=(unsigned short)nbytes;
        return p;
    }
    static void operator delete(void* p, unsigned int nbytes);
    EntityObj(int a,int b,int c);
    void FUN_00d4d410(const hkVector4& position,const hkVector4& rotation);
    void removeReference();
};
struct EntityOwner {
    virtual void v00(); virtual void v01(); virtual void v02(); virtual void v03();
    virtual void v04(); virtual void v05(); virtual void v06(); virtual void v07();
    virtual void v08(); virtual void v09(); virtual void v10(); virtual void v11();
    virtual void v12(); virtual void v13(); virtual void v14(); virtual void v15();
    virtual void v16(); virtual void v17(); virtual void v18(); virtual void v19();
    virtual void v20(); virtual void v21(); virtual void v22(); virtual void v23();
    virtual void v24(); virtual void v25(); virtual void v26(); virtual void v27();
    virtual void v28(); virtual void v29(); virtual void v30(); virtual void v31();
    virtual void v32(); virtual void v33(); virtual void v34();
    virtual void AddEntity(EntityObj* obj);
    virtual void v36(); virtual void v37(); virtual void v38(); virtual void v39();
    virtual void v40(); virtual void v41(); virtual void v42(); virtual void v43();
    virtual void v44(); virtual void v45(); virtual void v46();
    virtual int AddCinfo(EntityCinfo* info);
    int FUN_00cc3050(EntityCinfo* info);
};
int EntityOwner::FUN_00cc3050(EntityCinfo* info) {
    MemContextGuard guard(0x10);
    EntityObj* entity = new EntityObj(info->unk04,info->unk08,0);
    entity->unk54=info->unk34;
    entity->unk58=info->unk38;
    entity->unk50=info->unk30;
    BytePair flags;
    flags.a=info->unk3C;
    entity->unk5C=flags.a;
    flags.b=*(volatile char*)&info->unk3D;
    entity->unk5D=flags.b;
    hkVec4 rotation;
    rotation.m_quad=_mm_setr_ps(info->m_rotation[0],info->m_rotation[1],info->m_rotation[2],info->m_rotation[3]);
    hkVec4 position;
    position.m_quad=_mm_setr_ps(info->m_position[0],info->m_position[1],info->m_position[2],info->m_position[3]);
    entity->FUN_00d4d410(*(hkVector4*)&position,*(hkVector4*)&rotation);
    AddEntity(entity);
    entity->removeReference();
    return AddCinfo(info);
}