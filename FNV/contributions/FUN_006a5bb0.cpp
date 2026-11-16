
struct WorldObject : public NiAVObject {
    virtual void DeleteThis();
    virtual void GetRTTI();
    virtual void AsNode();
    virtual void AsSwitchNode();
    virtual void AsFadeNode();
    virtual void AsMultiBoundNode();
    virtual void AsGeometry();
    virtual void AsTriStrips();
    virtual void AsTriShape();
    virtual void AsSegmentedTriShape();
    virtual void AsSubIndexTriShape();
    virtual void AsDynamicTriShape();
    virtual void AsNiGeometry();
    virtual void AsNiTriBasedGeom();
    virtual void AsNiTriShape();
    virtual void AsParticlesGeom();
    virtual void AsLinesGeom();
    virtual void AsCollisionObject();
    virtual void AsBlendCollisionObject();
    virtual void AsAttachmentCollisionObject();
    virtual void AsRigidBody();
    virtual void AsLimitedHingeConstraint();
    virtual void CreateClone();
    virtual void LoadBinary();
    virtual void LinkObject();
    virtual void RegisterStreamables();
    virtual void SaveBinary();
    virtual void IsEqual();
    virtual void ProcessClone();
    virtual void PostLinkObject();
    virtual void StreamCanSkip();
    virtual void GetStreamableRTTI();
    virtual void GetBlockAllocationSize();
    virtual void GetGroup();
    virtual void SetGroup();
    virtual void AsControllerManager();
    virtual void UpdateControllers();
    virtual void PerformOperation();
    virtual void AttachProperty();
    virtual void SetMaterialNeedsUpdate();
    virtual void SetDefaultMaterialNeedsUpdateFlag();
    virtual void GetObjectByName();
    virtual void SetSelectiveUpdateFlags();
    virtual void UpdateDownwardPass();
    virtual void UpdateSelectedDownwardPass();
    virtual void UpdateRigidDownwardPass();
    virtual void UpdateWorldBound();
    virtual void UpdateWorldData();
    virtual void UpdateTransformAndBounds();
    virtual void PreAttachUpdate();
    virtual void PostAttachUpdate();
    virtual void OnVisible();
    virtual void UpdateWorldTransform();
    virtual void UpdateEffects();
    virtual void CalculateWorldBound();
    virtual void PropagateControllers();
    virtual void GetWorldTransform();
    virtual void GetLocalTransform();
    virtual void AttachChild(WorldObject* child);
};
struct WorldPointer : public GO { WorldObject* object; WorldPointer(WorldObject* object = 0); ~WorldPointer(); };
struct QueryQueue { bool FUN_006c62d0(int key, WorldPointer* result); void FUN_00405430(int key); };
struct RenderTask { void FUN_006a5bb0(int key); };
void RenderTask::FUN_006a5bb0(int key) {
    WorldPointer child(0);
    if (reinterpret_cast<QueryQueue*>(reinterpret_cast<char*>(this)+0x200)->FUN_006c62d0(key,&child)) {
        reinterpret_cast<WorldObject*>(static_cast<unsigned int>(g_011d6e5c))->
            AttachChild(reinterpret_cast<WorldObject*>(static_cast<unsigned int>(child)));
        NiUpdateData updateData(0.0f,false,false);
        reinterpret_cast<NiAVObject*>(static_cast<unsigned int>(g_011d6e5c))->Update(updateData);
        reinterpret_cast<NiAVObject*>(static_cast<unsigned int>(g_011d6e5c))->UpdateProperties();
        reinterpret_cast<QueryQueue*>(reinterpret_cast<char*>(this)+0x200)->FUN_00405430(key);
    }
}
