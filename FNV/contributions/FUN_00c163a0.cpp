struct RefHandle {
    RefObject* object;
    explicit RefHandle(RefObject* ptr = 0) : object(ptr) {}
    ~RefHandle() {
        if (object != 0)
            object->DecRefCount(DAT_00fdf1c4);
    }
    operator RefObject*() const { return object; }
};
extern RefHandle DAT_011fda48[208];
RefObject* __cdecl FUN_00c163a0(unsigned int index) {
    return index <= 207 ? DAT_011fda48[index] : static_cast<const RefHandle&>(RefHandle());
}
