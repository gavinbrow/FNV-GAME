struct FUN_004d9100 {
    virtual ~FUN_004d9100();
    unsigned int length;
    unsigned int capacity;
    void* elements;
    FUN_004d9100(unsigned int initialCapacity, unsigned int growthCapacity);
    unsigned int FUN_00658930();
    void** FUN_00877a30(unsigned int index);
    void FUN_005e03d0();
};
struct FNVObjectName {
    void* FUN_00559450();
};
struct FNVTreeNode {
    virtual void* f0();
    virtual void* f1();
    virtual FNVObjectName* GetName();
    virtual void* f3(); virtual void* f4(); virtual void* f5();
    virtual void* f6(); virtual void* f7(); virtual void* f8();
    virtual void* f9(); virtual void* f10(); virtual void* f11();
    virtual void* f12(); virtual void* f13(); virtual void* f14();
    virtual void* f15(); virtual void* f16(); virtual void* f17();
    virtual void* f18(); virtual void* f19(); virtual void* f20();
    virtual void* f21(); virtual void* f22(); virtual void* f23();
    virtual void CollectChildren(FUN_004d9100* result);
};
struct FNVTreeItem {
    unsigned int mask;
    void* itemHandle;
    unsigned int state;
    unsigned int stateMask;
    char* text;
    int textCapacity;
    int image;
    int selectedImage;
    int nodeArray;
    FNVTreeNode* node;
    int integralHeight;
    unsigned int extendedState;
    void* ownerWindow;
    int expandedImage;
};
struct FNVTreeInsert {
    void* parent;
    void* insertAfter;
    FNVTreeItem item;
};
struct FNVChildLink {
    FNVObjectName* FUN_006815c0();
    FNVChildLink* FUN_00726070();
};
struct FNVTypeA {
    FNVObjectName* FUN_004ae6a0();
};
struct FNVTypeB {
    int FUN_00c8d0d0();
    FNVChildLink* FUN_007d6bb0();
};
struct FNVTypeC {
    FNVTreeNode* FUN_004d8630();
};
struct FNVTypeD {
    unsigned int FUN_004d8560();
    FNVTreeNode* FUN_004d85a0(unsigned int index);
};
struct FNVTypeE {
    FNVTreeNode* FUN_004d8510();
};
struct FNVTypeF {
    FNVTreeNode* FUN_004d8530();
};
extern unsigned char DAT_01268110;
extern unsigned char DAT_012681c0;
extern unsigned char DAT_01268100;
extern unsigned char DAT_012681b4;
extern unsigned char DAT_012681a8;
extern unsigned char DAT_01268198;
extern unsigned char DAT_0126818c;
extern void* __cdecl FUN_00653270(const void*, void*);
extern char* __cdecl FUN_00464f30(const void*, int);
extern void __cdecl FUN_004add50(char*, const char*, unsigned int);
struct FUN_004d80b0_Class {
    void* m_object;
    void* m_owner;
    void* m_root;
    void* m_treeWindow;
    void __thiscall FUN_004d80b0(void* parent, FNVTreeNode* node);
};
void FUN_004d80b0_Class::FUN_004d80b0(void* parent, FNVTreeNode* node)
{
    unsigned int childIndex;
    FUN_004d9100* nodeArray;
    FNVTypeA* partA;
    if (node) {
    nodeArray = new FUN_004d9100(128, 128);
    char displayName[64];
    {
    FNVTreeInsert insertion;
    insertion.insertAfter = (void*)0xffff0002;
    insertion.item.mask = 0x27;
    insertion.item.node = node;
    FUN_004add50(displayName, (const char*)node->GetName()->FUN_00559450(), 63);
    displayName[63] = 0;
    insertion.item.text = FUN_00464f30(displayName, 0);
    insertion.item.image = 0;
    insertion.item.selectedImage = insertion.item.image;
    insertion.parent = parent;
    insertion.parent = ((void* (__stdcall *)(void*, int, int, int))DAT_00fdf28c)(m_treeWindow, 0x1100, 0, (int)&insertion);
    parent = insertion.parent;
    node->CollectChildren(nodeArray);
    for (childIndex = 0; childIndex < nodeArray->FUN_00658930(); ++childIndex) {
        insertion.item.text = FUN_00464f30(*nodeArray->FUN_00877a30(childIndex), 0);
        insertion.item.image = 6;
        insertion.item.selectedImage = insertion.item.image;
        DAT_00fdf28c(m_treeWindow, 0x1100, 0, (int)&insertion);
    }
    nodeArray->FUN_005e03d0();
    }
    partA = (FNVTypeA*)FUN_00653270(&DAT_01268110, node);
    if (partA) {
        FNVTreeNode* childNode = (FNVTreeNode*)partA->FUN_004ae6a0();
        FUN_004d80b0(parent, childNode);
        FNVTypeB* partB = (FNVTypeB*)FUN_00653270(&DAT_012681c0, node);
        if (partB && partB->FUN_00c8d0d0()) {
            FNVChildLink* link = partB->FUN_007d6bb0();
            while (link && link->FUN_006815c0()->FUN_00559450()) {
                FUN_004d80b0(parent, (FNVTreeNode*)link->FUN_006815c0()->FUN_00559450());
                link = link->FUN_00726070();
            }
        }
    } else {
        FNVTypeD* partD = (FNVTypeD*)FUN_00653270(&DAT_01268100, node);
        if (partD) {
            FNVTypeC* partC = (FNVTypeC*)FUN_00653270(&DAT_012681b4, partD);
            if (partC) {
                FUN_004d80b0(parent, partC->FUN_004d8630());
            } else {
                FNVTypeD* partE = (FNVTypeD*)FUN_00653270(&DAT_012681a8, partD);
                if (partE) {
                    unsigned int count = partE->FUN_004d8560();
                    if (count) {
                        for (unsigned int index = 0; index < count; ++index) {
                            FUN_004d80b0(parent, partE->FUN_004d85a0(index));
                        }
                    }
                }
            }
        } else {
            FNVTypeE* partE = (FNVTypeE*)FUN_00653270(&DAT_01268198, node);
            if (partE) {
                FUN_004d80b0(parent, partE->FUN_004d8510());
            } else {
                FNVTypeF* partF = (FNVTypeF*)FUN_00653270(&DAT_0126818c, node);
                if (partF) {
                    FUN_004d80b0(parent, partF->FUN_004d8530());
                }
            }
        }
    }
    delete nodeArray;
    }
}
