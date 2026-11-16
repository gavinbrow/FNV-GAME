
extern "C" void __cdecl FUN_00aa0020(int, int, const char*, ...);
extern "C" __declspec(dllimport) void __stdcall EnterCriticalSection(void*);
extern "C" __declspec(dllimport) void __stdcall LeaveCriticalSection(void*);
extern "C" char UNK_010f0b84[];
extern "C" char UNK_010f0b20[];
extern "C" char UNK_010f0b54[];

class ShaderLibraryProducer {
public:
    virtual void Reserved0();
    virtual void Reserved1();
    virtual ShaderLibrary* CreateShader(ShaderRenderer*, const char*, unsigned int);
};
class Logger {
public:
    virtual void Reserved0();
    virtual void Reserved1();
    virtual void Reserved2();
    virtual void Reserved3();
    virtual void Reserved4();
    virtual void Log(int, const char*, int, int, int);
};
extern "C" Logger* DAT_011f6388;

class ShaderFactory {
public:
    virtual void Reserved0();
    virtual void Reserved1();
    virtual void Reserved2();
    virtual ShaderLibrary* FindShader(const char*, unsigned int);
    virtual void Reserved4();
    virtual void Reserved5();
    virtual void RegisterShader(ShaderLibrary*, unsigned int);
    virtual void Reserved7();
    virtual void Reserved8();
    virtual void Reserved9();
    virtual void Reserved10();
    virtual void Reserved11();
    virtual void Reserved12();
    virtual void Reserved13();
    virtual ShaderLibraryProducer* GetFirstLibrary();
    virtual ShaderLibraryProducer* GetNextLibrary();

    int unk04;
    int unk08;
    int unk0C;
    int unk10;
    int unk14;
    int unk18;
    int unk1C;
    int unk20;
    ShaderRenderer* m_pkRenderer;
    int m_pkShaderMap;
    int m_kLibraryIter;
    int m_pkLibraryMap;
    int unk34;
    int unk38;
    int unk3C;
    int unk40;
    int unk44;
    int unk48;
    int unk4C;
    int unk50;
    int unk54;
    int unk58;
    int unk5C;
    int unk60;
    int unk64;
    int unk68;
    int unk6C;
    int unk70;
    int unk74;
    int unk78;
    int unk7C;
    int m_kShaderMapLock;

    ShaderLibrary* FUN_00e920a0(const char* pcName, unsigned int uiImplementation, bool bReportFailure);
};
ShaderLibrary* ShaderFactory::FUN_00e920a0(const char* pcName, unsigned int uiImplementation, bool bReportFailure)
{
    if (!m_pkRenderer) {
        if (DAT_011f6388)
            DAT_011f6388->Log(4, UNK_010f0b84, 0, 0, 0);
        return 0;
    }
    if (!pcName || !*pcName) {
        FUN_00aa0020(1, 0, UNK_010f0b20);
        return 0;
    }
    ShaderLibrary* pkShader = FindShader(pcName, uiImplementation);
    if (!pkShader) {
        void* pLock = &m_kShaderMapLock;
        EnterCriticalSection(pLock);
        ShaderLibraryProducer* pkLibrary = GetFirstLibrary();
        pkShader = FindShader(pcName, uiImplementation);
        if (!pkShader) {
            while (pkLibrary) {
                pkShader = pkLibrary->CreateShader(m_pkRenderer, pcName, uiImplementation);
                if (pkShader) {
                    RegisterShader(pkShader, uiImplementation);
                    m_pkRenderer->FUN_00e752b0(pkShader);
                    pkShader->FUN_00e818d0(m_pkRenderer);
                    break;
                }
                pkLibrary = GetNextLibrary();
            }
        }
        LeaveCriticalSection(pLock);
    }
    if (bReportFailure && !pkShader)
        FUN_00aa0020(1, 0, UNK_010f0b54, pcName, uiImplementation);
    return pkShader;
}
