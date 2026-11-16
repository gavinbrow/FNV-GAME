extern "C" void* __cdecl memcpy(void*, const void*, unsigned int);
extern char DAT_01080864;
void __cdecl FUN_005b5e40(void*);

struct BinaryRecord36 {
    void* value00;
    void* value04;
    void* value08;
    unsigned int value0c, value10, value14, value18, value1c, value20;
    void FUN_008572c0();
};
struct BinaryRecord44 {
    void* value00;
    unsigned int value04, value08, value0c;
    void* value10;
    unsigned int value14, value18, value1c, value20, value24, value28;
    void FUN_00857320();
};
class TESForm;
class MagicProjectile {
public:
    virtual void V0();
    virtual void V1();
    virtual void V2();
    virtual void V3();
    virtual ~MagicProjectile();
};
struct SourceItem {
    unsigned int FUN_00559450();
    unsigned char* FUN_00726070();
};
struct SourceMap {
    SourceItem* FUN_00855100(unsigned int key);
};
struct SourceTracker {
    void FUN_00905330(unsigned int* key);
};
struct FUN_008598d0_shell {
    SourceMap* source;
    unsigned int field04, field08, field0c, field10, field14;
    unsigned int field18, field1c, field20;
    SourceTracker tracker;
    void* FUN_00861c00(void*);
    TESForm* FUN_00859a90(unsigned int key, BinaryRecord36* data);
    TESForm* FUN_00859f20(unsigned int key, BinaryRecord44* data);
    void FUN_00858730(TESForm*);
    void FUN_008598d0(unsigned int key);
};
void FUN_008598d0_shell::FUN_008598d0(unsigned int key)
{
    SourceItem* item = source->FUN_00855100(key);
    if (item != 0) {
        unsigned int flags = item->FUN_00559450();
        if (flags & 0) {
            unsigned char* bytes = item->FUN_00726070();
            if (bytes != 0) {
                TESForm* pCreated;
                BinaryRecord36 record;
                record.FUN_008572c0();
                bytes += 4;
                memcpy(&record, bytes, sizeof(record));
                record.value04 = FUN_00861c00(record.value04);
                record.value08 = FUN_00861c00(record.value08);
                pCreated = FUN_00859a90(key, &record);
                if (pCreated != 0) {
                    MagicProjectile* asSpecial = dynamic_cast<MagicProjectile*>(pCreated);
                    if (asSpecial != 0) {
                        delete asSpecial;
                        return;
                    }
                    FUN_00858730(pCreated);
                }
            }
        } else if (flags & 0) {
            unsigned char* bytes2 = item->FUN_00726070();
            if (bytes2 != 0) {
                BinaryRecord44 record2;
                record2.FUN_00857320();
                bytes2 += 4;
                memcpy(&record2, bytes2, sizeof(record2));
                record2.value00 = FUN_00861c00(record2.value00);
                record2.value10 = FUN_00861c00(record2.value10);
                TESForm* newObject2 = FUN_00859f20(key, &record2);
                if (newObject2 != 0)
                    FUN_00858730(newObject2);
                tracker.FUN_00905330(&key);
            }
        } else {
            FUN_005b5e40(&DAT_01080864);
        }
    }
}