
struct FUN_0042fb00 {
 int state;
 FUN_0042fb00();
 ~FUN_0042fb00();
};
struct Input_006dfb00 {
 unsigned char FUN_0069ad00(FUN_0042fb00*);
};
struct Owner_006dfb00 {
 int unk00,unk04,unk08,unk0c;
 Input_006dfb00* input;
 void FUN_006dfba0(FUN_0042fb00*);
 void FUN_006dfb00(Input_006dfb00*);
};
void Owner_006dfb00::FUN_006dfb00(Input_006dfb00* p) {
 input=p;
 FUN_0042fb00 local;
 if(!input->FUN_0069ad00(&local)) { input=0; return; }
 FUN_006dfba0(&local);
}
