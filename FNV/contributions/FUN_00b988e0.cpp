struct EventHandler { void** vtable; };
struct UIService { void** vtable; };

extern "C" EventHandler* DAT_011ffe2c;
extern "C" unsigned int DAT_011ffe30;
extern "C" unsigned char DAT_011ad8ec;
extern "C" void* DAT_011f4748;

typedef void (__thiscall *NotifyEvent)(EventHandler*, unsigned int);
typedef void (__thiscall *FinishEvent)(EventHandler*);
typedef void (__stdcall *DispatchUI)(UIService*, unsigned int, unsigned int, unsigned int);

void __cdecl FUN_00b988e0()
{
    EventHandler* eventHandler = DAT_011ffe2c;
    if (eventHandler != 0) {
        NotifyEvent notify = (NotifyEvent)eventHandler->vtable[0x104 / 4];
        notify(eventHandler, DAT_011ffe30);

        if (DAT_011ad8ec == 0) {
            eventHandler = DAT_011ffe2c;
            FinishEvent finish = (FinishEvent)eventHandler->vtable[0x114 / 4];
            finish(eventHandler);
        }

        const unsigned int eventCode = DAT_011ffe30;
        if (eventCode == 0xfe || eventCode == 0x10b) {
            UIService* ui = *(UIService**)((char*)DAT_011f4748 + 0x288);
            DispatchUI send = (DispatchUI)ui->vtable[0x114 / 4];
            send(ui, 7, 8, 0);
        } else if (eventCode == 0x230) {
            UIService* ui = *(UIService**)((char*)DAT_011f4748 + 0x288);
            DispatchUI send = (DispatchUI)ui->vtable[0x114 / 4];
            send(ui, 2, 8, 0);
        }
    }
    DAT_011ffe2c = 0;
    DAT_011ffe30 = 0;
}