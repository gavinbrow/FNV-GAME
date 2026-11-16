#include "h_eaec426a33d7.h"

extern NiPoint3 _NiPoint3_ZERO;

struct FUN_004da230_node : public NiNode {
    NiNode* FUN_0045bc00(unsigned int);
};

struct FUN_004da230_intermediate {
    virtual void vfn_0();
    virtual void vfn_1();
    virtual void vfn_2();
    virtual FUN_004da230_node* GetNode();
};

struct FUN_004da230_param {
    virtual void vfn_0();
    virtual void vfn_1();
    virtual void vfn_2();
    virtual void vfn_3();
    virtual void vfn_4();
    virtual void vfn_5();
    virtual void vfn_6();
    virtual void vfn_7();
    virtual void vfn_8();
    virtual void vfn_9();
    virtual void vfn_10();
    virtual void vfn_11();
    virtual void vfn_12();
    virtual void vfn_13();
    virtual void vfn_14();
    virtual void vfn_15();
    virtual void vfn_16();
    virtual void vfn_17();
    virtual void vfn_18();
    virtual void vfn_19();
    virtual void vfn_20();
    virtual void vfn_21();
    virtual void vfn_22();
    virtual void vfn_23();
    virtual void vfn_24();
    virtual void vfn_25();
    virtual void vfn_26();
    virtual void vfn_27();
    virtual void vfn_28();
    virtual void vfn_29();
    virtual void vfn_30();
    virtual void vfn_31();
    virtual void vfn_32();
    virtual void vfn_33();
    virtual void vfn_34();
    virtual void vfn_35();
    virtual void vfn_36();
    virtual void vfn_37();
    virtual void vfn_38();
    virtual void vfn_39();
    virtual void vfn_40();
    virtual void vfn_41();
    virtual void vfn_42();
    virtual void vfn_43();
    virtual void vfn_44();
    virtual void vfn_45();
    virtual void vfn_46();
    virtual void vfn_47();
    virtual void vfn_48();
    virtual void vfn_49();
    virtual void vfn_50();
    virtual void vfn_51();
    virtual void vfn_52();
    virtual void vfn_53();
    virtual void vfn_54();
    virtual void vfn_55();
    virtual void vfn_56();
    virtual void vfn_57();
    virtual void vfn_58();
    virtual void vfn_59();
    virtual void vfn_60();
    virtual void vfn_61();
    virtual void vfn_62();
    virtual void vfn_63();
    virtual bool IsReady();
    virtual void vfn_65();
    virtual void vfn_66();
    virtual void vfn_67();
    virtual void vfn_68();
    virtual void vfn_69();
    virtual void vfn_70();
    virtual void vfn_71();
    virtual void vfn_72();
    virtual void vfn_73();
    virtual void vfn_74();
    virtual void vfn_75();
    virtual void vfn_76();
    virtual void vfn_77();
    virtual void vfn_78();
    virtual void vfn_79();
    virtual void vfn_80();
    virtual void vfn_81();
    virtual void vfn_82();
    virtual void vfn_83();
    virtual void vfn_84();
    virtual void vfn_85();
    virtual void vfn_86();
    virtual void vfn_87();
    virtual void vfn_88();
    virtual void vfn_89();
    virtual void vfn_90();
    virtual void vfn_91();
    virtual void vfn_92();
    virtual void vfn_93();
    virtual void vfn_94();
    virtual void vfn_95();
    virtual void vfn_96();
    virtual void vfn_97();
    virtual void vfn_98();
    virtual void vfn_99();
    virtual void vfn_100();
    virtual void vfn_101();
    virtual void vfn_102();
    virtual void vfn_103();
    virtual void vfn_104();
    virtual void vfn_105();
    virtual void vfn_106();
    virtual void vfn_107();
    virtual void vfn_108();
    virtual void vfn_109();
    virtual void vfn_110();
    virtual void vfn_111();
    virtual void vfn_112();
    virtual void vfn_113();
    virtual void vfn_114();
    virtual void vfn_115();
    virtual FUN_004da230_intermediate* GetContainer();
};

struct FUN_004da230_shell {
    unsigned int unk00;
    unsigned int unk04;
    NiPoint3 position;
    void FUN_004da230(FUN_004da230_param* object);
};

void FUN_004da230_shell::FUN_004da230(FUN_004da230_param* object)
{
    if (reinterpret_cast<Call_439090&>(position) ==
        reinterpret_cast<Call_439090&>(_NiPoint3_ZERO))
    {
        FUN_004da230_intermediate* nodeArg;
        FUN_004da230_node* container;

        nodeArg = (object != 0 && object->IsReady())
            ? object->GetContainer() : 0;
        container = (nodeArg != 0) ? nodeArg->GetNode() : 0;

        if (container != 0)
        {
            NiNode* node = container->FUN_0045bc00(0);
            if (node != 0)
            {
                NiMatrix3 rotation;
                rotation.FUN_00a59540(position.x, position.y, position.z);
                node->FUN_0043fa80(&rotation);
                NiUpdateData update(0.0f, false, false);
                node->UpdateWorldData(update);
            }
        }
    }
}
