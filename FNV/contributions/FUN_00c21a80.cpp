extern "C" int DAT_01202690;
struct FUN_00c21a80_obj;
struct FUN_00c21a80_entry {
    unsigned int unk00;
    FUN_00c21a80_entry* m_pNext;
};
struct FUN_00c21a80_node {
    FUN_00c21a80_node* m_pNext;
    unsigned int unk04;
    FUN_00c21a80_obj* m_pItem;
};
struct FUN_00c21a80_obj {
    virtual void v00();
    virtual void v01();
    virtual void* v02();
    virtual void v03();
    virtual void v04();
    virtual void v05();
    virtual void v06();
    virtual void v07();
    virtual void v08();
    virtual void v09();
    virtual void v10();
    virtual void v11();
    virtual void v12();
    virtual void v13();
    virtual void v14();
    virtual void v15();
    virtual void v16();
    virtual void v17();
    virtual void v18();
    virtual void v19();
    virtual void v20();
    virtual void v21();
    virtual void v22();
    virtual void v23();
    virtual void v24();
    virtual void v25();
    virtual void v26();
    virtual void v27();
    virtual void v28();
    virtual void v29();
    virtual void v30();
    virtual void v31();
    virtual void v32();
    virtual void v33();
    virtual void v34();
    virtual void v35();
    virtual void v36(NiUpdateData&);
    virtual void v37(NiUpdateData&);
    virtual void v38();
    virtual void v39();
    virtual void v40();
    virtual void v41();
    virtual void v42();
    virtual void v43();
    virtual void v44();
    virtual void v45();
    virtual void v46(NiUpdateData&);
    virtual void v47();
    unsigned int unk04;
    unsigned int unk08;
    unsigned int m_0c;
    unsigned int unk10;
    unsigned int unk14;
    unsigned int unk18;
    unsigned int unk1C;
    unsigned int unk20;
    unsigned int unk24;
    unsigned int unk28;
    unsigned int unk2C;
    FUN_00c21a80_obj* m_pNext30;
};
struct FUN_00c21a80_cls {
    virtual void v00();
    virtual void v01();
    virtual void* v02();
    virtual void v03();
    virtual void v04();
    virtual void v05();
    virtual void v06();
    virtual void v07();
    virtual void v08();
    virtual void v09();
    virtual void v10();
    virtual void v11();
    virtual void v12();
    virtual void v13();
    virtual void v14();
    virtual void v15();
    virtual void v16();
    virtual void v17();
    virtual void v18();
    virtual void v19();
    virtual void v20();
    virtual void v21();
    virtual void v22();
    virtual void v23();
    virtual void v24();
    virtual void v25();
    virtual void v26();
    virtual void v27();
    virtual void v28();
    virtual void v29();
    virtual void v30();
    virtual void v31();
    virtual void v32();
    virtual void v33();
    virtual void v34();
    virtual void v35();
    virtual void v36(NiUpdateData&);
    virtual void v37(NiUpdateData&);
    virtual void v38();
    virtual void v39();
    virtual void v40();
    virtual void v41();
    virtual void v42();
    virtual void v43();
    virtual void v44();
    virtual void v45();
    virtual void v46(NiUpdateData&);
    virtual void v47();
    unsigned int unk04;
    unsigned int unk08;
    FUN_00c21a80_obj* m_pList0C;
    unsigned int unk10;
    unsigned int unk14;
    unsigned int unk18;
    unsigned int unk1C;
    unsigned int unk20;
    FUN_00c21a80_node* m_pList24;
    unsigned int unk28;
    unsigned int unk2C;
    unsigned int unk30;
    unsigned int unk34;
    unsigned int unk38;
    unsigned int unk3C;
    unsigned int unk40;
    unsigned int unk44;
    unsigned int unk48;
    unsigned int unk4C;
    unsigned int unk50;
    unsigned int unk54;
    unsigned int unk58;
    unsigned int unk5C;
    unsigned int unk60;
    unsigned int unk64;
    unsigned int unk68;
    unsigned int unk6C;
    unsigned int unk70;
    unsigned int unk74;
    unsigned int unk78;
    unsigned int unk7C;
    unsigned int unk80;
    unsigned int unk84;
    unsigned int unk88;
    unsigned int unk8C;
    unsigned int unk90;
    unsigned int unk94;
    unsigned int unk98;
    unsigned int unk9C;
    unsigned int unkA0;
    unsigned int unkA4;
    unsigned int unkA8;
    unsigned int unkAC;
    unsigned int unkB0;
    unsigned int unkB4;
    unsigned int unkB8;
    unsigned int unkBC;
    unsigned int unkC0;
    unsigned int unkC4;
    unsigned int unkC8;
    unsigned int unkCC;
    unsigned int unkD0;
    unsigned int unkD4;
    unsigned int unkD8;
    unsigned int unkDC;
    unsigned int unkE0;
    unsigned int unkE4;
    unsigned int unkE8;
    unsigned int unkEC;
    unsigned int unkF0;
    unsigned int unkF4;
    unsigned int unkF8;
    unsigned int unkFC;
    unsigned int unk100;
    unsigned int unk104;
    unsigned int unk108;
    unsigned int unk10C;
    float m_f110;
    char m_b114;
    void __thiscall FUN_00c21a80(NiUpdateData&, unsigned int);
};
void FUN_00c21a80_cls::FUN_00c21a80(NiUpdateData& upd, unsigned int arg2) {
    if (upd.bParallelUpdate) {
        upd.bFoundParticles = true;
        return;
    }
    FUN_00c21a80_obj* found = 0;
    if (upd._pad04 != 0) {
        FUN_00c21a80_node* node = m_pList24;
        while (node) {
            FUN_00c21a80_obj*& ref = node->m_pItem;
            node = node->m_pNext;
            if (ref && ref->m_0c != 0) {
                ref->v36(upd);
            }
        }
        FUN_00c21a80_obj* obj = (FUN_00c21a80_obj*)m_pList0C;
        while (obj) {
            FUN_00c21a80_entry* e = (FUN_00c21a80_entry*)obj->v02();
            if (e) {
                do {
                    if ((void*)e == (void*)&DAT_01202690) {
                        found = obj;
                        goto next;
                    }
                    e = e->m_pNext;
                } while (e);
            }
            obj->v37(upd);
        next:
            obj = obj->m_pNext30;
        }
        v46(upd);
        if (found) found->v37(upd);
    } else {
        v46(upd);
    }
    v47();
    m_f110 = upd.fTime;
    m_b114 = upd._pad04;
}
