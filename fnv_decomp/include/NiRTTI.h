#ifndef FNV_NIRTTI_CANONICAL_H
#define FNV_NIRTTI_CANONICAL_H

class NiRTTI
{
  public:
    NiRTTI(const char* pcName, const NiRTTI* pkBaseRTTI);

    const char* GetName() const;
    const NiRTTI* GetBaseRTTI() const;

  protected:
    const char* m_pcName;
    const NiRTTI* m_pBaseRTTI;
};

#endif
