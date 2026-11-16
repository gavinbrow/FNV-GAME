#include "h_74712c1d3c73.h"

extern bool __cdecl FUN_00a614d0(int, int);

struct NiShaderBase
{
    virtual void M00() {}
    virtual void Release() = 0;
    virtual void M01() {}
    virtual void M02() {}
    virtual void M03() {}
    virtual void M04() {}
    virtual void M05() {}
    virtual void M06() {}
    virtual void M07() {}
    virtual void M08() {}
    virtual void M09() {}
    virtual void M10() {}
    virtual void M11() {}
    virtual void M12() {}
    virtual void M13() {}
    virtual void M14() {}
    virtual void M15() {}
    virtual void M16() {}
    virtual void M17() {}
    virtual void M18() {}
    virtual void M19() {}
    virtual void M20() {}
    virtual void M21() {}
    virtual void M22() {}
    virtual void M23() {}
    virtual void M24() {}
    virtual void M25() {}
    virtual void M26() {}
    virtual void M27() {}
    virtual void M28() {}
    virtual void M29() {}
    virtual void M30() {}
    virtual void M31() {}
    virtual void M32() {}
    virtual void M33() {}
    virtual void M34() {}
    virtual void M35() {}
    virtual void M36() {}
    virtual void M37() {}
};

class NiShader : public NiShaderBase
{
public:
    long m_refCount;
    int m_hash;

    virtual void Release();
    virtual int* GetHash();
};

struct FUN_00a61920_Node
{
    NiShader* m_pObject;
    int unk04;
    FUN_00a61920_Node* m_pkNext;
    short unk0c;
    short unk0e;
};

class FUN_00a61920_Class
{
public:
    FUN_00a61920_Node* m_pBuckets[1];

    bool __thiscall FUN_00a61920(int, int, NiShader**);
};

void NiShader::Release()
{
}

int* NiShader::GetHash()
{
    return &m_hash;
}

bool __thiscall FUN_00a61920_Class::FUN_00a61920(
    int index,
    int string,
    NiShader** out)
{
    FUN_00a61920_Node* node = m_pBuckets[index];
    bool found = false;

    if (node != 0) {
        do {
            int* hash = node->m_pObject->GetHash();
            int value = static_cast<int>(node->unk0e) + *hash;

            if (FUN_00a614d0(string, value)) {
                NiShader* oldObject = *out;

                if (oldObject != node->m_pObject) {
                    if (oldObject != 0) {
                        if (InterlockedDecrement(&oldObject->m_refCount) == 0) {
                            oldObject->Release();
                        }
                    }

                    *out = node->m_pObject;

                    if (*out != 0) {
                        InterlockedIncrement(&(*out)->m_refCount);
                    }
                }

                found = true;
                break;
            }

            node = node->m_pkNext;
        } while (node != 0);
    }

    return found;
}