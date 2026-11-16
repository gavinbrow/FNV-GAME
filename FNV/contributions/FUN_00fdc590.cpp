struct Free {void* p; inline ~Free(){ delete p; }}
;namespace fnv_00b31c70 {struct ElQ:Free{void Tidy();inline ~ElQ(){int scratch[7];Tidy();}};}
struct BranchConfigList:fnv_00b31c70::ElQ {};
// @fnv 0x00fdc590
BranchConfigList DAT_011f8c50;
void FUN_00fdc590(){}