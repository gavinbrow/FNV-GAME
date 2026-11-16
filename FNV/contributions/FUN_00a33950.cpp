
extern int (__stdcall* DAT_00fdf1c0)(void*);
extern "C" __declspec(dllimport) long __stdcall InterlockedDecrement(long volatile*);

struct A33950RefObject {
    virtual void Unused();
    virtual void Release();
    volatile long refCount;
};

struct A33950BinaryInput {
    void* vtable;
    unsigned int position;
    unsigned int (__cdecl *readFn)(A33950BinaryInput*, void*, unsigned int, unsigned int*, unsigned int);
    void Read(void* destination, unsigned int bytes) {
        unsigned int componentSize = bytes;
        position += readFn(this, destination, bytes, &componentSize, 1);
    }
};

struct A33950Stream {
    A33950RefObject* FUN_00a64620();
    unsigned int& Version() { return *(unsigned int*)((char*)this + 0xd8); }
    unsigned int& Count() { return *(unsigned int*)((char*)this + 4); }
    A33950BinaryInput* Input() { return *(A33950BinaryInput**)((char*)this + 0x24c); }
};

struct A33950Object {
    A33950RefObject* first;
    A33950RefObject* second;
    unsigned char unk08;
    unsigned char unk09;
    unsigned char unk0a;
    unsigned char unk0b;
    unsigned char unk0c;
    unsigned char flag0d;
    void FUN_00a33950(A33950Stream* stream);
};

void A33950Object::FUN_00a33950(A33950Stream* stream) {
    A33950RefObject* next = stream->FUN_00a64620();
    A33950RefObject* previous = first;
    if (previous != next) {
        if (previous && InterlockedDecrement(&previous->refCount) == 0)
            previous->Release();
        first = next;
        if (next)
            DAT_00fdf1c0((void*)&next->refCount);
    }

    next = stream->FUN_00a64620();
    previous = second;
    if (previous != next) {
        if (previous && InterlockedDecrement(&previous->refCount) == 0)
            previous->Release();
        second = next;
        if (next)
            DAT_00fdf1c0((void*)&next->refCount);
    }

    if (stream->Version() < 0x0a01006f) {
        unsigned short oldValue;
        stream->FUN_00a64620();
        stream->Input()->Read(&oldValue, 2);
    }
    if (stream->Count() > 0)
        stream->Input()->Read(&flag0d, 1);
}