
struct NiMatrix3_0068aa50 {
 float m00,m01,m02,m10,m11,m12,m20,m21,m22;
 void FUN_006815c0();
 void FUN_0043f850(float scale);
 NiMatrix3_0068aa50* FUN_0043f8d0(NiMatrix3_0068aa50*,const NiMatrix3_0068aa50*);
};
struct NavMeshChain_0068aa50 {
 NavMeshChain_0068aa50* FUN_00461130();
 void FUN_004b45b0();
};
struct NavMeshNode_0068aa50 {
 NavMeshChain_0068aa50* FUN_009611e0(NiMatrix3_0068aa50*);
 void FUN_0043fa80(NiMatrix3_0068aa50*);
};
struct NavMeshSearchList_0068aa50 {
 NavMeshNode_0068aa50** entries;
 unsigned int count;
 unsigned int capacity;
 unsigned int growStep;
 NavMeshSearchList_0068aa50(int initial, int growth);
 ~NavMeshSearchList_0068aa50();
 unsigned int FUN_00658930();
 NavMeshNode_0068aa50** FUN_00877a30(unsigned int);
};
extern float DAT_0102b3c8;
struct FUN_0068aa50_shell {
 void FUN_0068a8f0(void*,NavMeshSearchList_0068aa50*,unsigned int*);
 void FUN_0068aa50(void*);
};
void FUN_0068aa50_shell::FUN_0068aa50(void* searchArg) {
 NavMeshSearchList_0068aa50 items(10,1);
 {
 unsigned int found=0;
 FUN_0068a8f0(searchArg,&items,&found);
 for(unsigned int i=0;i<items.FUN_00658930();++i) {
   NavMeshNode_0068aa50* node=*items.FUN_00877a30(i);
   if(node){
     NiMatrix3_0068aa50 a;
     node->FUN_009611e0(&a)->FUN_00461130()->FUN_004b45b0();
     NiMatrix3_0068aa50 b;
     b.FUN_006815c0();
     b.FUN_0043f850(DAT_0102b3c8);
     NiMatrix3_0068aa50 c;
     node->FUN_0043fa80(a.FUN_0043f8d0(&c,&b));
   }
 }
 }
}
