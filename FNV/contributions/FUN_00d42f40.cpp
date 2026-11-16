struct __declspec(align(16)) Vector4_00d42f40
{
    float x, y, z, w;
};

struct __declspec(align(16)) Transform_00d42f40
{
    Vector4_00d42f40 basisX;
    Vector4_00d42f40 basisY;
    Vector4_00d42f40 basisZ;
    Vector4_00d42f40 translation;
    void __thiscall FUN_00cb2240(const Transform_00d42f40*, const Transform_00d42f40*);
};

struct Shape_00d42f40
{
    void* vtable;
    unsigned int unk04;
    unsigned int unk08;
    unsigned int type;
};

struct TransformShape_00d42f40 : Shape_00d42f40
{
    unsigned int unk10;
    Shape_00d42f40* child;
    unsigned int unk18;
    unsigned int unk1C;
    unsigned int unk20;
    unsigned int unk24;
    unsigned int unk28;
    unsigned int unk2C;
    Transform_00d42f40 transform;
};

struct CollisionBody_00d42f40
{
    Shape_00d42f40* shape;
    unsigned int shapeKey;
    const Transform_00d42f40* transform;
    const CollisionBody_00d42f40* parent;
};

struct CollisionInput_00d42f40;
typedef void (__cdecl *CollisionFunction_00d42f40)(
    const CollisionBody_00d42f40*, const CollisionBody_00d42f40*,
    const CollisionInput_00d42f40*, void*);

struct AgentFunctions_00d42f40
{
    CollisionFunction_00d42f40 process;
    void* create;
    void* closestPoints;
    void* penetrations;
    void* linearCast;
};

struct Dispatcher_00d42f40
{
    CollisionFunction_00d42f40 getFunction(unsigned int firstType, unsigned int secondType) const
    {
        const unsigned char* storage = reinterpret_cast<const unsigned char*>(this);
        const unsigned int lookupRow = firstType + 13;
        const unsigned int agent = storage[lookupRow * 32 + secondType];
        const AgentFunctions_00d42f40* functions =
            reinterpret_cast<const AgentFunctions_00d42f40*>(storage + 0x9A4);
        return functions[agent].process;
    }
};

struct CollisionInput_00d42f40
{
    const Dispatcher_00d42f40* dispatcher;
};

void __cdecl FUN_00d42f40(
    const CollisionBody_00d42f40* first,
    const CollisionBody_00d42f40* second,
    const CollisionInput_00d42f40* input,
    void* output)
{
    const TransformShape_00d42f40* shape =
        static_cast<const TransformShape_00d42f40*>(first->shape);
    Transform_00d42f40 transform;
    transform.FUN_00cb2240(first->transform, &shape->transform);

    CollisionBody_00d42f40 childBody;
    childBody.parent = first;
    childBody.transform = &transform;
    childBody.shape = shape->child;
    childBody.shapeKey = 0;

    input->dispatcher->getFunction(childBody.shape->type, second->shape->type)(
        &childBody, second, input, output);
}
