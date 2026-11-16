
struct hkArrayRaw { void** m_data; int m_size; int m_capacityAndFlags; };
struct hkVector4 {float x,y,z,w;};
struct hkMultiThreadCheck { unsigned int m_threadId; unsigned short m_markCount; unsigned short m_markBitStack; };
struct PendingOps { 
    void* m_vtbl; void* m_04; void* m_08; void* m_0c; 
    hkArrayRaw m_10; hkArrayRaw m_1c;
};
struct QueueNode { void* data; void* other; QueueNode* next; };
struct WorldSave {
    void* m_vtbl; unsigned short m_memSizeAndFlags; short m_referenceCount;
    void* m_simulation; unsigned int m_unknown0c;
    hkVector4 m_gravity;
    void* m_fixedIsland; void* m_fixedRigidBody;
    hkArrayRaw m_activeSimulationIslands;
    hkArrayRaw m_inactiveSimulationIslands;
    hkArrayRaw m_dirtySimulationIslands;
    void* m_maintenanceMgr; void* m_memoryWatchDog;
    unsigned char m_assertOnRunningOutOfSolverMemory;
    void* m_broadPhase; void* m_kdTreeManager;
    unsigned char m_autoUpdateTree;
    void* m_broadPhaseDispatcher; void* m_phantomBroadPhaseListener;
    void* m_entityEntityBroadPhaseListener; void* m_broadPhaseBorderListener;
    void* m_multithreadedSimulationJobData;
    void* m_collisionInput; void* m_collisionFilter; void* m_collisionDispatcher;
    void* m_convexListFilter; PendingOps* m_pendingOperations;
    int m_pendingOperationsCount; int m_pendingBodyOperationsCount;
    int m_criticalOperationsLockCount; int m_criticalOperationsLockCountForPhantoms;
    unsigned char m_blockExecutingPendingOperations; unsigned char m_criticalOperationsAllowed;
    QueueNode* m_pendingOperationQueues; int m_pendingOperationQueueCount;
    hkMultiThreadCheck m_multiThreadCheck;
    unsigned char m_processActionsInSingleThread;
    unsigned char m_allowIntegrationOfIslandsWithoutConstraintsInASeparateJob;
    unsigned int m_minDesiredIslandSize;
    void* m_modifyConstraintCriticalSection; int m_isLocked;
    void* m_islandDirtyListCriticalSection; void* m_propertyMasterLock;
    unsigned char m_wantSimulationIslands;
    float m_snapCollisionToConvexEdgeThreshold; float m_snapCollisionToConcaveEdgeThreshold;
    unsigned char m_enableToiWeldRejection; unsigned char m_wantDeactivation;
    unsigned char m_shouldActivateOnRigidBodyTransformChange;
    float m_deactivationReferenceDistance; float m_toiCollisionResponseRotateNormal;
    int m_maxSectorsPerCollideTask; unsigned char m_processToisMultithreaded;
    int m_maxEntriesPerToiCollideTask; int m_maxNumToiCollisionPairsSinglethreaded;
    int m_simulationType;
    float m_numToisTillAllowedPenetrationSimplifiedToi; float m_numToisTillAllowedPenetrationToi;
    float m_numToisTillAllowedPenetrationToiHigher; float m_numToisTillAllowedPenetrationToiForced;
    unsigned int m_lastEntityUid; unsigned int m_lastIslandUid; unsigned int m_lastConstraintUid;
    hkArrayRaw m_phantoms; hkArrayRaw m_actionListeners; hkArrayRaw m_entityListeners;
    hkArrayRaw m_phantomListeners; hkArrayRaw m_constraintListeners; hkArrayRaw m_worldDeletionListeners;
    hkArrayRaw m_islandActivationListeners; hkArrayRaw m_worldPostSimulationListeners;
    hkArrayRaw m_worldPostIntegrateListeners; hkArrayRaw m_worldPostCollideListeners;
    hkArrayRaw m_islandPostIntegrateListeners; hkArrayRaw m_islandPostCollideListeners;
    hkArrayRaw m_contactListeners; hkArrayRaw m_contactImpulseLimitBreachedListeners;
    void* m_violatedConstraintArray; void* m_broadPhaseBorder;
    void FUN_00c92db0(struct StreamWriter* writer, void* unused);
};
struct StreamWriter {
    virtual void slot00();
    virtual void slot04();
    virtual void slot08();
    virtual void WriteValue(char* name, void* value, int flags);
    virtual void slot10();
    virtual void WriteArray(int kind, char* name, void* array, int length, void* bounded);
    virtual void OpenBlock(char* name);
    virtual void CloseBlock();
    int m_unknown04;
    void* m_reference08;
    int m_unknown0c;
    unsigned char m_writeAll10;
    void FUN_00d06fb0(char* name, void* value, unsigned int length, int flags);
};
void* __cdecl FUN_00d06f80(void* array, unsigned int bytes);
extern char str_010c6700;
extern char str_0109c938;
extern char str_010c66f0;
extern char str_010c66e4;
extern char str_010c6084;
extern char str_010c66d8;
extern char str_010c41a4;
extern char str_010c66b8;
extern char str_010c6698;
extern char str_010c6684;
extern char str_010c6664;
extern char str_010c664c;
extern char str_010c6630;
extern char str_010c6624;
extern char str_010c6618;
extern char str_010c660c;
extern char str_010c6600;
extern char str_010c65f8;
extern char str_010c65e8;
extern char str_010c65d8;
extern char str_010c65c4;
extern char str_010c65bc;
extern char str_010c65b0;
extern char str_010c65a4;
extern char str_010c6598;
extern char str_010c6580;
extern char str_010c6578;
extern char str_010c6564;
extern char str_010c6558;
extern char str_010c654c;
extern char str_010c6540;
extern char str_010c6534;
extern char str_010c6524;
extern char str_010c6514;
extern char str_010c6504;
extern char str_010c64f4;
extern char str_010c64e4;
extern char str_010c64d4;
extern char str_010c64c8;
static __forceinline void SaveArray(StreamWriter* writer,hkArrayRaw& array,char* name,unsigned int stride) {
    if ((array.m_capacityAndFlags & 0x80000000u) == 0 || writer->m_writeAll10) {
        void* ptr = array.m_data;
         unsigned int capacity = (array.m_capacityAndFlags & 0x3fffffff);
         void* bounded = FUN_00d06f80(ptr, capacity * stride);
        writer->WriteArray(3, name, array.m_data, array.m_size * stride, bounded);
    }
}
static __forceinline void SaveBlob(StreamWriter* writer,char* name,void* address,unsigned int length) {
    writer->FUN_00d06fb0(name,address,length,0);
}

