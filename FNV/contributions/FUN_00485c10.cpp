struct FormMap {
    void FUN_00405430(unsigned int);
    void FUN_00844700(unsigned int, TESForm*);
};
struct DebugTarget {
    virtual void v00(); virtual void v01(); virtual void v02(); virtual void v03();
    virtual void v04(); virtual void v05(); virtual void v06(); virtual void v07();
    virtual void v08(); virtual void v09(); virtual void v10(); virtual void v11();
    virtual void v12(); virtual void v13(); virtual void v14(); virtual void v15();
    virtual void v16(); virtual void v17(); virtual void v18(); virtual void v19();
    virtual void v20(); virtual void v21(); virtual void v22(); virtual void v23();
    virtual void v24(); virtual void v25(); virtual void v26(); virtual void v27();
    virtual void v28(); virtual void v29(); virtual void v30(); virtual void v31();
    virtual void v32(); virtual void v33(); virtual void v34(); virtual void v35();
    virtual void GetDebugInfo(BSStringT<char>*);
};
extern const char DAT_0101c9c8[];
extern unsigned char DAT_011c54b9;
void __cdecl FUN_00461300();
struct FUN_00485c10_shell : public TESForm {
    bool FUN_004077c0();
    const char* FUN_00440e30();
    void FUN_00485c10(unsigned int id, bool notify);
};
void FUN_00485c10_shell::FUN_00485c10(unsigned int id, bool notify) {
    if (id == iFormID)
        return;
    if (!FUN_004077c0()) {
        DebugTarget* debug = 0;
        if (iFormID != 0) {
            reinterpret_cast<FormMap*>(TESForm::pAllForms)->FUN_00405430(iFormID);
        }
        debug = 0;
        if (debug != 0) {
            FUN_00461300();
            BSStringT<char> details;
            debug->GetDebugInfo(&details);
            _FNV_Warning(DAT_0101c9c8, id, FUN_00440e30(), details.String());
            DAT_011c54b9 = 1;
        } else if (notify && iFormID != 0) {
            g_dataHandler->FUN_004696f0(iFormID);
        }
        if (id != 0) {
            reinterpret_cast<FormMap*>(TESForm::pAllForms)->FUN_00844700(id, this);
        }
    }
    iFormID = id;
}