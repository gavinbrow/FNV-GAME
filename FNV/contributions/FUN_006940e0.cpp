struct NavMeshAction {
    unsigned int descriptor;
    unsigned int userData;
    unsigned int triangleIndex;
    unsigned int action;
};
extern unsigned int DAT_01187020;
struct PathingService {
    virtual void UnknownVirtual_00();
    virtual void UnknownVirtual_01();
    virtual void UnknownVirtual_02();
    virtual void UnknownVirtual_03();
    virtual void UnknownVirtual_04();
    virtual void UnknownVirtual_05();
    virtual void UnknownVirtual_06();
    virtual void UnknownVirtual_07();
    virtual void UnknownVirtual_08();
    virtual void UnknownVirtual_09();
    virtual void UnknownVirtual_0a();
    virtual void UnknownVirtual_0b();
    virtual void UnknownVirtual_0c();
    virtual void UnknownVirtual_0d();
    virtual void UnknownVirtual_0e();
    virtual void UnknownVirtual_0f();
    virtual void UnknownVirtual_10();
    virtual void UnknownVirtual_11();
    virtual void UnknownVirtual_12();
    virtual void UnknownVirtual_13();
    virtual void UnknownVirtual_14();
    virtual void UnknownVirtual_15();
    virtual void UnknownVirtual_16();
    virtual void UnknownVirtual_17();
    virtual void UnknownVirtual_18();
    virtual void UnknownVirtual_19();
    virtual void UnknownVirtual_1a();
    virtual void UnknownVirtual_1b();
    virtual void UnknownVirtual_1c();
    virtual void UnknownVirtual_1d();
    virtual void UnknownVirtual_1e();
    virtual void UnknownVirtual_1f();
    virtual void UnknownVirtual_20();
    virtual void UnknownVirtual_21();
    virtual void UnknownVirtual_22();
    virtual void UnknownVirtual_23();
    virtual void UnknownVirtual_24();
    virtual void UnknownVirtual_25();
    virtual void UnknownVirtual_26();
    virtual void UnknownVirtual_27();
    virtual void UnknownVirtual_28();
    virtual void UnknownVirtual_29();
    virtual void UnknownVirtual_2a();
    virtual void UnknownVirtual_2b();
    virtual void UnknownVirtual_2c();
    virtual void UnknownVirtual_2d();
    virtual void UnknownVirtual_2e();
    virtual void UnknownVirtual_2f();
    virtual void UnknownVirtual_30();
    virtual void UnknownVirtual_31();
    virtual void UnknownVirtual_32();
    virtual void UnknownVirtual_33();
    virtual void UnknownVirtual_34();
    virtual void UnknownVirtual_35();
    virtual void UnknownVirtual_36();
    virtual void UnknownVirtual_37();
    virtual void UnknownVirtual_38();
    virtual void UnknownVirtual_39();
    virtual void UnknownVirtual_3a();
    virtual void UnknownVirtual_3b();
    virtual void UnknownVirtual_3c();
    virtual void UnknownVirtual_3d();
    virtual void UnknownVirtual_3e();
    virtual void UnknownVirtual_3f();
    virtual void UnknownVirtual_40();
    virtual void UnknownVirtual_41();
    virtual void UnknownVirtual_42();
    virtual void UnknownVirtual_43();
    virtual unsigned char DispatchAction(NavMeshAction* action, unsigned char enabled, unsigned char option);
    unsigned char FUN_00485be0(unsigned int triangleIndex);
};
struct NavMeshActionController {
    PathingService* FUN_0059bb30();
    unsigned char FUN_006940e0(NavMeshAction* entry, unsigned char enabled, unsigned char option);
};
unsigned char NavMeshActionController::FUN_006940e0(NavMeshAction* entry, unsigned char enabled, unsigned char option)
{
    unsigned char result = 0;
    if (entry != 0 && entry->descriptor == DAT_01187020) {
        PathingService* service = FUN_0059bb30();
        switch (entry->action) {
        case 6:
            if (enabled == 0) {
                result = 0;
                break;
            }
        case 8:
        case 9:
        {
            unsigned char valid = 0;
            if (service->FUN_00485be0(entry->triangleIndex))
                valid = 1;
            if (valid) {
                switch (entry->action) {
                case 8:
                    result = 0;
                    break;
                default:
                    result = 1;
                    break;
                }
            }
            break;
        }
        default:
            if (enabled)
                result = service->DispatchAction(entry, enabled, option);
            break;
        }
    }
    return result;
}