void WorldSave::FUN_00c92db0(StreamWriter* writer,void* unused) {
    writer->m_reference08 = m_collisionInput;
    SaveArray(writer, m_activeSimulationIslands, &str_010c6700, 4);
    for (int i = m_activeSimulationIslands.m_size - 1; i >= 0; --i) writer->WriteValue(&str_0109c938, m_activeSimulationIslands.m_data[i], 0);
    SaveArray(writer, m_inactiveSimulationIslands, &str_010c66f0, 4);
    for (int i = m_inactiveSimulationIslands.m_size - 1; i >= 0; --i) writer->WriteValue(&str_010c66e4, m_inactiveSimulationIslands.m_data[i], 0);
    writer->WriteValue(&str_010c6084, reinterpret_cast<void*>(m_fixedIsland), 0);
    SaveArray(writer, m_phantoms, &str_010c66d8, 4);
    for (int i = 0; i < m_phantoms.m_size; ++i) writer->WriteValue(&str_010c41a4, m_phantoms.m_data[i], 0);
    if (m_modifyConstraintCriticalSection) {    SaveBlob(writer,&str_010c66b8, reinterpret_cast<void*>(m_modifyConstraintCriticalSection), 0x18);}
    SaveBlob(writer,&str_010c6698, reinterpret_cast<void*>(m_islandDirtyListCriticalSection), 0x18);
    if (m_propertyMasterLock) {    SaveBlob(writer,&str_010c6684, reinterpret_cast<void*>(m_propertyMasterLock), 0x18);}
    SaveBlob(writer,&str_010c6664, reinterpret_cast<void*>(m_multithreadedSimulationJobData), 0x120);
    if (m_pendingOperationQueues) {
       QueueNode* position = m_pendingOperationQueues;
       do {
    SaveBlob(writer,&str_010c664c, reinterpret_cast<void*>(m_pendingOperationQueues), 0x10);
          if (m_pendingOperationQueues->data) {
              hkArrayRaw* batch = static_cast<hkArrayRaw*>(m_pendingOperationQueues->data);
    SaveArray(writer, (*batch), &str_010c6630, 20);
          }
          position = position->next;
       } while (position);
    }
    writer->OpenBlock(&str_010c6624);
    writer->WriteValue(&str_010c6618, reinterpret_cast<void*>(m_simulation), 0);
    SaveArray(writer, m_dirtySimulationIslands, &str_010c660c, 4);
    writer->WriteValue(&str_010c6600, reinterpret_cast<void*>(m_maintenanceMgr), 0);
    SaveBlob(writer,&str_010c65f8, reinterpret_cast<void*>(m_pendingOperations), 0x28);
    writer->OpenBlock(&str_010c65f8);
    SaveArray(writer, m_pendingOperations->m_10, &str_010c65e8, 20);
    SaveArray(writer, m_pendingOperations->m_1c, &str_010c65d8, 16);
    writer->CloseBlock();
    writer->WriteValue(&str_010c65c4, reinterpret_cast<void*>(m_broadPhaseBorder), 0);
    writer->OpenBlock(&str_010c65bc);
    writer->WriteValue(&str_010c65b0, reinterpret_cast<void*>(m_broadPhase), 0);
    SaveBlob(writer,&str_010c65a4, reinterpret_cast<void*>(m_broadPhaseDispatcher), 0x10c);
    SaveBlob(writer,&str_010c65a4, reinterpret_cast<void*>(m_entityEntityBroadPhaseListener), 0x10);
    SaveBlob(writer,&str_010c65a4, reinterpret_cast<void*>(m_phantomBroadPhaseListener), 0xc);
    SaveBlob(writer,&str_010c65a4, reinterpret_cast<void*>(m_broadPhaseBorderListener), 0xc);
    SaveBlob(writer,&str_010c6598, reinterpret_cast<void*>(m_collisionInput), 0x80);
    if (m_collisionInput) {
      SaveBlob(writer,&str_010c6580,*reinterpret_cast<void**>(reinterpret_cast<unsigned char*>(m_collisionInput)+0x70),0x10);
    }
    writer->WriteValue(&str_010c6578, reinterpret_cast<void*>(m_collisionFilter), 0);
    writer->WriteValue(&str_010c6564, reinterpret_cast<void*>(m_convexListFilter), 0);
    writer->WriteValue(&str_010c6558, reinterpret_cast<void*>(m_collisionDispatcher), 0);
    writer->CloseBlock(); writer->CloseBlock();
    writer->OpenBlock(&str_010c654c);
    SaveArray(writer, m_entityListeners, &str_010c6540, 4);
    SaveArray(writer, m_phantomListeners, &str_010c6534, 4);
    SaveArray(writer, m_constraintListeners, &str_010c6524, 4);
    SaveArray(writer, m_worldDeletionListeners, &str_010c6514, 4);
    SaveArray(writer, m_islandActivationListeners, &str_010c6504, 4);
    SaveArray(writer, m_worldPostSimulationListeners, &str_010c64f4, 4);
    SaveArray(writer, m_worldPostIntegrateListeners, &str_010c64e4, 4);
    SaveArray(writer, m_worldPostCollideListeners, &str_010c64d4, 4);
    SaveArray(writer, m_islandPostIntegrateListeners, &str_010c64e4, 4);
    SaveArray(writer, m_contactListeners, &str_010c64c8, 4);
    writer->CloseBlock();
    writer->m_reference08 = 0;
}