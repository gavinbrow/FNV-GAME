
struct NiRTTI {
    const char* name;
    const NiRTTI* parent;
};
extern "C" NiRTTI DAT_01202500;
extern "C" NiRTTI DAT_01202530;
struct NiObject {
    const NiRTTI* QueryRTTI() {
        typedef const NiRTTI* (__thiscall *Fn)(NiObject*);
        return ((Fn*)*(void***)this)[2](this);
    }
    void Update(unsigned int value) {
        typedef void (__thiscall *Fn)(NiObject*, unsigned int);
        ((Fn*)*(void***)this)[54](this, value);
    }
    unsigned short MeshChildCount() const {
        return *(const unsigned short*)((const char*)this + 0x60);
    }
    unsigned short ChildCount() const {
        return *(const unsigned short*)((const char*)this + 0x22);
    }
    NiObject** MeshChildren() const {
        return *(NiObject** const*)((const char*)this + 0x58);
    }
    NiObject** Children() const {
        return *(NiObject** const*)((const char*)this + 0x1c);
    }
    void __thiscall FUN_00c21a10(unsigned int);
    void __thiscall FUN_00a809b0(unsigned int);
    void __thiscall FUN_00c21cb0(unsigned int);
};
struct NiObjectNode {
    NiObjectNode* next;
    NiObjectNode* previous;
    NiObject* object;
    static NiObject*& GetNext(NiObjectNode*& it) { NiObject*& result = it->object; it = it->next; return result; }
};
void __thiscall NiObject::FUN_00c21cb0(unsigned int value) {
    FUN_00a809b0(value);
    NiObject* linked = *(NiObject**)((char*)this + 0xb8);
    if (linked) {
        NiObject* child = *(NiObject**)((char*)linked + 0x7c);
        if (child) child->Update(value);
        linked->FUN_00c21a10(value);
    }
    for (NiObjectNode* node = *(NiObjectNode**)((char*)this + 0xc8); node;) {
        NiObject* object = NiObjectNode::GetNext(node);
        if (!object) continue;
        for (const NiRTTI* type = object->QueryRTTI(); type; type = type->parent) {
            if (type == &DAT_01202500) {
                unsigned int count = object->MeshChildCount();
                for (unsigned int i=0; i<count; ++i) {
                    if (i < object->MeshChildCount()) {
                        NiObject* child = object->MeshChildren()[i];
                        if (child) child->Update(value);
                    }
                }
                goto next_object;
            }
        }
        for (const NiRTTI* type = object->QueryRTTI(); type; type = type->parent) {
            if (type == &DAT_01202530) {
                unsigned int count = object->ChildCount();
                for (unsigned int i=0; i<count; ++i) {
                    if (i < object->ChildCount()) {
                        NiObject* child = object->Children()[i];
                        if (child) child->Update(value);
                    }
                }
                goto next_object;
            }
        }
        next_object: ;
    }
}
