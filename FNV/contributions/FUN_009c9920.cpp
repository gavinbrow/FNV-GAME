
struct CameraShotExtra : BGSCameraShot {
    float __thiscall FUN_005081b0();
    bool __thiscall FUN_009c8600();
};
struct CameraDisplayManager {
    void __thiscall FUN_00950110(bool);
};
extern CameraDisplayManager* DAT_011dea3c;
extern unsigned char DAT_011f21d3;

struct FUN_009c9920_shell : VATS {
    bool __thiscall FUN_009c9920();
};
bool __thiscall FUN_009c9920_shell::FUN_009c9920() {
    BSSimpleList<BGSCameraShot*>* nextCamera = pCameraList;
    bool found = false;
    while (nextCamera && nextCamera->GetItem() != pCamera) {
        nextCamera = nextCamera->GetNext();
    }
    if (nextCamera) {
        nextCamera = nextCamera->GetNext();
    }
    if (nextCamera) {
        if (pCamera) {
            pCamera->SetCameraTarget();
            pCamera = 0;
        }
        pCamera = nextCamera->GetItem();
        if (pCamera && fCameraMinTimer < static_cast<CameraShotExtra*>(pCamera)->FUN_005081b0()) {
            fCameraMinTimer = static_cast<CameraShotExtra*>(pCamera)->FUN_005081b0();
        }
        if (pCamera && static_cast<CameraShotExtra*>(pCamera)->FUN_009c8600()) {
            DAT_011dea3c->FUN_00950110(true);
        } else {
            DAT_011f21d3 = 1;
        }
        found = true;
    } else if (!nextCamera && pCamera && !pCamera->FUN_0058d630()) {
        pCamera->SetCameraTarget();
        pCamera = 0;
    }
    return found;
}
