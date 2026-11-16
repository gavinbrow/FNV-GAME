#include "unit_0ba7b1b86df7.cpp"
void* __cdecl B59890GetMap();
struct B59890MapItem { B59890MapItem* m_pkNext; unsigned int m_key; void* m_val; };
struct B59890Value { ~B59890Value(); static void operator delete(void* p) { g_memoryManager.Deallocate(p); } };
struct B59890Map : NiTMapBaseStub {
    unsigned int m_uiCount;
    B59890MapItem* GetFirstPos() {
        for (unsigned int i=0; i<m_uiHashSize; ++i)
            if (m_ppkHashTable[i]) return (B59890MapItem*)m_ppkHashTable[i];
        return 0;
    }
    void __thiscall GetNext(B59890MapItem*& pkPos, unsigned int& key, void* volatile& value);
};
extern int DAT_011f963c;
extern int DAT_011f9640;
void FUN_00b59890()
{
    B59890MapItem* pkItem = ((B59890Map*)B59890GetMap())->GetFirstPos();
    B59890MapItem* pos = pkItem;
    void* volatile value = 0;
    unsigned int key;
    if (((B59890Map*)B59890GetMap())->m_uiCount > 0 && pkItem != 0) {
        do {
            ((B59890Map*)B59890GetMap())->GetNext(pos, key, value);
            delete (B59890Value*)value;
        } while (pos != 0);
    }
    ((B59890Map*)B59890GetMap())->RemoveAll();
    DAT_011f963c = 0;
    DAT_011f9640 = 0;
}