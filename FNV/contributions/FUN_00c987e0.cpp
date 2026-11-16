struct __declspec(align(16)) FUN_00c987e0_Pose {
    hkVector4 translation;
    hkQuaternion rotation;
    hkVector4 scale;
    void FUN_00ce52e0(int a1);
};
struct FUN_00c98780_Obj {
    void FUN_00c98780(FUN_00c987e0_Pose* pose, int a2,int a3,int a4,int a5,int a6);
};
struct FUN_00c987e0_Cls {
    void FUN_00c987e0(int a1,int a2,int a3,int a4,int a5,int a6);
};
void FUN_00c987e0_Cls::FUN_00c987e0(int a1,int a2,int a3,int a4,int a5,int a6)
{
    FUN_00c987e0_Pose pose;
    pose.FUN_00ce52e0(a1);
    reinterpret_cast<FUN_00c98780_Obj*>(this)->FUN_00c98780(&pose,a2,a3,a4,a5,a6);
}