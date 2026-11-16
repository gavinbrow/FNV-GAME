#include "h_74712c1d3c73.h"

extern int DAT_011fdff8;
extern int DAT_011fe000;

class FUN_00bd0cb0_base
{
public:
    virtual void v00(int) = 0;
    virtual void v01(int) = 0;
    virtual void v02(int) = 0;
    virtual void v03(int) = 0;
    virtual void v04(int) = 0;
    virtual void v05(int) = 0;
    virtual void v06(int) = 0;
    virtual void v07(int) = 0;
    virtual void v08(int) = 0;
    virtual void v09(int) = 0;
    virtual void v10(int) = 0;
    virtual void v11(int) = 0;
    virtual void v12(int) = 0;
    virtual void v13(int) = 0;
    virtual void v14(int) = 0;
    virtual void v15(int) = 0;
    virtual void v16(int) = 0;
    virtual void v17(int) = 0;
    virtual void v18(int) = 0;
    virtual void v19(int) = 0;
    virtual void v20(int) = 0;
    virtual void v21(int) = 0;
    virtual void v22(int) = 0;
    virtual void v23(int) = 0;
    virtual void v24(int) = 0;
    virtual void v25(int) = 0;
    virtual void v26(int) = 0;
    virtual void v27(int) = 0;
    virtual void v28(int) = 0;
    virtual void v29(int) = 0;
    virtual void v30(int) = 0;
    virtual void v31(int) = 0;
    virtual void v32(int) = 0;
    virtual void v33(int) = 0;
    virtual void v34(int) = 0;
    virtual void v35(int) = 0;
    virtual void v36(int) = 0;
    virtual void v37(int) = 0;
    virtual void v38(int) = 0;
    virtual void v39(int) = 0;
    virtual void v40(int) = 0;
    virtual void v41(int) = 0;
    virtual void v42(int) = 0;
    virtual void v43(int) = 0;
    virtual void v44(int) = 0;
    virtual void v45(int) = 0;
    virtual void v46(int) = 0;
    virtual void v47(int) = 0;
    virtual void v48(int) = 0;
    virtual void v49(int) = 0;
    virtual void v50(int) = 0;
    virtual void v51(int) = 0;
    virtual void v52(int) = 0;
    virtual void v53(int) = 0;
    virtual void v54(int) = 0;
    virtual void v55(int) = 0;
    virtual void v56(int) = 0;
    virtual void v57(int) = 0;
    virtual void v58(int) = 0;
    virtual void v59(int) = 0;
    virtual void v60(int) = 0;
    virtual void v61(int) = 0;
    virtual void v62(int) = 0;
    virtual void v63(int) = 0;
    virtual void v64(int) = 0;
    virtual void v65(int) = 0;
    virtual void v66(int) = 0;
    virtual void v67(int) = 0;
    virtual void v68(int) = 0;
    virtual void v69(int) = 0;
    virtual void v70(int) = 0;
    virtual void v71(int) = 0;
    virtual void v72(int) = 0;
    virtual void v73(int) = 0;
};

class FUN_00bd0cb0_class : public FUN_00bd0cb0_base
{
public:
    virtual void v74(int) = 0;
    void __thiscall FUN_00bd0cb0();
};

void __thiscall FUN_00bd0cb0_class::FUN_00bd0cb0()
{
    int* p = &DAT_011fdff8;
    int* end = &DAT_011fe000;

    do
    {
        this->v74(*p);
        ++p;
    }
    while ((long)p < (long)end);
}