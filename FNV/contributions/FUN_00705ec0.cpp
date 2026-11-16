class IMHelper { public: bool FUN_009373f0(); void FUN_007181d0(); };
class ValueHolder { public: void* FUN_0056c7f0(); };
class DatHolder { public: unsigned char* FUN_00408d60(); };
extern DatHolder DAT_011db620;
class SpawnedObject {
 public:
 SpawnedObject();
 SpawnedObject* Init();
 void Attach(ValueHolder* a);
 void Set(void* a);
 int unk00;
int unk04;
int unk08;
int unk0c;
int unk10;
int unk14;
int unk18;
int unk1c;
int unk20;
int unk24;
int unk28;
int unk2c;
int unk30;
int unk34;
int unk38;
int unk3c;
int unk40;
int unk44;
int unk48;
int unk4c;
int unk50;
int unk54;
int unk58;
int unk5c;
int unk60;
int unk64;
int unk68;
int unk6c;
int unk70;
int unk74;
int unk78;
int unk7c;
int unk80;
int unk84;
int unk88;
int unk8c;
int unk90;
int unk94;
int unk98;
int unk9c;
int unka0;
int unka4;
int unka8;
int unkac;
int unkb0;
int unkb4;
int unkb8;
int unkbc;
int unkc0;
int unkc4;
int unkc8;
int unkcc;
int unkd0;
int unkd4;
int unkd8;
int unkdc;
int unke0;
int unke4;
int unke8;
int unkec;
};
InterfaceManager* FUN_004b7210();
IMHelper* __stdcall Getter2(SpawnedObject* obj);
ValueHolder* FUN_00765b80(void* a);
void FUN_00a04200(int a);
bool FUN_00705ec0(void* arg)
{
  if (FUN_004b7210() != 0 && ((IMHelper*)FUN_004b7210())->FUN_009373f0()) {
    ValueHolder* v = FUN_00765b80(arg);
    if (*DAT_011db620.FUN_00408d60()) {
      FUN_00a04200(0);
      SpawnedObject* obj = new SpawnedObject();
      obj->Attach(v);
      obj->Set(v->FUN_0056c7f0());
      Getter2(obj)->FUN_007181d0();
    }
    return true;
  } else {
    return false;
  }
}