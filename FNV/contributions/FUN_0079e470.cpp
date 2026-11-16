#include <stdio.h>
struct TeleportPathHelper {
    BSSimpleArray<TESObjectREFR*> references;
    BSSimpleArray<TESObjectCELL*> cells;
    NiPoint3 start, end;
    TeleportPathHelper();
    ~TeleportPathHelper();
};
struct QuestMarkerNode {
    TESObjectREFR*& GetItem();
    QuestMarkerNode* GetNext();
};
struct MarkerPlayer {
    QuestMarkerNode* FUN_005eb7e0();
    void FUN_00952d60(TESObjectREFR*, TeleportPathHelper*, int);
};
struct MarkerReference : TESObjectREFR {
    const char* GetFullName();
    TESWorldSpace* FUN_00575d70();
};
struct MarkerTile : Tile {
    float FUN_00a011b0(int);
    MarkerTile* FUN_00a03da0(const char*);
    void FUN_00a07530(int);
};
struct MarkerMenu : MapMenu {
    TESObjectREFR* FUN_0079f7e0(TESObjectREFR*,TeleportPathHelper*);
    NiPoint3 FUN_0079c380(NiPoint3,TESWorldSpace*);
    void FUN_0079e470();
};
int FUN_00404dc0(const char*,const char*);
void MarkerMenu::FUN_0079e470()
{
    QuestMarkerNode* p = ((MarkerPlayer*)g_thePlayer)->FUN_005eb7e0();
    MarkerTile* a;
    while (p) {
        MarkerReference* aMap = (MarkerReference*)p->GetItem();
        TeleportPathHelper aArea;
        if (iCurrentPage == 33)
            ((MarkerPlayer*)g_thePlayer)->FUN_00952d60(aMap,&aArea,1);
        MarkerReference* aFirst = iCurrentPage == 33 ? (MarkerReference*)FUN_0079f7e0(aMap,&aArea) : aMap;
        a = aFirst ? ((MarkerTile*)pMapTile)->FUN_00a03da0(aFirst->GetFullName()) : 0;
        if (a && a->GetString(0xfc4) && !FUN_00404dc0(aMap->GetFullName(),a->GetString(0xfc4))) {
            char markerName[64];
            sprintf(markerName,"%s Marker",aFirst ? aFirst->GetFullName() : 0);
            MarkerTile* aB = aFirst ? ((MarkerTile*)pMapTile)->FUN_00a03da0(markerName) : 0;
            NiPoint3 _point2 = *aFirst->GetPos();
            NiPoint3 _pos2 = _point2;
            if (iCurrentPage == 33) _pos2.y -= 1024.0;
            else _pos2.y -= 128.0;
            NiPoint3 aCollision;
            NiPoint3 aOffset;
            if (pAdjustNorthRotationCell)
                pAdjustNorthRotationCell->FUN_00555b10(_point2,_point2,true);
            aCollision = FUN_0079c380(_point2,aFirst->FUN_00575d70());
            aOffset = FUN_0079c380(_pos2,aFirst->FUN_00575d70());
            float _target = ((MarkerTile*)pMapTile)->FUN_00a011b0(0xfb1);
            float _scale = ((MarkerTile*)pMapTile)->FUN_00a011b0(0xfb0);
            _target *= aOffset.x;
            _scale *= aOffset.y;
            float fX7 = _target;
            float fY3 = _scale;
            a->Set(DAT_011da350,aOffset.x,true);
            a->Set(DAT_011da34c,aOffset.y,true);
            a->Set(0xfa1,fX7,true);
            a->Set(0xfa2,fY3,true);
            a->Set(0xfc4,aMap->GetFullName(),true);
            a->Set(0xfba,200.0f,true);
            a->Set(0xfaa,38);
            a->Set(0xfad,2.0f,true);
            a->Set(0xfa3,1);
            a->Set(0xfae,1);
            a->Set(0xfb7,2);
            a->Set(0xfb9,2);
            a->Set(0xfb0,60.0f,true);
            if (aB) {
                LBValue* aCreated = (LBValue*)a->GetValue(0xfa1);
                LBValue* aCacheObject = (LBValue*)a->GetValue(0xfa2);
                aCreated->FUN_00a09200();
                aCreated->FUN_00a09130(0x7d0,aB,0xfa1);
                aCreated->FUN_00a09410(0);
                aCacheObject->FUN_00a09200();
                aCacheObject->FUN_00a09130(0x7d0,aB,0xfa2);
                aCacheObject->FUN_00a09080(0x7d1,60.0f);
                aCacheObject->FUN_00a09410(0);
            }
            a->FUN_00a07530(0x3ff);
        }
        p = p->GetNext();
    }
}
