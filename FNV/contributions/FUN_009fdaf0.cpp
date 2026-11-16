struct Interface {
    virtual void __stdcall method0();
    virtual void __stdcall method1();
    virtual void __stdcall method2();
    virtual void __stdcall method3();
    virtual void __stdcall method4();
    virtual void __stdcall method5();
    virtual void __stdcall method6();
    virtual void __stdcall method7();
    virtual void __stdcall method8();
    virtual void __stdcall method9();
    virtual void __stdcall method10();
    virtual void __stdcall method11();
    virtual void __stdcall OnReady(int flags);
};
struct Worker {
    int __thiscall FUN_009fe570(int resource, Interface** result, int flags, int* originalFlags);
};
struct Device {
    int m_vft;
    int m_04;
    int m_08;
    int m_0c;
    int m_10;
    int m_14;
    int m_18;
    int m_1c;
    int m_20;
    int m_24;
    int m_28;
    int m_2c;
    int m_30;
    int m_34;
    int m_38;
    int m_3c;
    int m_40;
    int m_44;
    int m_48;
    int m_4c;
    int m_50;
    int m_54;
    int m_58;
    int m_5c;
    int m_60;
    int m_64;
    int m_68;
    int m_6c;
    int m_70;
    int m_74;
    int m_78;
    int m_7c;
    int m_80;
    int m_84;
    int m_88;
    int m_8c;
    int m_90;
    int m_94;
    int m_98;
    int m_9c;
    int m_a0;
    Worker* m_a4;
};
int __stdcall FUN_009fdaf0(Device* device, int resource, Interface** output, int flags)
{
    if (output == 0)
        return 0x80004003;
    Interface* result = 0;
    int status = device->m_a4->FUN_009fe570(resource, &result, flags, &flags);
    if (status >= 0)
        result->OnReady(flags);
    *output = result;
    return status;
}