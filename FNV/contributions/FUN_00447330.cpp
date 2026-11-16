// Adapted from Worker2 (2026-10-23) by GPT-6.
struct FUN_00447300_shell : public ModelLoader {
    void* FUN_00447300(char*, char*, void*);
};
struct KFGlobal447330 {
    void* FUN_00600700(char*, int);
    void FUN_00600170(char*, void*, int);
};
extern KFGlobal447330* DAT_011cb6a0;
struct KFList447330 {
    ~KFList447330();
    bool _ref_008256d0();
    char** _ref_006815c0();
    void _ref_0063f7b0();
};
char* __cdecl FUN_0040ab30(char*, int);
int __cdecl strcpy_s(char*, unsigned int, const char*);
void __cdecl _Deallocate(void*);

struct FUN_00447330_shell : public ModelLoader {
    void* FUN_00447330(char* arg0, bool arg1, bool arg2, int arg3);
};

void* FUN_00447330_shell::FUN_00447330(char* arg0, bool arg1, bool arg2, int arg3)
{
    AutoMemHelper helper2(0x33, true, "D:\\_Fallout3\\Platforms\\Common\\Code\\Fallout Shared\\ModelLoader.cpp", 0x108e);
    void* retVal_2;
    char buf6[260];
    char* p;
    void* res3;
    if (DAT_011cb6a0 != 0 && DAT_011cb6a0->FUN_00600700(arg0, 0) != 0) {
        retVal_2 = 0;
        if (arg3 == 12) {
            int i5;
            for (i5 = 0; (unsigned int)i5 < 12; i5++) {
                if (retVal_2 != 0) {
                    ((FUN_00447850_shell*)this)->FUN_00447850(DAT_011cb6a0->FUN_00600700(arg0, i5), retVal_2);
                } else {
                    retVal_2 = ((FUN_00447850_shell*)this)->FUN_00447850(DAT_011cb6a0->FUN_00600700(arg0, i5), 0);
                }
            }
        } else if (arg3 != 0 && arg2) {
            retVal_2 = ((FUN_00447850_shell*)this)->FUN_00447850(DAT_011cb6a0->FUN_00600700(arg0, 0), 0);
            ((FUN_00447850_shell*)this)->FUN_00447850(DAT_011cb6a0->FUN_00600700(arg0, arg3), retVal_2);
        } else {
            retVal_2 = ((FUN_00447850_shell*)this)->FUN_00447850(DAT_011cb6a0->FUN_00600700(arg0, arg3), 0);
        }
        return retVal_2;
    }
    strcpy_s(buf6, 260, "Data\\Meshes\\");
    strcat_s(buf6, 260, arg0);
    p = FUN_0040ab30(buf6, '\\');
    if (p == 0) {
        return 0;
    }
    strcpy_s(p, 260 - (p - buf6), "\\*.KF");
    res3 = ((FUN_00447300_shell*)this)->FUN_00447300(buf6, arg0, 0);
    if (arg1 && BSStringLength(arg0)) {
        char buf3[260];
        char* pA;
        KFList447330* res4;
        strcpy_s(buf3, 260, arg0);
        pA = FUN_0040ab30(buf3, '\\');
        if (pA != 0) {
            *pA = 0;
            strcat_s(pA, 260 - (pA - buf3), "\\Locomotion\\");
            strcpy_s(p, 260 - (p - buf6), "\\Locomotion\\*.KF");
            if (res3 == 0) {
                res3 = ((FUN_00447300_shell*)this)->FUN_00447300(buf6, buf3, 0);
            } else {
                ((FUN_00447300_shell*)this)->FUN_00447300(buf6, buf3, res3);
            }
            strcat_s(pA, 260 - (pA - buf3), "Hurt\\");
            strcat_s(pA, 260 - (pA - buf3), "IdleAnims");
            strcpy_s(p, 260 - (p - buf6), "\\Locomotion\\Hurt\\*.KF");
            res4 = (KFList447330*)((FUN_00447300_shell*)this)->FUN_00447300(buf6, buf3, 0);
            if (res4 != 0) {
                DAT_011cb6a0->FUN_00600170(buf3, res4, 1);
                while (!res4->_ref_008256d0()) {
                    char* head = *res4->_ref_006815c0();
                    delete head;
                    res4->_ref_0063f7b0();
                }
                delete res4;
            }
        }
    }
    DAT_011cb6a0->FUN_00600170(arg0, res3, 0);
    return res3;
}
