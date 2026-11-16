#include <stdlib.h>
struct FUN_005c90d0 { ~FUN_005c90d0(); };
struct DialogueList;
struct FUN_0061b320_shell {
    DialogueItem* FUN_0061b320(TESObjectREFR*, TESObjectREFR*, TESTopic*, DialogueList*, bool);
};
struct FormTypeView { int FUN_00401170(); };
extern TESDataHandler* g_dataHandler;
unsigned int __cdecl FUN_0061b9d0(int);
struct DialogueList {
 DialogueItem*& FUN_006815c0();
 bool FUN_008256d0();
 void FUN_0063f7b0();
 unsigned int FUN_005ae380();
 DialogueList* FUN_00726070();
 void AddTail(DialogueItem*&);
};
struct TopicList {
 TESTopic*& FUN_006815c0();
 bool FUN_008256d0();
 unsigned int FUN_005ae380();
 TopicList* FUN_00726070();
};
struct ConversationDataView { TopicList* FUN_00413f40(); };
struct InfoView {
 bool FUN_00579200();
 void FUN_0061f170(bool,TESObjectREFR*);
 void FUN_0061f150();
 ConversationDataView* FUN_009e32d0();
 int FUN_0061b9f0();
};
struct ItemView {
 InfoView* FUN_0084e3a0();
 bool FUN_0083c7b0();
 ItemView* FUN_0083c820();
 BSStringT<char>* FUN_006815c0();
 TESForm* FUN_009611e0();
};
struct DataHandlerView { FUN_0061b320_shell* FUN_00461690(int); };
struct AIView {
 virtual void v00(); virtual void v01(); virtual void v02(); virtual void v03();
 virtual void v04(); virtual void v05(); virtual void v06(); virtual void v07();
 virtual void v08(); virtual void v09(); virtual void v10(); virtual void v11();
 virtual void v12(); virtual void v13(); virtual void v14(); virtual void v15();
 virtual void v16(); virtual void v17(); virtual void v18(); virtual void v19();
 virtual void v20(); virtual void v21(); virtual void v22(); virtual void v23();
 virtual void v24(); virtual void v25(); virtual int GetDisposition();
};
struct ActorBaseView : TESForm {
 int unk18; int unk1c; int unk20; int unk24; int unk28; int unk2c;
 AIView ai;
};
extern unsigned char DAT_011cbeac;
void __cdecl DebugLog(const char*,...);
void __cdecl FUN_00403d30(void*,int,unsigned int);
unsigned int __cdecl FUN_0061b440(TESObjectREFR* speaker,TESObjectREFR* listener,DialogueList* history,FUN_0061b320_shell* initialTopic)
{
 int used[500];
 DialogueItem* choice;
 bool item;
 if (!history) return 0;
 while(history && !history->FUN_008256d0()) {
  delete (FUN_005c90d0*)history->FUN_006815c0();
  history->FUN_0063f7b0();
 }
 if(!speaker || !listener) return 0;
 TESObjectREFR* previous=speaker;
 TESObjectREFR* currentSpeaker=listener;
 FUN_0061b320_shell* nextItem=0;
 TESTopic* currentListener=0;
 TESBoundObject* topic=previous->GetObjectReference();
 if(topic && ((FormTypeView*)topic)->FUN_00401170()==43 && !((ActorBaseView*)topic)->ai.GetDisposition()) return 0;
 nextItem=initialTopic;
 if(!nextItem) nextItem=((DataHandlerView*)g_dataHandler)->FUN_00461690(210);
 DialogueItem* base=0;
 int exhausted=-1;
 srand((unsigned int)FUN_0061b9d0(0));
 while(nextItem && history->FUN_005ae380()<100) {
  TopicList* topics;
  base=nextItem->FUN_0061b320(previous,currentSpeaker,currentListener,history,false);
  if(!base) {
   if(!initialTopic || ((InfoView*)initialTopic)->FUN_0061b9f0()==1) {
    nextItem=((DataHandlerView*)g_dataHandler)->FUN_00461690(212);
    base=nextItem->FUN_0061b320(previous,currentSpeaker,currentListener,history,false);
   }
   if(!base) break;
  }
  if(base && ((ItemView*)base)->FUN_0084e3a0() && ((ItemView*)base)->FUN_0084e3a0()->FUN_00579200()) {
   ((ItemView*)base)->FUN_0084e3a0()->FUN_0061f170(false,speaker);
   ((ItemView*)base)->FUN_0084e3a0()->FUN_0061f170(true,speaker);
   ((ItemView*)base)->FUN_0084e3a0()->FUN_0061f150();
  }
  history->AddTail(base);
  currentListener=(TESTopic*)nextItem;
  nextItem=0;
  choice=0;
  item=false;
  FUN_00403d30(used,0,2000);
  exhausted=-1;
  while(!choice && !item) {
   int count;
   if(((ItemView*)base)->FUN_0084e3a0() && ((ItemView*)base)->FUN_0084e3a0()->FUN_009e32d0()) {
    topics=((ItemView*)base)->FUN_0084e3a0()->FUN_009e32d0()->FUN_00413f40();
    count=topics->FUN_005ae380();
    if(count) {
     if(exhausted==-1) exhausted=rand()%count+1;
     else while(used[exhausted-1]) exhausted=rand()%count+1;
    }
    if(exhausted>0) used[exhausted-1]=1;
    int n=0;
    while(n<exhausted && topics && !topics->FUN_008256d0()) {
     nextItem=(FUN_0061b320_shell*)topics->FUN_006815c0();
     topics=topics->FUN_00726070();
     n++;
    }
    switch(((ItemView*)base)->FUN_0084e3a0()->FUN_0061b9f0()) {
     case 2: if(rand()%2!=0) break;
     case 0: {
      TESObjectREFR* temp=previous;
      previous=currentSpeaker;
      currentSpeaker=temp;
      break;
     }
    }
    item=true;
    for(unsigned int i=0;i<(unsigned int)count && item;i++) if(!used[i]) item=false;
    choice=nextItem->FUN_0061b320(previous,currentSpeaker,currentListener,history,false);
   } else item=true;
  }
 }
 if(DAT_011cbeac) {
  DebugLog("------NEW CONVERSATION CREATED---------------------");
  DialogueList* node=history;
  {
  int index=1;
  while(node && node->FUN_006815c0()) {
   ItemView* entry=(ItemView*)node->FUN_006815c0();
   node=node->FUN_00726070();
   if(entry) {
    if(entry->FUN_0083c7b0()) {
      DebugLog("Item %d: %s says '%s'",index,entry->FUN_009611e0()->GetName(),entry->FUN_0083c820()->FUN_006815c0()->String());
    } else {
      DebugLog("Item %d: %s has no response!",index,entry->FUN_009611e0()->GetName());
    }
   }
   index++;
  }
  }
 }
 return history->FUN_005ae380();
}
