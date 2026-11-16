
extern __declspec(thread) int gShaderAllocationContext;
extern "C" void* __cdecl FUN_00aa13e0(unsigned int);
extern "C" char DAT_010a1e50, DAT_010af648, DAT_01011584;
extern "C" char DAT_010b8c54, DAT_010b8c48, DAT_010b8c34, DAT_010b8c24;
extern "C" char DAT_010b8c10, DAT_010b8bfc, DAT_010b8bec;
extern "C" char DAT_011fd884, DAT_011fa280, DAT_011fa290, DAT_01200510;
struct AllocationScope {
    int previous;
    AllocationScope() : previous(gShaderAllocationContext) { gShaderAllocationContext = 28; }
    ~AllocationScope() { gShaderAllocationContext = previous; }
};
struct ShaderVariableMap : RefObj_bacd00 {
    ShaderVariableMap(void* context, int mode);
    static void* operator new(unsigned int) { return FUN_00aa13e0(0x44); }
    virtual void Register(const void* name, unsigned int type, int a, int b, int c, const void* desc, int stride, int count, const void* data, int optional);
    typedef int (__thiscall* LookupFn)(ShaderVariableMap*, const void*);
    int Lookup(const void* name) {
        return reinterpret_cast<LookupFn>((*reinterpret_cast<void***>(this))[28])(this,name);
    }
};
struct ShaderRegister {
    void FUN_00bad100();
};
void ShaderRegister::FUN_00bad100() {
    AllocationScope allocScope;
    RefPtr_bacd00& mainGroup = *reinterpret_cast<RefPtr_bacd00*>(reinterpret_cast<char*>(this) + 0x34);
    RefPtr_bacd00& extraGroup = *reinterpret_cast<RefPtr_bacd00*>(reinterpret_cast<char*>(this) + 0x30);
    if (!mainGroup.m_pObject) {
        mainGroup = new ShaderVariableMap(*reinterpret_cast<void**>(reinterpret_cast<char*>(this) + 0x18), 0);
        static_cast<ShaderVariableMap*>(mainGroup.m_pObject)->Register(&DAT_010a1e50,0x20000009,0,9,4,0,0,0,0,0);
        static_cast<ShaderVariableMap*>(mainGroup.m_pObject)->Register(&DAT_010af648,0x10000007,0,13,1,&DAT_01011584,0x10,4,&DAT_011fd884,0);
        static_cast<ShaderVariableMap*>(mainGroup.m_pObject)->Register(&DAT_010b8c54,0x10000007,0,15,1,&DAT_01011584,0x10,4,&DAT_011fa280,0);
        static_cast<ShaderVariableMap*>(mainGroup.m_pObject)->Register(&DAT_010b8c48,0x10000007,0,14,1,&DAT_01011584,0x10,4,&DAT_011fa290,0);
        static_cast<ShaderVariableMap*>(mainGroup.m_pObject)->Register(&DAT_010b8c34,0x10000009,0,0,9,&DAT_01011584,0x90,4,&DAT_01200510,0);
        unsigned int count = *reinterpret_cast<unsigned short*>(reinterpret_cast<char*>(this) + 0x1ac);
        static_cast<ShaderVariableMap*>(mainGroup.m_pObject)->Register(&DAT_010b8c24,0x10000009,0,20,count,&DAT_01011584,count<<4,4,*reinterpret_cast<void**>(reinterpret_cast<char*>(this) + 0x1a4),0);
        *reinterpret_cast<int*>(reinterpret_cast<char*>(this) + 0x1a8) = static_cast<ShaderVariableMap*>(mainGroup.m_pObject)->Lookup(&DAT_010b8c24);
    }
    if (!extraGroup.m_pObject) {
        extraGroup = new ShaderVariableMap(*reinterpret_cast<void**>(reinterpret_cast<char*>(this) + 0x18), 2);
        static_cast<ShaderVariableMap*>(extraGroup.m_pObject)->Register(&DAT_010b8c10,0x10000007,0,2,1,&DAT_01011584,0x10,4,reinterpret_cast<char*>(this)+0x1b0,0);
        static_cast<ShaderVariableMap*>(extraGroup.m_pObject)->Register(&DAT_010b8bfc,0x10000007,0,4,1,&DAT_01011584,0x10,4,reinterpret_cast<char*>(this)+0x1c0,0);
        static_cast<ShaderVariableMap*>(extraGroup.m_pObject)->Register(&DAT_010b8bec,0x10000007,0,3,1,&DAT_01011584,0x10,4,reinterpret_cast<char*>(this)+0x1d0,0);
    }
}