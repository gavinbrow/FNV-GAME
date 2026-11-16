
struct NotificationProbe : NiAVObject { virtual void UpdateAttach(NiAVObject*, int); };
struct SkinDataProbe {
    unsigned int FUN_008041a0();
};
struct SkinInstanceProbe : NiSkinInstance {
    void FUN_00437730(NiAVObject*);
};
struct SceneNodeProbe : NiNode {
    NiAVObject* FUN_009611e0();
};
struct HandleVectorProbe {
    void FUN_004afc50(const NiPointer<NiAVObject>&);
};
extern bool __cdecl FUN_0043b300(const NiRTTI*, NiNode*);
extern const char* __cdecl FUN_0044a670(const char*);
extern int __cdecl FUN_00ec7ec0(const char*, const char*, const char*);
extern void __cdecl FUN_005b5e40(const char*, ...);
extern const char DAT_0101f8d8[];
extern const char DAT_0101f890[];
extern const char DAT_0101f840[];
extern const char DAT_0101f7c8[];

void __cdecl FUN_004ade40(NiNode* source, NiAVObject* object, NiAVObject* notify, bool report)
{
    if (!object)
        return;

    NiNode* node = object->IsNode();
    if (object->IsGeometry()) {
        NiSkinInstance* geometry;
        NiTriBasedGeom* skin = static_cast<NiTriBasedGeom*>(object);
        geometry = skin->FUN_0043fad0();
        if (geometry) {
            NiAVObject* boneCount;
            unsigned int replacement = reinterpret_cast<SkinDataProbe*>(geometry->GetData())->FUN_008041a0();
            NiAVObject** bones = geometry->GetBones();
            for (unsigned int i = 0; i < replacement; ++i) {
                if (bones[i]) {
                        boneCount = FUN_004ade00(source, bones[i]->GetName());
                    if (boneCount) {
                        geometry->FUN_004adda0(i, boneCount);
                    } else {
                        geometry->FUN_004adda0(i, source);
                        if (report) {
                            if (node && !FUN_00ec7ec0((const char*)object->GetName(),
                                (const char*)bones[i]->GetName(),
                                FUN_0044a670((const char*)bones[i]->GetName()))) {
                                FUN_005b5e40(DAT_0101f8d8,
                                    (const char*)bones[i]->GetName(),
                                    (const char*)static_cast<SceneNodeProbe*>(node)->FUN_009611e0()->GetName(),
                                    (const char*)node->GetName());
                            } else if (node && source) {
                                FUN_005b5e40(DAT_0101f890,
                                    (const char*)bones[i]->GetName(),
                                    (const char*)node->GetName(),
                                    (const char*)source->GetName());
                            } else {
                                FUN_005b5e40(DAT_0101f840,(const char*)bones[i]->GetName());
                            }
                        }
                    }
                }
            }
            if (notify) {
                reinterpret_cast<SkinInstanceProbe*>(geometry)->FUN_00437730(notify);
                static_cast<NotificationProbe*>(notify)->UpdateAttach(object, 1);
            }
        }
    }
    bool printed = false;
    if (node) {
        node->FUN_004add70();
        GlobalObject_004aff00 children(0,1);
        for (unsigned int j = 0; j < node->FUN_0043b480(); ++j) {
            NiAVObject* childNode = node->FUN_0043b4a0(j);
            NiNode* child = 0;
            if (childNode)
                child = childNode->IsNode();
            else
                continue;
            if (FUN_0043b300(&DAT_011f9140, node) && child) {
                FUN_004ade40(source,childNode,notify,true);
                continue;
            }
            if (!childNode->IsGeometry()) {
                if (!printed && child && reinterpret_cast<NiNode*>(childNode)->FUN_00453470()) {
                    FUN_005b5e40(DAT_0101f7c8,
                        (const char*)static_cast<SceneNodeProbe*>(node)->FUN_009611e0()->GetName(),
                        (const char*)node->GetName(),
                        (const char*)source->GetName());
                    printed=true;
                }
                {
                    NiPointer<NiAVObject> item(childNode);
                    reinterpret_cast<HandleVectorProbe*>(&children)->FUN_004afc50(item);
                }
                node->RemoveObject(childNode);
                continue;
            }
            FUN_004ade40(source,childNode,notify,report);
        }
        node->FUN_004add70();
    }
}
