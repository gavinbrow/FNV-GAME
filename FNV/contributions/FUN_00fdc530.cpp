struct Free {void* p; inline ~Free(){ delete p; }};
namespace fnv_00b31c70 { struct ElQ : Free { void Tidy(); inline ~ElQ(){int scratch[7]; Tidy();} }; }
struct IndexSet : fnv_00b31c70::ElQ {};
IndexSet DAT_011f8c18;
void FUN_00fdc530(){}