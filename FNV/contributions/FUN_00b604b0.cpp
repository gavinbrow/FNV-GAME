extern "C" unsigned int __cdecl strlen(const char*);
extern "C" int __cdecl strcpy_s(char*, unsigned int, const char*);
void* __cdecl FUN_00aa1070(unsigned int);
extern "C" __declspec(dllimport) long __stdcall InterlockedDecrement(volatile long*);
extern "C" __declspec(dllimport) long __stdcall InterlockedIncrement(volatile long*);

struct ManagedRef {
    virtual void v0();
    virtual void DeleteThis();
    volatile long refCount;
    void IncRefCount() { InterlockedIncrement(&refCount); }
    void DecRefCount() { if (InterlockedDecrement(&refCount) == 0) DeleteThis(); }
};

template <class T> struct RefPtr {
    T* value;
    RefPtr(const RefPtr& other) : value(other.value) { if (value) value->IncRefCount(); }
    ~RefPtr() { if (value) value->DecRefCount(); }
    RefPtr& operator=(const RefPtr& other) {
        if (value != other.value) {
            if (value) value->DecRefCount();
            value = other.value;
            if (value) value->IncRefCount();
        }
        return *this;
    }
};

struct AssignedString {
    int unk00;
    char* text;
    RefPtr<ManagedRef> object;
};

struct FUN_00b604b0_class {
    int unk00;
    int unk04;
    int unk08;
    int unk0c;
    bool copyText;
    void FUN_00b604b0(AssignedString* out, const char* input, RefPtr<ManagedRef> ref);
};

void FUN_00b604b0_class::FUN_00b604b0(AssignedString* out, const char* input, RefPtr<ManagedRef> ref) {
    if (copyText) {
        unsigned int length = strlen(input) + 1;
        char* buffer = static_cast<char*>(FUN_00aa1070(length));
        out->text = buffer;
        strcpy_s(buffer, length, input);
    } else {
        out->text = const_cast<char*>(input);
    }
    out->object = ref;
}
