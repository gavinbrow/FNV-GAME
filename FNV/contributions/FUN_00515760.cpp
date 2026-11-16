extern "C" void* __cdecl _alloca(unsigned int);

struct RecordReader {
    unsigned char FUN_00472660();
    int FUN_004726b0();
    bool FUN_004726f0();
    unsigned int FUN_00401660();
    void FUN_004727f0(unsigned int*);
    void FUN_00472840(unsigned short*);
    void FUN_00472890(void*,unsigned int);
    unsigned short FUN_00403570();
    bool FUN_00401680();
};
struct BipedFlags { void FUN_00512810(); void FUN_00503210(); };
struct ScriptView { void FUN_006ecd40(unsigned int); void FUN_0048cd90(void*); };
struct EnchantmentView { void FUN_006ecd40(unsigned int); void FUN_00483170(unsigned short); };
struct EquipView { void FUN_006ecd40(unsigned int); };
struct ModelSegment {
    virtual void Reserved0();
    virtual void Reserved1();
    virtual void Reserved2();
    virtual void Reserved3();
    virtual void Reserved4();
    virtual void Reserved5();
    virtual void ReadModel(char*);
    unsigned int textureSet;
    unsigned int modelPath;
    unsigned int modelFileSize;
    unsigned int textureHash;
    unsigned int meshFlags;
    unsigned int reservedData;
    unsigned int modelVersion;
};
struct SmallModelSegment {
    virtual void Reserved0();
    virtual void Reserved1();
    virtual void Reserved2();
    virtual void Reserved3();
    virtual void Reserved4();
    virtual void Reserved5();
    virtual void ReadModel(char*);
    unsigned int textureSet;
    unsigned int modelPath;
    unsigned int modelFlags;
    unsigned int meshFlags;
    unsigned int modelVersion;
};
struct IconSegment { int description; int flags; int lastUpdate; void FUN_00489100(char*); };
struct TextureSegment { int description; int flags; int lastUpdate; int size; void FUN_0047a380(char*); };
struct BipedView {
    void* vtable;
    unsigned int bipedMask;
    unsigned char bipedType;
    unsigned char humanoidFlags;
    unsigned short wornSlots;
    ModelSegment male;
    ModelSegment female;
    ModelSegment male4;
    ModelSegment female4;
    IconSegment firstIcon;
    IconSegment secondIcon;
    TextureSegment firstTexture;
    TextureSegment secondTexture;
    SmallModelSegment fifth;
};
struct ClothingVirtual {
    virtual void Unknown00();
    virtual void Unknown01();
    virtual void Unknown02();
    virtual void Unknown03();
    virtual void Unknown04();
    virtual void Unknown05();
    virtual void Unknown06();
    virtual void Unknown07();
    virtual void Unknown08();
    virtual void Unknown09();
    virtual void Unknown10();
    virtual void Unknown11();
    virtual void Unknown12();
    virtual void Unknown13();
    virtual void Unknown14();
    virtual void Unknown15();
    virtual void Unknown16();
    virtual void Unknown17();
    virtual void Unknown18();
    virtual void Unknown19();
    virtual void Unknown20();
    virtual void Unknown21();
    virtual void Unknown22();
    virtual void Unknown23();
    virtual void Unknown24();
    virtual void Unknown25();
    virtual void Unknown26();
    virtual void Unknown27();
    virtual void Unknown28();
    virtual void Unknown29();
    virtual void Unknown30();
    virtual void Unknown31();
    virtual void Unknown32();
    virtual void Unknown33();
    virtual void Unknown34();
    virtual void Unknown35();
    virtual void Unknown36();
    virtual void Unknown37();
    virtual void Unknown38();
    virtual void Unknown39();
    virtual void Unknown40();
    virtual void Unknown41();
    virtual void Unknown42();
    virtual void Unknown43();
    virtual void Unknown44();
    virtual void Unknown45();
    virtual void Unknown46();
    virtual void Unknown47();
    virtual void Unknown48();
    virtual void Unknown49();
    virtual void Unknown50();
    virtual void Unknown51();
    virtual void Unknown52();
    virtual void Unknown53();
    virtual void Unknown54();
    virtual void Unknown55();
    virtual void ReadBounds(RecordReader*);
    virtual void Unknown57();
    virtual void Unknown58();
    virtual void Unknown59();
    virtual void Unknown60();
    virtual void Unknown61();
    virtual void Unknown62();
    virtual void Unknown63();
    virtual void Unknown64();
    virtual void Unknown65();
    virtual void Unknown66();
    virtual void Unknown67();
    virtual void Unknown68();
    virtual void Unknown69();
    virtual void Unknown70();
    virtual void Unknown71();
    virtual void Unknown72();
    virtual void Unknown73();
    virtual void Unknown74();
    virtual void Unknown75();
    virtual void Unknown76();
    virtual void ReadEditorID(char*);
};
void __cdecl FUN_00487050(TESFullName*, RecordReader*);
void __cdecl FUN_004781e0(BGSDestructibleObjectForm*, RecordReader*);
void __cdecl FUN_004892d0(ModelSegment*, RecordReader*);
void __cdecl FUN_004893e0(ModelSegment*, RecordReader*);
void __cdecl FUN_0048a990(ModelSegment*, RecordReader*);
struct ClothingLoader {
    B1_4fe base;
    TESFullName fullName;
    TESScriptableForm scriptForm;
    TESEnchantableForm enchantment;
    TESValueForm value;
    TESWeightForm weight;
    BipedView biped;
    BGSDestructibleObjectForm destructible;
    BGSEquipType equip;

