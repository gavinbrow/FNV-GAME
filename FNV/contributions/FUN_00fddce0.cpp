extern "C" __declspec(dllimport) long __stdcall InterlockedDecrement(volatile long *);
struct RefObject {
    virtual void stub();
    virtual void destroy();
    volatile long refs;
    void decRef() {
       if (InterlockedDecrement(&refs) == 0) destroy();
    }
};
extern "C" RefObject* DAT_012043c0;
struct FUN_00fddce0 {
  ~FUN_00fddce0() {
    if (DAT_012043c0) DAT_012043c0->decRef();
  }
};
FUN_00fddce0 g_destruct_ref;