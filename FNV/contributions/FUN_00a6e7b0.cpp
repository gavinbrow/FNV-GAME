extern char* DAT_0109b220;
extern "C" void (__stdcall* DAT_00fdf1c4)(void*);

struct PaletteMap {
    void* unk00; int unk04; void* unk08; unsigned int m_count;
    void* FUN_00ee8ac0();
    void FUN_00a8f770(void** iterator, char** key, void** object);
};
class FUN_00a6e7b0_class {
public:
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
virtual void vf18();
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
    virtual int vf35(char** key);
    int unk04;
    PaletteMap m_map;
    bool FUN_00a88a50(FUN_00a6e7b0_class* other);
    bool FUN_00a6e7b0(FUN_00a6e7b0_class* other);
};
bool FUN_00a6e7b0_class::FUN_00a6e7b0(FUN_00a6e7b0_class* other)
{
    if (!FUN_00a88a50(other)) return false;
    unsigned int num = m_map.m_count;
    if (other->m_map.m_count != num) return false;
    if (num) {
        void* iterator = m_map.FUN_00ee8ac0();
        if (iterator) {
            void (__stdcall *deallocate)(void*) = DAT_00fdf1c4;
            do {
                char* key = DAT_0109b220;
                void* object;
                m_map.FUN_00a8f770(&iterator, &key, &object);
                if (!other->vf35(&key)) {
                    if (key != DAT_0109b220)
                        deallocate(key - 8);
                    return false;
                }
                if (key != DAT_0109b220)
                    deallocate(key - 8);
            } while (iterator != 0);
        }
    }
    return true;
}