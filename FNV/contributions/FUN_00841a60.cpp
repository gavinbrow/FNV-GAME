struct ReconstructCellBlock {virtual ~ReconstructCellBlock();};
struct FUN_00841a60 : FUN_008448e0 {
 virtual ~FUN_00841a60(); void* FUN_004b9ba0();
 void FUN_006b7f20(void**, unsigned int*, ReconstructCellBlock**);
};
FUN_00841a60::~FUN_00841a60() {
 void* position=FUN_004b9ba0();
 while(position) {
 unsigned int key=0;
 ReconstructCellBlock* pEntry=0;
 FUN_006b7f20(&position,&key,&pEntry);
 delete pEntry;
 }
}