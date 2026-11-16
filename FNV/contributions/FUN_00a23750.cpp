typedef unsigned int DWORD;
struct DIPROPHEADER {
    DWORD dwSize;
    DWORD dwHeaderSize;
    DWORD dwObj;
    DWORD dwHow;
};
struct DIPROPDWORD {
    DIPROPHEADER diph;
    DWORD dwData;
};
struct InputDevice {
    virtual unsigned int __stdcall QueryInterface(void*, void**);
    virtual unsigned int __stdcall AddRef();
    virtual unsigned int __stdcall Release();
    virtual unsigned int __stdcall GetCapabilities(void*);
    virtual unsigned int __stdcall EnumObjects(void*,void*,DWORD);
    virtual unsigned int __stdcall GetProperty(const void*,DIPROPHEADER*);
    virtual unsigned int __stdcall SetProperty(const void*,const DIPROPHEADER*);
};
struct InputManager {
    int unk00;
    int unk04;
    int unk08;
    InputDevice* devices[1];
    void FUN_00a23750(int index, float value);
};
void InputManager::FUN_00a23750(int index, float value)
{
    InputDevice* device = devices[index];
    DIPROPDWORD property;
    property.diph.dwSize = sizeof(DIPROPDWORD);
    property.diph.dwHeaderSize = sizeof(DIPROPHEADER);
    property.diph.dwHow = 0;
    property.diph.dwObj = 0;
    property.dwData = (int)(value * 10000.0);
    device->SetProperty((const void*)5, &property.diph);
}