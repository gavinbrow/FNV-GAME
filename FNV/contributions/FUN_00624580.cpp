struct SceneList { SceneList* FUN_00624700(); int FUN_00726070(); void** FUN_00629ab0(int offset); };
struct Geometry { Geometry* FUN_0044ddc0(); Geometry* FUN_005497a0(); };
struct SceneObject { Geometry* FUN_008d6f30(); };
Geometry* __cdecl FUN_004b5a50(void* object);
SceneObject* __cdecl FUN_0056f930(Geometry* object);
bool __cdecl FUN_008c7aa0();
void __cdecl FUN_0054abd0(SceneObject* object, Geometry* geometry);
void __cdecl FUN_00624560();
struct FUN_00624580_Class { void __thiscall FUN_00624580(SceneList* object); };
void FUN_00624580_Class::FUN_00624580(SceneList* object)
{
    if (!object) return;
    SceneList* count = object->FUN_00624700();
    int items = count->FUN_00726070();
    void* index;
    for (int sceneObject = 0; sceneObject < items; ++sceneObject)
    {
        index = *count->FUN_00629ab0(sceneObject);
        Geometry* handle = FUN_004b5a50(index);
        Geometry* geometry = handle ? handle->FUN_0044ddc0() : 0;
        SceneObject* parent = geometry ? FUN_0056f930(geometry) : 0;
        if (parent)
        {
            typedef unsigned char (__thiscall* Predicate)(SceneObject*);
            typedef void (__thiscall* Dispatch)(SceneObject*, int);
            typedef int (__thiscall* Retrieve)(SceneObject*, int);
            if (!reinterpret_cast<Predicate>((*reinterpret_cast<void***>(parent))[64])(parent))
            {
                reinterpret_cast<Dispatch>((*reinterpret_cast<void***>(parent))[18])(parent, 4);
                Geometry* target;
                Geometry* owner = parent->FUN_008d6f30();
                target = owner ? owner->FUN_005497a0() : 0;
                if (target)
                {
                    if (FUN_008c7aa0()) FUN_0054abd0(parent, target);
                    else reinterpret_cast<Dispatch>((*reinterpret_cast<void***>(target))[55])(
                           reinterpret_cast<SceneObject*>(target),
                           reinterpret_cast<Retrieve>((*reinterpret_cast<void***>(parent))[116])(parent, 1));
                }
                if (reinterpret_cast<Predicate>((*reinterpret_cast<void***>(parent))[84])(parent))
                    FUN_00624560();
            }
        }
    }
}