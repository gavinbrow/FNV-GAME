void* __fastcall FUN_005ac020(Script*);

struct FUN_005a9d00_shell : public ScriptLocals {
    void FUN_005a8c90();
    void FUN_005a8ea0();
    void FUN_005a9d00();
};

void FUN_005a9d00_shell::FUN_005a9d00()
{
    FUN_005a8c90();
    FUN_005a8ea0();
    if (m_pMasterScript)
        m_pLocalList = (BSSimpleList<SCRIPT_LOCAL*>*)FUN_005ac020(m_pMasterScript);
    if (m_pScriptEffectData)
        delete (void*)m_pScriptEffectData;
    m_pScriptEffectData = 0;
}