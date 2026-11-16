
struct LightManager {
    void FUN_00e6fe30(void* geometry, int transform, int flag0, int pass, int enabled);
};
extern LightManager* DAT_011f9508;
extern void* DAT_0126f74c;
extern "C" const char DAT_010A1CAC[];

struct ShaderVirtualObject {
    void** vtable;
};
typedef void* (__thiscall *FindConstantFn)(void*, const char*, void*, unsigned short, int, void*);
typedef void (__thiscall *ApplyConstantFn)(void*, void*);
typedef void (__thiscall *ApplyConstantDataFn)(void*, void*, void*, unsigned short, int, void*);

struct ShaderAdapter : ShadowLightShader {
    int FUN_00b7a2c0(int a1, void* geometry, void* constantData, int a4,
                     int a5, int a6, int transform, int a8);
};

int ShaderAdapter::FUN_00b7a2c0(int a1, void* geometry, void* constantData, int a4,
                                int a5, int a6, int transform, int a8)
{
    if ((constantData && *reinterpret_cast<int*>(layoutPadding38) == 0 &&
         DAT_011fec00.m_pObject &&
         *reinterpret_cast<char*>(reinterpret_cast<char*>(DAT_011fec00.m_pObject) + 8)) ||
        m_spVertexConstantMap.m_pObject == spTexEffectVConstantMap.m_pObject) {
        DAT_011f9508->FUN_00e6fe30(geometry, transform, 0, 3, 1);
        void* geometryData = *reinterpret_cast<void**>(reinterpret_cast<char*>(geometry) + 0x28);
        if (m_spVertexConstantMap.m_pObject == spTexEffectVConstantMap.m_pObject) {
            ShaderVirtualObject* pass = *reinterpret_cast<ShaderVirtualObject**>(
                reinterpret_cast<char*>(DAT_0126f74c) + 0x5c);
            ShaderVirtualObject* map = reinterpret_cast<ShaderVirtualObject*>(
                spTexEffectVConstantMap.m_pObject);
            void** applySlot = pass->vtable + 30;
            void* result = reinterpret_cast<FindConstantFn>(reinterpret_cast<void* volatile*>(map->vtable)[28])(
                map, DAT_010A1CAC,
                geometryData,
                *reinterpret_cast<unsigned short*>(reinterpret_cast<char*>(constantData) + 0x20),
                3,
                *reinterpret_cast<void**>(reinterpret_cast<char*>(constantData) + 4));
            reinterpret_cast<ApplyConstantFn>(*applySlot)(pass, result);
        } else {
            ShaderVirtualObject* pass = *reinterpret_cast<ShaderVirtualObject**>(
                reinterpret_cast<char*>(DAT_0126f74c) + 0x5c);
            reinterpret_cast<ApplyConstantDataFn>(pass->vtable[30])(
                pass, DAT_011fec00.m_pObject,
                geometryData,
                *reinterpret_cast<unsigned short*>(reinterpret_cast<char*>(constantData) + 0x20),
                3,
                *reinterpret_cast<void**>(reinterpret_cast<char*>(constantData) + 4));
        }
    }
    return 0;
}