    void FUN_00485110(RecordReader*);
    void FUN_00484ab0(int);
    void FUN_004861f0(RecordReader*, int, int);
    bool FUN_00515760(RecordReader*);
};
bool ClothingLoader::FUN_00515760(RecordReader* reader) {
    unsigned char marker = reader->FUN_00472660();
    if (marker != 0x1a)
        return false;
    FUN_00485110(reader);
    FUN_00484ab0(0);
    int chunk;
    while ((chunk = reader->FUN_004726b0()) != 0) {
        switch (chunk) {
        case 0x44494445: {
            char* data = (char*)_alloca(reader->FUN_00401660());
            reader->FUN_00472890(data, 0x200);
            reinterpret_cast<ClothingVirtual*>(this)->ReadEditorID(data);
            break;
        }
        case 0x444e424f: {
            reinterpret_cast<ClothingVirtual*>(this)->ReadBounds(reader);
            break;
        }
        case 0x4c4c5546: {
            FUN_00487050(this ? &this->fullName : 0, reader);
            break;
        }
        case 0x49524353: {
            unsigned int formID = 0;
            reader->FUN_004727f0(&formID);
            reinterpret_cast<ScriptView*>(&this->scriptForm)->FUN_006ecd40(formID);
            reinterpret_cast<ScriptView*>(&this->scriptForm)->FUN_0048cd90(this);
            break;
        }
        case 0x4d544945:
        case 0x4d414e45: {
            unsigned int formID = 0;
            reader->FUN_004727f0(&formID);
            reinterpret_cast<EnchantmentView*>(&this->enchantment)->FUN_006ecd40(formID);
            break;
        }
        case 0x4d414e41:
        case 0x544d4145: {
            unsigned short amount = 0;
            reader->FUN_00472840(&amount);
            reinterpret_cast<EnchantmentView*>(&this->enchantment)->FUN_00483170(amount);
            break;
        }
        case 0x54444d42: {
            if (reader->FUN_00403570() < 11) {
                unsigned int bipedData;
                reader->FUN_00472890(&bipedData, 4);
                if (reader->FUN_00401680())
                    reinterpret_cast<BipedFlags*>(&bipedData)->FUN_00512810();
                (&this->biped)->bipedType = ((unsigned char*)&bipedData)[2];
                (&this->biped)->bipedMask = *(unsigned short*)&bipedData;
            } else {
                reader->FUN_00472890(&(&this->biped)->bipedMask, 8);
                if (reader->FUN_00401680())
                    reinterpret_cast<BipedFlags*>(&(&this->biped)->bipedMask)->FUN_00503210();
            }
            (&this->biped)->bipedType &= ~0x10;
            break;
        }
        case 0x54434d42: {
            char* buffer = (char*)_alloca(reader->FUN_00401660());
            reader->FUN_00472890(buffer, 0);
            (&this->biped)->fifth.ReadModel(buffer);
            break;
        }
        case 0x4c444f4d: {
            char* buffer = (char*)_alloca(reader->FUN_00401660());
            reader->FUN_00472890(buffer, 0);
            (&this->biped)->male.ReadModel(buffer);
            break;
        }
        case 0x54444f4d: {
            FUN_004893e0(&(&this->biped)->male, reader);
            break;
        }
        case 0x53444f4d: {
            FUN_0048a990(&(&this->biped)->male, reader);
            break;
        }
        case 0x44444f4d: {
            FUN_004892d0(&(&this->biped)->male, reader);
            break;
        }
        case 0x44534f4d: {
            FUN_004892d0(&(&this->biped)->female, reader);
            break;
        }
        case 0x32444f4d: {
            char* buffer = (char*)_alloca(reader->FUN_00401660());
            reader->FUN_00472890(buffer, 0);
            (&this->biped)->male4.ReadModel(buffer);
            break;
        }
        case 0x54324f4d: {
            FUN_004893e0(&(&this->biped)->male4, reader);
            break;
        }
        case 0x53324f4d: {
            FUN_0048a990(&(&this->biped)->male4, reader);
            break;
        }
        case 0x4e4f4349: {
            char* buffer = (char*)_alloca(reader->FUN_00401660());
            reader->FUN_00472890(buffer, 0);
            (&this->biped)->firstIcon.FUN_00489100(buffer);
            break;
        }
        case 0x4f43494d: {
            char* buffer = (char*)_alloca(reader->FUN_00401660());
            reader->FUN_00472890(buffer, 0);
            (&this->biped)->firstTexture.FUN_0047a380(buffer);
            break;
        }
        case 0x3243494d: {
            char* buffer = (char*)_alloca(reader->FUN_00401660());
            reader->FUN_00472890(buffer, 0);
            (&this->biped)->secondTexture.FUN_0047a380(buffer);
            break;
        }
        case 0x33444f4d: {
            char* buffer = (char*)_alloca(reader->FUN_00401660());
            reader->FUN_00472890(buffer, 0);
            (&this->biped)->female.ReadModel(buffer);
            break;
        }
        case 0x54334f4d: {
            FUN_004893e0(&(&this->biped)->female, reader);
            break;
        }
        case 0x53334f4d: {
            FUN_0048a990(&(&this->biped)->female, reader);
            break;
        }
        case 0x34444f4d: {
            char* buffer = (char*)_alloca(reader->FUN_00401660());
            reader->FUN_00472890(buffer, 0);
            (&this->biped)->female4.ReadModel(buffer);
            break;
        }
        case 0x54344f4d: {
            FUN_004893e0(&(&this->biped)->female4, reader);
            break;
        }
        case 0x53344f4d: {
            FUN_0048a990(&(&this->biped)->female4, reader);
            break;
        }
        case 0x324f4349: {
            char* buffer = (char*)_alloca(reader->FUN_00401660());
            reader->FUN_00472890(buffer, 0);
            (&this->biped)->secondIcon.FUN_00489100(buffer);
            break;
        }
        case 0x44545344:
        case 0x54534544: {
            FUN_004781e0(this ? &this->destructible : 0, reader);
            break;
        }
        case 0x50595445: {
            unsigned int equipID = 0;
            reader->FUN_004727f0(&equipID);
            reinterpret_cast<EquipView*>(&this->equip)->FUN_006ecd40(equipID);
            break;
        }
        case 0x41544144: {
            FUN_004861f0(reader, 0, 0);
            break;
        }
        default:
            break;
        }
        if (!reader->FUN_004726f0())
            break;
    }
    return true;
}
