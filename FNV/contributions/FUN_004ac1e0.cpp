struct BipedLoadAccess : BipedAnim {
 void FUN_004ac1e0(bool);
 void FUN_004af490(NiAVObject*, bool);
 void FUN_004ab750(TESObjectWEAP*, unsigned char);
};
struct ActorLoadAccess : Actor { void FUN_00571760(TESObjectWEAP*); bool FUN_008a16d0(); Animation* FUN_008b70d0(); };
struct PlayerLoadAccess : PlayerCharacter { BipedAnim* FUN_00950b00(bool); };
struct ItemLoadAccess : ItemChange { unsigned char FUN_004bd820(); bool FUN_004bd8d0(unsigned char,float&); };
struct WeapLoadAccess : TESObjectWEAP { bool FUN_004ad030(); };
struct FUN_004ab730_shell : TESForm { bool FUN_004ab730(); };
struct DataLoadAccess : NiGeometryData { void FUN_00a5d510(NiPointer<NiGeometryData>&); };
struct CloneLoadAccess : NiNode { NiObject* FUN_00a5d2c0(NiCloningProcess&); void FUN_00a5a040(); };
struct MatrixLoadAccess {
 float entry[3][3];
 MatrixLoadAccess(); void FUN_0043f850(float); MatrixLoadAccess operator*(const NiMatrix3&) const;
};
struct TESLoadAccess : TES { NiNode* FUN_00457ba0(NiNode*,NiCloningProcess&); };
struct ExtraLoadAccess : ExtraDataList { ExtraDismemberedLimbs* FUN_0042e8c0(); };
struct RefrLoadAccess : TESObjectREFR { ExtraLoadAccess* FUN_005d43c0(); };
struct NodeLoadAccess : NiNode { void FUN_00b4dec0(int); };
int __cdecl FUN_005b5e40(const char*,...);
void FUN_004b7660(NiNode*);
bool FUN_004b5bf0(NiAVObject*);
bool FUN_004abfa0();
void FUN_00709c20(TESModel*);
void FUN_004af240(NiNode*,NiNode*,BIPED_OBJECT,TESObjectREFR*);
int __cdecl FUN_00406f60(BSStringT<char>*,const char*,...);
void BipedLoadAccess::FUN_004ac1e0(bool force)
{
 bool hasHead = false;
 bool first = object[6].pParent;
 if (m_pRequester == g_thePlayer && g_thePlayer->Is1stPersonBiped(this)) hasHead = true;
 if (DAT_011c5cb4) FUN_006570e0(m_pRequester->GetObjectReference());
 for (int slot=0; slot<20; slot++) {
  if (object[slot].pPart && object[slot].pPart == bufferedObjects[slot].pPart && object[slot].pParent == bufferedObjects[slot].pParent && bufferedObjects[slot].pPartClone) {
   bool reload = false;
   object[slot] = bufferedObjects[slot];
   memset(&bufferedObjects[slot],0,sizeof(BIPOBJECT));
   if (DAT_011c5cb4 && object[slot].pPartClone) {
    NiNode* existing = object[slot].pPartClone->IsNode();
    if(existing) {
     for(unsigned int child=0;child<existing->FUN_0043b480();child++) FUN_004af490(existing->FUN_0043b4a0(child),false);
    } else FUN_004af490(object[slot].pPartClone,false);
   }
   if(slot==7 && object[5].pParent && ((FUN_004ab730_shell*)object[5].pParent)->FUN_004ab730() && object[slot].pPartClone) object[slot].pPartClone->FUN_00450f90(true);
   if(!reload) continue;
  } else {
   if(bufferedObjects[slot].pPartClone) FUN_004ab020(&bufferedObjects[slot],true,0);
   else memset(&bufferedObjects[slot],0,sizeof(BIPOBJECT));
  }
  bool mods=false;
  unsigned char modScope=0;
  if(slot==5 && object[slot].pParent) {
   if(m_pRequester == g_thePlayer) {
    TESObjectWEAP* weapon = (TESObjectWEAP*)object[slot].pParent;
    ItemLoadAccess* amount = (ItemLoadAccess*)g_thePlayer->GetProcess()->GetWeaponInfo();
    modScope = amount->FUN_004bd820();
    float info=0.0f;
    mods = amount->FUN_004bd8d0(14,info);
    FUN_004ab750(weapon,modScope);
    if(weapon->GetHasScope() && this==((PlayerLoadAccess*)g_thePlayer)->FUN_00950b00(false)) {
     if(!((WeapLoadAccess*)weapon)->FUN_004ad030() || mods) FUN_00709c20(weapon->FUN_00504e60());
    }
   } else ((ActorLoadAccess*)m_pRequester)->FUN_00571760((TESObjectWEAP*)object[slot].pParent);
   continue;
  }
  if(object[slot].pPart && object[slot].pPart != (TESModel*)-1) {
   if(hasHead) { switch(slot) { case 2: case 3: case 4: case 5: case 6: break; default: continue; } }
   if(!force && IsFaceGenObject((BIPED_OBJECT)slot) && m_pRequester != g_thePlayer && DAT_011c5ef0.Bool()->b && FUN_0043faf0() && FUN_004abfa0()) {
    FUN_004aede0(TASK_DEFAULT,0,(BIPED_OBJECT)slot); continue;
   }
   if(!object[slot].pPart->GetModelLength()) continue;
   int node=DAT_01188be8[slot];
   NiAVObject* result;
   NiNode* _clone = g_modelLoader->LoadFile(object[slot].pPart->GetModel(),3,true,false,IsFaceGenObject((BIPED_OBJECT)slot),false);
   NiCloningProcess boneIndex(1.0f);
   NiPointer<NiNode> copy(0);
   NiObject* model;
   if(FUN_004b5bf0(_clone)) {
    copy = ((TESLoadAccess*)g_TES)->FUN_00457ba0(_clone,boneIndex);
    model=copy;
   } else model=((CloneLoadAccess*)_clone)->FUN_00a5d2c0(boneIndex);
   NiNode* boneIndexd=model->IsNode();
   result=0;
   if(boneIndexd) {
    TESModelTextureSwap* fade=object[slot].pPart ? object[slot].pPart->GetAsModelTextureSwap() : 0;
    if(fade) fade->SwapTextures(boneIndexd);
    if(object[slot].pParent && object[slot].pParent->Unk_2B()) FUN_004b7660(boneIndexd);
    BSFadeNode* swap=boneIndexd->IsFadeNode();
    if(swap) ((NodeLoadAccess*)swap)->FUN_00b4dec0(7);
    boneIndexd->FUN_00440460(NiPoint3::ZERO);
    boneIndexd->FUN_0043fa80(DAT_011a9448);
    result=ApplySkinnedObjects(boneIndexd,(BIPED_OBJECT)slot,hasHead,first,0);
    if(!result) {
     result=boneIndexd;
     if(this && IsFaceGenObject((BIPED_OBJECT)slot)) {
      BSFaceGenModel* face=LoadFaceGenModel((BIPED_OBJECT)slot);
      if(face) {
       for(unsigned int index=0;index<boneIndexd->FUN_0043b480();index++) {
        NiAVObject* childNode=boneIndexd->FUN_0043b4a0(index);
        NiTriBasedGeom* geometry=childNode->IsTriBasedGeom();
        if(childNode && !geometry) FUN_005b5e40("FaceGen NIF contains non-geometry at root: '%s'",object[slot].pPart->GetModel());
        if(geometry && geometry->FUN_005495f0() && m_pRequester && m_pRequester->GetObjectReference() && m_pRequester->GetObjectReference()->GetFormType()==FORM_NPC) {
         TESNPC* newData=(TESNPC*)m_pRequester->GetObjectReference();
         FaceGenCoord coords[4];
         NiPointer<NiGeometryData> data(0);
         NiPointer<NiGeometryData> npc(0);
         ((DataLoadAccess*)geometry->FUN_005495f0())->FUN_00a5d510(data);
         npc=(NiGeometryData*)data;
         geometry->SetModelData(npc);
         newData->GetFaceCoord(coords);
         if(!FUN_0043faf0() || face->ApplyCoordinateToExistingMesh(&coords,geometry,false)) {
          NiMatrix3 rotation;
          rotation.MakeYRotation(-1.57079637f);
          geometry->FUN_0043fa80(geometry->FUN_006a9540() * rotation);
         }
        }
       }
      }
     }
     AttachToParent(root,boneIndexd,0,this,(BIPED_OBJECT)slot,0);
     if(!g_TESSaveLoadGame->GetLoading() && slot==5) {
      ActorLoadAccess* actor=(ActorLoadAccess*)m_pRequester;
      if(actor->GetProcess()) {
       if(m_pRequester==g_thePlayer && this==((PlayerLoadAccess*)g_thePlayer)->FUN_00950b00(true)) actor->GetProcess()->UpdateWeaponDrawn(actor->FUN_008a16d0(),this,g_thePlayer->GetAnimation(true),actor);
       else actor->GetProcess()->UpdateWeaponDrawn(actor->FUN_008a16d0(),this,actor->FUN_008b70d0(),actor);
      }
     }
    }
   }
   if(result) {
    BSStringT<char> name;
    FUN_00406f60(&name,"%s %s (%08X)",DAT_01188b98[slot],object[slot].pParent->GetEditorID(),object[slot].pParent->GetFormID());
    result->SetName(NiFixedString(name));
    FUN_004af240(_clone,boneIndexd,(BIPED_OBJECT)slot,m_pRequester);
    if(!object[slot].bSkinned && result->IsNode()) {
     NiNode* parent=result->GetParent();
     if(node==-1) {
      FUN_005b5e40("MODELS: The biped part '%s' should be skinned for '%s'.",object[slot].pPart->GetModel(),m_pRequester->GetFullName());
      if(parent) parent->RemoveObject(result);
      else { NiPointer<NiAVObject> release(result); }
      result=0;
     } else {
      if(bone[node].pParent) bone[node].pParent->AddObject(result,true);
      else if(result->GetParent()) root->AddObject(result,true);
     }
    }
    ExtraDismemberedLimbs* limbs=((RefrLoadAccess*)m_pRequester)->FUN_005d43c0()->FUN_0042e8c0();
    if(limbs) {
     for(int limb=0;limb<15;limb++) if(limbs->FUN_004303e0(limb)) FUN_005e4730(limb,result);
    }
    if(slot==7 && object[5].pParent && ((FUN_004ab730_shell*)object[5].pParent)->FUN_004ab730() && result) result->FUN_00450f90(true);
    object[slot].pPartClone=result;
   }
  }
 }
 ((CloneLoadAccess*)m_pRequester->Get3DSimple())->FUN_00a5a040();
}
