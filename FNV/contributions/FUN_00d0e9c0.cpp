// Baseline from the attributed contributor draft dated 2026-10-28.
// Current-claim official checking is required; no padding instructions are inserted.
struct S_00d0d150_Entity {
    int unk00; int unk04; int unk08; int unk0c;
    int unk10; int unk14; int unk18; int unk1c;
    int unk20; int unk24; int unk28; int unk2c;
    int unk30; int unk34; int unk38; int unk3c;
    int unk40; int unk44; int unk48; int unk4c;
    int unk50; int unk54; int unk58; int unk5c;
    int unk60; int unk64; int unk68; int unk6c;
    int unk70; int unk74; int unk78; int unk7c;
    int unk80; int unk84; int unk88; int unk8c;
    int unk90; int unk94; int unk98; int unk9c;
    int unka0; int unka4; int unka8; int unkac;
    int unkb0; int unkb4; int unkb8; int unkbc;
    int unkc0; int unkc4; int unkc8; int unkcc;
    int unkd0;
    unsigned int m_uid;
};

static __forceinline float& getSubStepTime(Context* ctx) {
    return reinterpret_cast<float&>(reinterpret_cast<Ctx*>(ctx)->unk0dc);
}

static __forceinline TimeStep& getContextTimeStep(Context* ctx) {
    return reinterpret_cast<TimeStep&>(reinterpret_cast<Ctx*>(ctx)->m_1d0);
}

static __forceinline void unlockContext(Context* ctx) {
    if (--ctx->depth() == 0 && !ctx->locked()) {
        if (ctx->pending())
            ctx->FUN_00c91120();
        if (ctx->mode() == 1 && ctx->otherPending())
            ctx->FUN_00c91140();
    }
}

struct S00d0e9c0_StepInfo {
    TimeStep s;
    __forceinline S00d0e9c0_StepInfo(float start, float end) {
        s.start = start;
        s.end = end;
        s.delta = end - start;
        s.inverse = (s.delta == 0.0f) ? 0.0f : (1.0f / s.delta);
    }
};

struct S00d0e9c0_DwordPair { int a, b; };

static __forceinline void memCpyOneAligned112(void* dst, const void* src) {
    for (int i = 0; i < 14; i++) {
        static_cast<S00d0e9c0_DwordPair*>(dst)[i] = static_cast<const S00d0e9c0_DwordPair*>(src)[i];
    }
}

static __forceinline void removeToiEventAt(S_00d0d150_Array<S_00d0d150_ToiEvent>& arr, int index) {
    arr.m_size--;
    if (arr.m_size != index) {
        memCpyOneAligned112(arr.m_data + index, arr.m_data + arr.m_size);
    }
}

struct S00d0e9c0_Key {
    unsigned int hi; unsigned int lo;
    __forceinline bool operator<(const S00d0e9c0_Key& o) const { return hi < o.hi || (hi == o.hi && lo < o.lo); }
};

struct S_00d0e9c0 {
    virtual void vfn0();
    virtual void vfn1();
    virtual void vfn2();
    virtual void vfn3();
    virtual void vfn4();
    virtual void vfn5();
    virtual void vfn6();
    virtual void vfn7();
    virtual void vfn8();
    virtual void vfn9();
    virtual void vfn10();
    virtual void vfn11();
    virtual void vfn12();
    virtual void vfn13();
    virtual void vfn14();
    virtual void vfn15();
    virtual void vfn16();
    virtual void vfn17(Context* ctx, S_00d0d150_ToiEvent* ev, float fStepTime, float fSubStepTime);

    int unk04;
    int unk08;
    Context* m_context;
    int unk10;
    float m_start;
    float m_end;
    float m_stepTime;
    int unk20;
    int unk24;
    int unk28;
    int unk2c;
    S_00d0d150_Array<S_00d0d150_ToiEvent> m_toiEvents;
    int unk3c;
    int unk40;
    int unk44;
    int unk48;
    int m_numSteps;

    int FUN_00d0e9c0(float arg1);
    hkBool FUN_00d0bc20(S_00d0d150_ToiEvent* ev, float* fSubStepTime);
    void FUN_00d0e210(Context* ctx, S_00d0d150_ToiEvent* ev, float fStepTime, float fSubStepTime);
};

int S_00d0e9c0::FUN_00d0e9c0(float minTime) {
    while (true) {
        struct Selection { union { int i; float end; } scan; float earliest; }; Selection sel;
        Context* ctx = this->m_context;
        ctx->depth()++;


        int bestIdx;
        float subStepTime;
        sel.earliest = minTime;
        subStepTime = getSubStepTime(this->m_context);
        bestIdx = -1;
        while (true) {
            for (sel.scan.i = 0; sel.scan.i < this->m_toiEvents.m_size; sel.scan.i++) {
                S_00d0d150_ToiEvent& cand = this->m_toiEvents.m_data[sel.scan.i];
                if (cand.m_time < sel.earliest) {
                    bestIdx = sel.scan.i;
                    sel.earliest = cand.m_time;
                } else if (cand.m_time == sel.earliest && bestIdx != -1) {
                    S_00d0d150_ToiEvent& best = this->m_toiEvents.m_data[bestIdx];
                    S00d0e9c0_Key candKey = { cand.m_entities[0]->m_uid, cand.m_entities[1]->m_uid };
                    S00d0e9c0_Key bestKey = { best.m_entities[0]->m_uid, best.m_entities[1]->m_uid };
                    if (candKey < bestKey) {
                        bestIdx = sel.scan.i;
                        sel.earliest = cand.m_time;
                    }
                }
            }

            if (0 > bestIdx) {
                unlockContext(ctx);
                return 0;
            }

            S_00d0d150_ToiEvent* pEvent = &this->m_toiEvents.m_data[bestIdx];
            if (this->FUN_00d0bc20(pEvent, &subStepTime)) {
                break;
            }
            removeToiEventAt(this->m_toiEvents, bestIdx);
            sel.earliest = minTime;
            subStepTime = getSubStepTime(this->m_context);
            bestIdx = -1;
        }

        S_00d0d150_ToiEvent event = this->m_toiEvents.m_data[bestIdx];
        removeToiEventAt(this->m_toiEvents, bestIdx);

        this->m_start = event.m_time;
        sel.scan.end = this->m_end;
        S00d0e9c0_StepInfo step(event.m_time, sel.scan.end);
        getContextTimeStep(this->m_context) = step.s;
        this->m_context->world()->time() = step.s;

        if (event.m_useSimpleHandling == 0) {
            this->vfn17(this->m_context, &event, this->m_stepTime, subStepTime);
        } else {
            this->FUN_00d0e210(this->m_context, &event, this->m_stepTime, subStepTime);
        }

        this->m_numSteps++;
        if (DAT_01269200 == 1) {
            unlockContext(ctx);
            return 3;
        }

        unlockContext(ctx);
    }
}
