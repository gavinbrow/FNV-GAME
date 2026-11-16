struct DispatchTarget {
    virtual void Event0();
    virtual void Event1();
    virtual void Event2();
    virtual void Event3();
    virtual void Event4();
    virtual void Event5();
    virtual void Event6();
    virtual void Dispatch(int argument);
};
void __cdecl FUN_00d921e0(void* context, DispatchTarget** target, void* reserved, int argument) {
    (*target)->Dispatch(argument);
}