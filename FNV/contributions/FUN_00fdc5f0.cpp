void operator delete(void*);
struct Deallocator { ~Deallocator(){volatile int pad[7]; typedef char T; delete *reinterpret_cast<T**>(this);} };
struct ElQ { void* ptr; void FUN_00b17f50(); ~ElQ(){ FUN_00b17f50();} };
struct BranchLeaves: Deallocator, ElQ{};
BranchLeaves DAT_011f8c80;
void FUN_00fdc5f0(){}
