
struct DecompPass266 {
    void* unk00;
    void* unk04;
    void* m_resource;
    void FUN_00e7de90(unsigned int value);
    void FUN_00e7def0(unsigned int value);
};
struct ShaderPasses {
    DecompPass266* m_primary;
    DecompPass266* m_secondary;
    DecompPass266* m_tertiary;
};
struct GlobalShader {
    unsigned int unk00;
    unsigned int unk04;
    unsigned int unk08;
    unsigned int unk0c;
    unsigned int unk10;
    unsigned int unk14;
    unsigned int unk18;
    unsigned int unk1c;
    unsigned int unk20;
    ShaderPasses* m_passes;
};


extern unsigned int DAT_011f91e4;
struct ObjectHandle { void* m_object; };

struct Renderer {
    virtual void slot00();
    virtual void slot04();
    virtual void slot08();
    virtual void slot0c();
    virtual void slot10();
    virtual void slot14();
    virtual void slot18();
    virtual void slot1c();
    virtual void slot20();
    virtual void slot24();
    virtual void slot28();
    virtual void slot2c();
    virtual void slot30();
    virtual void slot34();
    virtual void slot38();
    virtual void slot3c();
    virtual void slot40();
    virtual void slot44();
    virtual void slot48();
    virtual void slot4c();
    virtual void slot50();
    virtual void slot54();
    virtual void slot58();
    virtual void slot5c();
    virtual void slot60();
    virtual void slot64();
    virtual void slot68();
    virtual void slot6c();
    virtual void slot70();
    virtual void slot74();
    virtual void slot78();
    virtual void slot7c();
    virtual void slot80();
    virtual void slot84();
    virtual void slot88();
    virtual void slot8c();
    virtual void slot90();
    virtual void slot94();
    virtual void slot98();
    virtual void slot9c();
    virtual void slota0();
    virtual void slota4();
    virtual void slota8();
    virtual void slotac();
    virtual void slotb0();
    virtual void slotb4();
    virtual void slotb8();
    virtual void slotbc();
    virtual void slotc0();
    virtual void slotc4();
    virtual void slotc8();
    virtual void slotcc();
    virtual void slotd0();
    virtual void slotd4();
    virtual void slotd8();
    virtual void slotdc();
    virtual unsigned int getProperty();
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
    unsigned int unk50;
    unsigned int unk54;
    unsigned int unk58;
    unsigned int unk5c;
    unsigned int unk60;
    unsigned int unk64;
    unsigned int unk68;
    unsigned int unk6c;
    unsigned int unk70;
    unsigned int unk74;
    unsigned int unk78;
    unsigned int unk7c;
    unsigned int unk80;
    unsigned int unk84;
    unsigned int unk88;
    unsigned int unk8c;
    unsigned int unk90;
    unsigned int unk94;
    unsigned int unk98;
    unsigned int unk9c;
    unsigned int unka0;
    unsigned int unka4;
    unsigned int unka8;
    ObjectHandle* m_primary;
    ObjectHandle* m_secondary;
    unsigned short FUN_00b704b0();
};
struct TextureGenerator {
    void* FUN_004bc320(unsigned int code);
};
struct ShaderResource {
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
    unsigned int unk50;
    unsigned int unk54;
    unsigned int unk58;
    unsigned int unk5c;
    unsigned int unk60;
    unsigned int unk64;
    unsigned int unk68;
    unsigned int unk6c;
    unsigned int unk70;
    unsigned int unk74;
    unsigned int unk78;
    unsigned int unk7c;
    unsigned int unk80;
    unsigned int unk84;
    unsigned int unk88;
    unsigned int unk8c;
    unsigned int unk90;
    unsigned int unk94;
    unsigned int unk98;
    unsigned int unk9c;
    unsigned int unka0;
    unsigned int unka4;
    unsigned int unka8;
    unsigned int unkac;
    unsigned int unkb0;
    unsigned int unkb4;
    unsigned int unkb8;
    unsigned int unkbc;
    unsigned int unkc0;
    unsigned int unkc4;
    unsigned int unkc8;
    unsigned int unkcc;
    unsigned int unkd0;
    unsigned int unkd4;
    unsigned int unkd8;
    unsigned int unkdc;
    unsigned int unke0;
    unsigned int unke4;
    unsigned int unke8;
    unsigned char m_active;
    unsigned char unkED,unkEE,unkEF;
    unsigned int unkf0;
    unsigned int unkf4;
    unsigned int unkf8;
    unsigned int unkfc;
    unsigned int unk100;
    unsigned int unk104;
    unsigned int unk108;
    TextureGenerator* m_generator;
};
struct ResourceHandle { ShaderResource* m_resource; };
struct RenderOptions {
    unsigned int unk00;
    unsigned int unk04;
    unsigned char unk08;
    unsigned char m_active;
    unsigned short unk0a;
    ResourceHandle* m_handle;
};


void __stdcall FUN_00c02e20(unsigned int opcode, Renderer* renderer)
{
    GlobalShader* g = (GlobalShader*)DAT_0126f74c;
    if ((unsigned int)(opcode - 445) <= 36) {
        if (opcode < 452 || opcode > 455) {
            if ((unsigned int)(opcode - 456) > 3)
                return;
        }
    }
    if (opcode >= 728 && opcode <= 751)
        return;

    DecompPass266* first = g->m_passes->m_primary;
    first->m_resource = renderer->m_primary->m_object;
    first->FUN_00e7de90(renderer->getProperty());

    DecompPass266* second = g->m_passes->m_secondary;
    if (second) {
        void* resource = renderer->m_secondary->m_object;
        if (!resource)
            resource = (void*)DAT_011f9510;
        second->m_resource = resource;
        second->FUN_00e7de90(renderer->getProperty());
    }

    if ((unsigned int)(DAT_011f91e4 - 452) <= 3 && renderer->FUN_00b704b0() > 0) {
        RenderOptions* options = (RenderOptions*)DAT_011f91e0;
        ShaderResource* resource = options->m_handle->m_resource;
        if (resource->m_active && resource->m_generator && options->m_active > 0) {
            DecompPass266* third = g->m_passes->m_tertiary;
            third->m_resource = resource->m_generator->FUN_004bc320(0);
            third->FUN_00e7def0(1);
            third->FUN_00e7de90(0);
        }
    }
}
