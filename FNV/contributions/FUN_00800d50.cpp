class NiNode;
template <> class NiPointer<NiNode> {
public:
    NiNode* m_pObject;
    NiPointer<NiNode>& operator=(NiNode* p);
    operator NiNode*() const;
};
struct Ptr_0066b0d0 { Ptr_0066b0d0& FUN_0066b0d0(NiNode* value); };
void __cdecl FUN_005b5e40(const char* value);
void __cdecl FUN_00ba91a0(void* value, int a, const void* b);
typedef NiNode* (__thiscall *FUN_00800d50_getter)(NiNode*);
extern char DAT_01078e78;

void FUN_00800e50_Class::FUN_00800d50(int a)
{
    ((char*)this)[0x2b4] = 0;
    for (int i = 0; i < this->f0c; ++i) {
        if (*(int*)((char*)this + i * 8 + 0x14) == a) {
            return;
        }
    }
    if (this->f0c + 1 >= 0x20) {
        FUN_005b5e40(&DAT_01078e78);
        return;
    }
    *(int*)((char*)this + this->f0c * 8 + 0x14) = a;
    ((Ptr_0066b0d0*)((char*)this + this->f0c * 8 + 0x18))->FUN_0066b0d0(((FUN_00800d50_getter)(*(unsigned int*)(*(unsigned int*)a + 0x1d0)))((NiNode*)a));
    this->f0c++;
    if (this->f04 == 0) {
        this->f04 = a;
        ((Ptr_0066b0d0*)((char*)this + 8))->FUN_0066b0d0(((FUN_00800d50_getter)(*(unsigned int*)(*(unsigned int*)a + 0x1d0)))((NiNode*)a));
    }
    FUN_00ba91a0((NiNode*)*((NiPointer<NiNode>*)((char*)this + this->f0c * 8 + 0x18)), 0x31, 0);
}