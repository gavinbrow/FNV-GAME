
struct BaseFormDC {
    int FUN_00401170();
    unsigned char FUN_005194d0();
};

struct ReferenceDC {
    unsigned char FUN_00440da0();
    unsigned char FUN_00440d80();
    BaseFormDC* FUN_007af430();
    int FUN_00568e50();
};

struct ReferenceNodeDC {
    ReferenceDC** FUN_006815c0();
    ReferenceNodeDC* FUN_00726070();
};

struct ReferenceCollectorDC {
    void FUN_005ae3d0(ReferenceDC**);
};

extern BaseFormDC* DAT_011ca258;

struct FUN_0054dcf0_shell : TESObjectCELL {
    void FUN_0054dcf0(ReferenceCollectorDC* collector);
};

void FUN_0054dcf0_shell::FUN_0054dcf0(ReferenceCollectorDC* collector)
{
    if (collector != 0) {
        CellRefLockEnter();
        ReferenceNodeDC* node = reinterpret_cast<ReferenceNodeDC*>(FUN_009604f0());
        while (node != 0) {
            ReferenceDC* reference = *node->FUN_006815c0();
            if (reference != 0) {
                if (!reference->FUN_00440da0()) {
                    if (!reference->FUN_00440d80()) {
                        BaseFormDC* baseForm = reference->FUN_007af430();
                        if (baseForm->FUN_00401170() == 0x1c && baseForm != DAT_011ca258) {
                            BaseFormDC* currentForm = reference->FUN_007af430();
                            if (reference->FUN_00568e50() || currentForm->FUN_005194d0()) {
                                collector->FUN_005ae3d0(&reference);
                            }
                        }
                    }
                }
            }
            node = node->FUN_00726070();
        }
        CellRefLockLeave();
    }
}