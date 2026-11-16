extern "C" __declspec(dllimport) long __stdcall InterlockedIncrement(volatile long*);
extern "C" __declspec(dllimport) long __stdcall InterlockedDecrement(volatile long*);
struct ControllerPointerProxy { NiTimeController* m_pObject; void FUN_00a5f860(NiTimeController* replacement); void FUN_0045cec0(); };
struct ControllerLinkProxy { void FUN_00a67260(NiTimeController* replacement); };
struct ControllerOwner : NiObjectNET { void FUN_00a5c480(NiTimeController* controller); };
void ControllerOwner::FUN_00a5c480(NiTimeController* controller) {
 if (!controller || !m_spControllers) return;
 NiTimeController* current=m_spControllers;
 if (current==controller) {
  volatile long* refCount=reinterpret_cast<volatile long*>(&controller->m_uiRefCount);
  InterlockedIncrement(refCount);
  reinterpret_cast<ControllerPointerProxy*>(&m_spControllers)->FUN_00a5f860(controller->m_spNext);
  NiTimeController* following=controller->m_spNext;
  if (following) {
   if (InterlockedDecrement(reinterpret_cast<volatile long*>(&following->m_uiRefCount))==0) following->DeleteThis();
   controller->m_spNext=0;
  }
  if (InterlockedDecrement(refCount)==0) controller->DeleteThis();
  return;
 }
 NiTimeController* following=current->m_spNext;
 while (following && following!=controller) {
  current=following;
  following=following->m_spNext;
 }
 if (following) {
  ControllerPointerProxy retained={controller};
  InterlockedIncrement(reinterpret_cast<volatile long*>(&controller->m_uiRefCount));
  reinterpret_cast<ControllerLinkProxy*>(current)->FUN_00a67260(controller->m_spNext);
  NiTimeController* tail=controller->m_spNext;
  if (tail) {
   if (InterlockedDecrement(reinterpret_cast<volatile long*>(&tail->m_uiRefCount))==0) tail->DeleteThis();
   controller->m_spNext=0;
  }
  retained.FUN_0045cec0();
 }
}