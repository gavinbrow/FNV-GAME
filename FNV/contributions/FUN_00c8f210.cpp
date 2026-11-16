struct NiNode;
struct HavokShape {
    void FUN_00c8f080();
    void FUN_00c8eb20(void* context);
};
struct HavokLookup {
    void* unused0;
    void* unused4;
    void* unused8;
    void* unusedC;
    HavokShape* shape;
};
struct HavokProperty {
    HavokLookup* FUN_00653290(const void* key);
};
struct HavokObject {
    virtual void Virt0();
    virtual void Virt1();
    virtual void Virt2();
    virtual NiNode* GetChildNode();

    unsigned int referenceCount;
    void* extraData;
    void* userData;
    void* collisionData;
    void* owner;
    void* source;
    HavokProperty* property;

    void FUN_00a68bf0();
};
struct NiTransform {
    float rotation[3][3];
    float translation[3];
    float scale;
};
struct NiBound {
    float center[3];
    float radius;
};
struct NiNode {
    void* vtbl;
    unsigned int referenceCount;
    const char* name;
    void* controller;
    void* extraData;
    unsigned short extraDataCount;
    unsigned short extraDataCapacity;
    void* parent;
    NiBound worldBound;
    NiTransform local;
    NiTransform world;
    void* collisionObject;
    unsigned int flags;
    unsigned int unknown9C;
    HavokObject** children;
    unsigned short maxChildren;
    unsigned short childCount;
};
extern char DAT_012043f8;
void __cdecl FUN_00c8f210(HavokObject* object, int operation, void* context)
{
    if (object != 0) {
        object->FUN_00a68bf0();
        HavokProperty* property = object->property;
        if (property != 0) {
            HavokLookup* lookup = property->FUN_00653290(&DAT_012043f8);
            if (lookup != 0 && lookup->shape != 0) {
                if ((char)operation)
                    lookup->shape->FUN_00c8f080();
                else
                    lookup->shape->FUN_00c8eb20(context);
            }
        }
        NiNode* node = object->GetChildNode();
        if (node) {
            for (unsigned int index = 0; index < node->childCount; ++index)
                FUN_00c8f210(node->children[index], operation, context);
        }
    }
}