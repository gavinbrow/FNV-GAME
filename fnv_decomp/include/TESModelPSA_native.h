#ifndef FNV_EXPERIMENT_TESMODELPSA_H
#define FNV_EXPERIMENT_TESMODELPSA_H
#include "TESModel_native.h"
#pragma pack(push, 4)
class TESModelPSA : public TESModel
{
  public:
    TESModelPSA();

};
#pragma pack(pop)
FNV_STATIC_ASSERT(sizeof(TESModelPSA) == 24);
#endif
