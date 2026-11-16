extern "C" __declspec(dllimport) long __stdcall InterlockedDecrement(volatile long*);

struct RefObject {
    virtual void Acquire();
    virtual void ReleaseObject();
    volatile long refCount;

    void DecRefCount() {
        if (InterlockedDecrement(&refCount) == 0)
            ReleaseObject();
    }
};

struct SharedRef {
    RefObject* ptr;
    ~SharedRef() throw() {
        if (ptr)
            ptr->DecRefCount();
    }
    void Reset() {
        if (ptr) {
            ptr->DecRefCount();
            ptr = 0;
        }
    }
};

struct BaseController {
    virtual ~BaseController() throw();
    unsigned int unk004;
    unsigned int unk008;
    unsigned int unk00c;
    unsigned int unk010;
    unsigned int unk014;
    unsigned int unk018;
    unsigned int unk01c;
    unsigned int unk020;
    unsigned int unk024;
    unsigned int unk028;
    unsigned int unk02c;
    unsigned int unk030;
    unsigned int unk034;
    unsigned int unk038;
    unsigned int unk03c;
    unsigned int unk040;
    unsigned int unk044;
};

struct FUN_00a45b60 : BaseController {
    SharedRef owner;
    virtual ~FUN_00a45b60() throw();
};

FUN_00a45b60::~FUN_00a45b60() throw()
{
    owner.Reset();
}
