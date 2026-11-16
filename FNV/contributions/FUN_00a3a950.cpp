

struct InterpolatorCaller {
    virtual void Slot0() = 0;
    virtual void Slot1() = 0;
    virtual void Slot2() = 0;
    virtual void Slot3() = 0;
    virtual void Slot4() = 0;
    virtual void Slot5() = 0;
    virtual void Slot6() = 0;
    virtual void Slot7() = 0;
    virtual void Slot8() = 0;
    virtual void Slot9() = 0;
    virtual void Slot10() = 0;
    virtual void Slot11() = 0;
    virtual void Slot12() = 0;
    virtual void Slot13() = 0;
    virtual void Slot14() = 0;
    virtual void Slot15() = 0;
    virtual void Slot16() = 0;
    virtual void Slot17() = 0;
    virtual void Slot18() = 0;
    virtual void Slot19() = 0;
    virtual void Slot20() = 0;
    virtual void Slot21() = 0;
    virtual void Slot22() = 0;
    virtual void Slot23() = 0;
    virtual void Slot24() = 0;
    virtual void Slot25() = 0;
    virtual void Slot26() = 0;
    virtual void Slot27() = 0;
    virtual void Slot28() = 0;
    virtual void Slot29() = 0;
    virtual void Slot30() = 0;
    virtual void Slot31() = 0;
    virtual void Slot32() = 0;
    virtual void Slot33() = 0;
    virtual void Slot34() = 0;
    virtual void Slot35() = 0;
    virtual void Slot36() = 0;
    virtual void Slot37() = 0;
    virtual void Slot38() = 0;
    virtual void Slot39() = 0;
    virtual void Slot40() = 0;
    virtual void Slot41() = 0;
    virtual void Slot42() = 0;
    virtual void Slot43() = 0;
    virtual void Slot44() = 0;
    virtual void Slot45() = 0;
    virtual void Slot46() = 0;
    virtual void Slot47() = 0;
    virtual void GetActiveTimeRange(float* minimum, float* maximum) = 0;
};

struct MorpherCaller {
    virtual void Slot0() = 0;
    virtual void Slot1() = 0;
    virtual void Slot2() = 0;
    virtual void Slot3() = 0;
    virtual void Slot4() = 0;
    virtual void Slot5() = 0;
    virtual void Slot6() = 0;
    virtual void Slot7() = 0;
    virtual void Slot8() = 0;
    virtual void Slot9() = 0;
    virtual void Slot10() = 0;
    virtual void Slot11() = 0;
    virtual void Slot12() = 0;
    virtual void Slot13() = 0;
    virtual void Slot14() = 0;
    virtual void Slot15() = 0;
    virtual void Slot16() = 0;
    virtual void Slot17() = 0;
    virtual void Slot18() = 0;
    virtual void Slot19() = 0;
    virtual void Slot20() = 0;
    virtual void Slot21() = 0;
    virtual void Slot22() = 0;
    virtual void Slot23() = 0;
    virtual void Slot24() = 0;
    virtual void Slot25() = 0;
    virtual void Slot26() = 0;
    virtual void Slot27() = 0;
    virtual void Slot28() = 0;
    virtual void Slot29() = 0;
    virtual void Slot30() = 0;
    virtual void Slot31() = 0;
    virtual void Slot32() = 0;
    virtual void Slot33() = 0;
    virtual void Slot34() = 0;
    virtual void Slot35() = 0;
    virtual void Slot36() = 0;
    virtual void Slot37() = 0;
    virtual void Slot38() = 0;
    virtual void Slot39() = 0;
    virtual void Slot40() = 0;
    virtual void Slot41() = 0;
    virtual void Slot42() = 0;
    virtual void Slot43() = 0;
    virtual void Slot44() = 0;
    virtual void Slot45() = 0;
    virtual void Slot46() = 0;
    virtual void Slot47() = 0;
    virtual void Slot48() = 0;
    virtual NiInterpolator* GetInterpolator(unsigned int index) = 0;
};

struct TimeFlags {
    unsigned char lowerBits : 5;
    unsigned char updateAllowed : 1;
    unsigned char upperBits : 2;
};
extern const float DAT_01096ce0;
extern const float DAT_01015f5c;

__forceinline unsigned char IsManaged(const NiTimeController* object) { return (object->m_uFlags >> 5) & 1; }
struct FUN_00a3a950_shell : NiGeomMorpherController {
    void FUN_00a3a950();
};

void FUN_00a3a950_shell::FUN_00a3a950()
{
    if (!IsManaged(this)) {
        NiMorphData* morphData = m_spMorphData.m_pObject;
        unsigned int numTargets = morphData ? morphData->m_uiNumTargets : 0;
        m_fLoKeyTime = DAT_01096ce0;
        m_fHiKeyTime = DAT_01015f5c;

        unsigned int index = 0;
        if (index < numTargets) {
            do {
            NiInterpolator* interpolator = reinterpret_cast<MorpherCaller*>(this)->GetInterpolator(index);
            if (interpolator) {
                float upper = DAT_01015f5c;
                float lower = DAT_01096ce0;
                reinterpret_cast<InterpolatorCaller*>(interpolator)->GetActiveTimeRange(&lower, &upper);
                if (lower < m_fLoKeyTime) {
                    m_fLoKeyTime = lower;
                }
                if (upper > m_fHiKeyTime) {
                    m_fHiKeyTime = upper;
                }
            }
                ++index;
            } while (index < numTargets);
        }
    }
}