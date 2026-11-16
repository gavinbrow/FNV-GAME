#include "h_74712c1d3c73.h"

struct MagicCaster;
struct MagicItem;
struct EffectItem;

struct ActiveEffectStandIn {
    void __thiscall FUN_0082ba60(MagicCaster*, MagicItem*, EffectItem*);
};

extern char DAT_01079e7c[];

struct FUN_0080cd30_Class {
    void* vft;
    void* __thiscall FUN_0080cd30(MagicCaster*, MagicItem*, EffectItem*);
};

void* __thiscall FUN_0080cd30_Class::FUN_0080cd30(
    MagicCaster* a,
    MagicItem* b,
    EffectItem* c)
{
    reinterpret_cast<ActiveEffectStandIn*>(this)->FUN_0082ba60(a, b, c);
    vft = DAT_01079e7c;
    return this;
}