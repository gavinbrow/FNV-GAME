class BSSpinLock {
};
struct GlobalObject_0096a2d0 {
    void Lock(const char*);
};
struct BSSpinLockUnlock {
    void Unlock();
};
class ActorDeletionQueue {
public:
    void FUN_0096d470(MobileObject*, int);
};
struct Host096d450 {
    void FUN_0096d450(MobileObject*, int, bool, bool, bool);
};
enum PROCESS_TYPE { PROCESS_TYPE_Default = 0 };
struct BaseProcess {
    PROCESS_TYPE GetProcessLevel();
};
class Base_0092c950 {
public:
    virtual ~Base_0092c950();
    virtual void FUN_0092c950(Base_0092c950*);
    Base_0092c950();
private:
    int unk04;
    int unk08;
    int unk0C;
    int unk10;
    int unk14;
    int unk18;
    int unk1C;
    int unk20;
    int unk24;
    int unk28;
    int unk2C;
    int unk30;
    int unk34;
    int unk38;
    int unk3C;
    int unk40;
    int unk44;
    int unk48;
    int unk4C;
    int unk50;
    int unk54;
    int unk58;
    int unk5C;
    int unk60;
    int unk64;
    int unk68;
    int unk6C;
    int unk70;
    int unk74;
    int unk78;
    int unk7C;
    int unk80;
    int unk84;
    int unk88;
    int unk8C;
    int unk90;
    int unk94;
    int unk98;
    int unk9C;
    int unkA0;
    int unkA4;
    int unkA8;
    int unkAC;
    int unkB0;
};
extern BSSpinLock DAT_011f11a0;
extern ActorDeletionQueue DAT_011e0e80;
struct FUN_009c4b60_shell : public MobileObject {
    bool FUN_009c4b60();
};

bool FUN_009c4b60_shell::FUN_009c4b60() {
    ((GlobalObject_0096a2d0*)&DAT_011f11a0)->Lock(0);
    if (this->word68 != 0) {
        PROCESS_TYPE level = ((BaseProcess*)this->word68)->GetProcessLevel();
        DAT_011e0e80.FUN_0096d470(this, level);
    }
    Base_0092c950* newProcess = new Base_0092c950();
    newProcess->FUN_0092c950((Base_0092c950*)this->word68);
    delete (Base_0092c950*)this->word68;
    this->word68 = (unsigned int)newProcess;
    ((Host096d450*)&DAT_011e0e80)->FUN_0096d450(this, 3, 0, 0, 0);
    ((BSSpinLockUnlock*)&DAT_011f11a0)->Unlock();
    return true;
}



