
struct Behavior;
struct Record{unsigned int unk00,unk04,unk08;Behavior* behavior;};
struct CountBlock{unsigned int unk0; unsigned int unk4; unsigned int unk8; unsigned int unkc; unsigned int unk10; unsigned int unk14; unsigned int unk18; int count;};
struct InputMap{unsigned int unk0; unsigned int unk4; unsigned int unk8; unsigned int unkc; unsigned int unk10; Record** records;unsigned int unk18,unk1c;int* indices;unsigned int unk24,unk28;CountBlock* counts;};
struct StateFlag{ bool enabled; StateFlag(bool value):enabled(value){} };
extern int DAT_01268370;
struct Behavior {
virtual void v0();virtual void v1();virtual void v2();virtual void v3();
virtual void v4();virtual void v5();virtual void v6();virtual void v7();
virtual int GetKind();
unsigned int unk4; unsigned int unk8; unsigned int unkc; unsigned int unk10; unsigned int unk14; unsigned int unk18; unsigned int unk1c; unsigned int unk20; unsigned int unk24; unsigned int unk28; unsigned int unk2c; unsigned int unk30; unsigned int unk34; unsigned int unk38; unsigned int unk3c; unsigned int unk40; unsigned int unk44; unsigned int unk48; unsigned int unk4c; unsigned int unk50; unsigned int unk54; unsigned int unk58; unsigned int unk5c; unsigned int unk60; unsigned int unk64; unsigned int unk68; unsigned int unk6c; unsigned int unk70; unsigned int unk74; unsigned int unk78; unsigned int unk7c; unsigned int unk80; unsigned int unk84; unsigned int unk88; unsigned int unk8c; unsigned int unk90; unsigned int unk94; unsigned int unk98; unsigned int unk9c; unsigned int unka0; unsigned int unka4; unsigned int unka8;
float valueAC;
Behavior* FUN_00cdf6c0();
void FUN_00cb8fe0(Record*,StateFlag);
void FUN_00cdf290(Record*,StateFlag);
void FUN_00cdf230(int*);
};
void __cdecl FUN_00c7a2d0(InputMap* input){
int count=input->counts->count;
for(int i=0;i<count;++i){
int index=input->indices[i]-1;
if(index<0)continue;
Record* item=input->records[index];
if(!item)continue;
Behavior* behavior=item->behavior;
if(behavior->GetKind()==13) behavior=behavior->FUN_00cdf6c0();
if(!behavior)continue;
switch(behavior->GetKind()){
case 2:behavior->FUN_00cb8fe0(item,true);behavior->valueAC=0.0f;break;
case 7:behavior->FUN_00cdf290(item,true);behavior->FUN_00cdf230(&DAT_01268370);break;
}
}
}
