struct NiAVObject { void FUN_00a64670(); NiAVObjectPalette *FUN_00a64620(); };
void __stdcall FUN_00a6d5e0(NiAVObject *);
struct SequenceNotifier { void *unk00; int m_uiPending; int (__cdecl *m_pfnNotify)(SequenceNotifier *, unsigned char *, int, int *, int); };
struct NiControllerManagerFacade : NiControllerManager { void FUN_00a2eaa0(NiAVObject *source); };
void NiControllerManagerFacade::FUN_00a2eaa0(NiAVObject *source) {
  FUN_00a6d5e0(source);
  SequenceNotifier *notifier = *reinterpret_cast<SequenceNotifier **>(reinterpret_cast<char *>(source) + 0x24c);
  { int isActive = 1; unsigned char firstOutput; notifier->m_uiPending += notifier->m_pfnNotify(notifier, &firstOutput, 1, &isActive, 1); m_bCumulative = firstOutput != 0; }
  source->FUN_00a64670();
  if (*reinterpret_cast<unsigned int *>(reinterpret_cast<char *>(source) + 0xd8) >= 0x0a010068u) {
    NiAVObjectPalette *replacement = source->FUN_00a64620();
    NiAVObjectPalette *old = m_spObjectPalette.m_pObject;
    if (old != replacement) {
      if (old && InterlockedDecrement(reinterpret_cast<volatile long *>(reinterpret_cast<char *>(old) + 4)) == 0)
        reinterpret_cast<NiRefObject *>(old)->DeleteThis();
      m_spObjectPalette.m_pObject = replacement;
      if (replacement)
        InterlockedIncrement(reinterpret_cast<volatile long *>(reinterpret_cast<char *>(replacement) + 4));
    }
  }
}