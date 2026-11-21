// fallout_shared/bgsbodypart_decls.h: declares TESFileFormVersion, TESFile, TESForm, BGSExplosion, BGSDebris and more
#ifndef FNV_BGSBODYPART_DECLS_H
#define FNV_BGSBODYPART_DECLS_H


extern "C" void* _alloca(unsigned int);
#pragma intrinsic(_alloca)
int Warning(const char*, ...);
class TESFileFormVersion
{
  public:
    unsigned short GetFormVersion();
};
// TESFile definition and chunk methods come from the shared layout_support.h.
class TESFile;
class TESForm
{
  public:
    virtual ~TESForm();
    bool GetInitialized() const;
    TESFile* GetFile(int);
    static void RemapFormIDForFile(unsigned int&, TESFile*);
    static TESForm* GetFormByID(unsigned int);
};
class BGSExplosion : public TESForm
{
};
class BGSDebris : public TESForm
{
};
class BGSImpactDataSet : public TESForm
{
};
class TESObjectREFR;
class DialogueItem
{
  public:
    TESObjectREFR* SelectDefaultResponseList();
};
class BaseProcess;
class Actor
{
  public:
    BaseProcess* GetProcess();
};
class TESSound;
class TESEffectShader;
class EffectSetting
{
  public:
    TESSound* GetCastSound();
    TESEffectShader* GetEnchantEffectShader();
};
class Tile;
class InterfaceManager
{
  public:
    Tile* FUN_004fd400();
    void FUN_00500a20(Tile*);
};
#include "BGSBodyPart_native.h"
extern "C" NiPoint3 NiPoint3_ZERO;

class ModelLoader
{
  public:
    void ProcessModelRequest(TESModel*, int, QueuedFile*, bool, bool, bool, bool);
};
extern ModelLoader* g_modelLoader;



extern "C" void* memset(void*, int, unsigned int);


class Queueable18
{
  public:
    virtual void Slot0() = 0;
    virtual void Slot1() = 0;
    virtual void Slot2() = 0;
    virtual void Slot3() = 0;
    virtual void QueueResourceLoad(IO_TASK_PRIORITY, QueuedFile*) = 0;
};

#endif
