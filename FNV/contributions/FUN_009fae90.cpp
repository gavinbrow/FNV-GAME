#include <windows.h>

struct Packet;
struct PacketCallbacks {
    void (__stdcall *onIdle)(Packet*);
    void (__stdcall *onStart)(Packet*);
};
struct Packet {
    PacketCallbacks* callbacks;
    CRITICAL_SECTION criticalSection;
    int unk1c, unk20, unk24, unk28, unk2c;
    int unk30, unk34, unk38, unk3c, unk40;
    int active, delayed;
};
struct Parent {
    virtual int Operation00();
    virtual int Operation04();
    virtual int Operation08();
    virtual int Operation0c();
    virtual int Operation10();
    virtual int Start();
};
class CriticalSectionGuard {
    CRITICAL_SECTION* section;
public:
    explicit CriticalSectionGuard(CRITICAL_SECTION* s) : section(s) {
        EnterCriticalSection(section);
    }
    ~CriticalSectionGuard() { LeaveCriticalSection(section); }
};
int __stdcall FUN_009fae90(Packet* packet) {
    CRITICAL_SECTION* section =
        reinterpret_cast<Parent*>(reinterpret_cast<char*>(packet) - 12)
        ? &packet->criticalSection : 0;
    CriticalSectionGuard guard(section);
    if (!packet->active) {
        packet->active = 1;
        if (packet->delayed) {
            packet->delayed = 0;
        } else {
            int result = reinterpret_cast<Parent*>(reinterpret_cast<char*>(packet) - 12)->Start();
            if (result < 0) {
                packet->active = 0;
                goto return_error;
            }
            packet->callbacks->onStart(packet);
            return 0;
        return_error:
            return result;
        }
    }
    return 0;
}
