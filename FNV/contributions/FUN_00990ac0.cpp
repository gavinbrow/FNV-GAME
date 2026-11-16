struct NiPoint4 { float x,y,z,w; };
struct CombatGroupMember { int FUN_00575650(NiPoint4*,float,int); };
extern const float DAT_01050b98;
struct CombatGroupMethods {int FUN_0098a340(unsigned); CombatGroupMember* FUN_00903600(unsigned); int FUN_00989700(int);};
struct CombatGroupStrategy { bool FUN_00990ac0(CombatGroup*);};
bool CombatGroupStrategy::FUN_00990ac0(CombatGroup* group) {
bool bFound=false;
unsigned count=group->GetCount();
for(unsigned index=0;index<count;++index) {
if(((CombatGroupMethods*)group)->FUN_0098a340(index)==1) {
CombatGroupMember* pData=((CombatGroupMethods*)group)->FUN_00903600(index);
NiPoint4 position;
if(((CombatGroupMethods*)group)->FUN_00989700(pData->FUN_00575650(&position,DAT_01050b98,0))) group->FUN_0098a390(index,0);
else bFound=true;
}}
if(!bFound)return false;return true;
}