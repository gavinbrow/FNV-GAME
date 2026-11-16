struct ValueProvider {
    virtual void v00(); virtual void v01(); virtual void v02(); virtual void v03(); virtual void v04();
    virtual void v05(); virtual void v06(); virtual void v07(); virtual void v08(); virtual void v09();
    virtual void v10(); virtual void v11(); virtual void v12(); virtual void v13(); virtual void v14();
    virtual void v15(); virtual void v16(); virtual void v17(); virtual void v18(); virtual void v19();
    virtual void* CreateValue(void* source);
};
struct FUN_00dba760_cls { void* value; void FUN_00dba760(void* newValue); };
struct FUN_00dbaca0_cls {
    ValueProvider* provider;
    void* source;
    FUN_00dba760_cls* FUN_00dbaca0(FUN_00dba760_cls* output);
};
FUN_00dba760_cls* FUN_00dbaca0_cls::FUN_00dbaca0(FUN_00dba760_cls* output) {
    output->FUN_00dba760(provider->CreateValue(source));
    return output;
}
