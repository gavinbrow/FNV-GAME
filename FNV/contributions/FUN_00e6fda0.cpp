struct TransformManager {
virtual void __thiscall slot0() = 0;
virtual void __thiscall slot1() = 0;
virtual void __thiscall slot2() = 0;
virtual void __thiscall slot3() = 0;
virtual void __thiscall slot4() = 0;
virtual void __thiscall slot5() = 0;
virtual void __thiscall slot6() = 0;
virtual void __thiscall slot7() = 0;
virtual void __thiscall slot8() = 0;
virtual void __thiscall slot9() = 0;
virtual void __thiscall slot10() = 0;
virtual void __thiscall slot11() = 0;
virtual void __thiscall UpdateGeometry(void* geometry) = 0;
};
struct D3DDevice {
virtual int __stdcall slot0() = 0;
virtual int __stdcall slot1() = 0;
virtual int __stdcall slot2() = 0;
virtual int __stdcall slot3() = 0;
virtual int __stdcall slot4() = 0;
virtual int __stdcall slot5() = 0;
virtual int __stdcall slot6() = 0;
virtual int __stdcall slot7() = 0;
virtual int __stdcall slot8() = 0;
virtual int __stdcall slot9() = 0;
virtual int __stdcall slot10() = 0;
virtual int __stdcall slot11() = 0;
virtual int __stdcall slot12() = 0;
virtual int __stdcall slot13() = 0;
virtual int __stdcall slot14() = 0;
virtual int __stdcall slot15() = 0;
virtual int __stdcall slot16() = 0;
virtual int __stdcall slot17() = 0;
virtual int __stdcall slot18() = 0;
virtual int __stdcall slot19() = 0;
virtual int __stdcall slot20() = 0;
virtual int __stdcall slot21() = 0;
virtual int __stdcall slot22() = 0;
virtual int __stdcall slot23() = 0;
virtual int __stdcall slot24() = 0;
virtual int __stdcall slot25() = 0;
virtual int __stdcall slot26() = 0;
virtual int __stdcall slot27() = 0;
virtual int __stdcall slot28() = 0;
virtual int __stdcall slot29() = 0;
virtual int __stdcall slot30() = 0;
virtual int __stdcall slot31() = 0;
virtual int __stdcall slot32() = 0;
virtual int __stdcall slot33() = 0;
virtual int __stdcall slot34() = 0;
virtual int __stdcall slot35() = 0;
virtual int __stdcall slot36() = 0;
virtual int __stdcall slot37() = 0;
virtual int __stdcall slot38() = 0;
virtual int __stdcall slot39() = 0;
virtual int __stdcall slot40() = 0;
virtual int __stdcall slot41() = 0;
virtual int __stdcall slot42() = 0;
virtual int __stdcall slot43() = 0;
virtual int __stdcall SetTransform(unsigned int state, const void* matrix) = 0;
};
extern "C" void __cdecl FUN_00b71a40(void* state, void* geometry, void* input, float weight);
struct Renderer {
    D3DDevice* GetDevice() { return *reinterpret_cast<D3DDevice**>(reinterpret_cast<char*>(this) + 0x288); }
    TransformManager* GetManager() { return *reinterpret_cast<TransformManager**>(reinterpret_cast<char*>(this) + 0x8b8); }
    void* GetState() { return reinterpret_cast<char*>(this) + 0x940; }
    void FUN_00e6fda0(void* frame, void* mapping, void* geometry);
};
void Renderer::FUN_00e6fda0(void* frame, void* mapping, void* geometry) {
    GetManager()->UpdateGeometry(geometry);
    const float weight = *reinterpret_cast<float*>(reinterpret_cast<char*>(geometry) + 0x30);
    FUN_00b71a40(GetState(), geometry, reinterpret_cast<char*>(geometry) + 0x24, weight);
    if (*reinterpret_cast<unsigned short*>(reinterpret_cast<char*>(mapping) + 0x20) <= 4) {
        const char* const matrixBase = *reinterpret_cast<const char**>(reinterpret_cast<char*>(frame) + 0x28);
        for (unsigned int i = 0; i < 4; ++i) {
            GetDevice()->SetTransform(0x100 + i, matrixBase + 64 * (*reinterpret_cast<unsigned short**>(reinterpret_cast<char*>(mapping) + 4))[i]);
        }
    }
}
