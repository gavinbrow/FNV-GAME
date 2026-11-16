struct SaveDataWriter {
    void FUN_008579b0(void* data, unsigned int size);
};
extern SaveDataWriter* DAT_011de45c;

struct SeenSectionDispatcher {
    virtual void Release();
    virtual void LoadGame();
    virtual void GetSaveSize();
    virtual void SaveGame();
    virtual void FUN_0087a330(bool abRecursing);
};

struct FUN_0087a330_shell : SeenData {
    char cSectionX;
    char cSectionY;
    unsigned short layoutPadding26;
    FUN_0087a330_shell* pNextSection;

    void FUN_0087a060(bool abRecursing);
    void FUN_0087a330(bool abRecursing);
};

void FUN_0087a330_shell::FUN_0087a330(bool abRecursing)
{
    FUN_0087a330_shell* pSection;
    FUN_0087a060(false);
    if (!abRecursing) {
        unsigned short numSections;
        numSections = 1;
        pSection = this;
        while ((pSection = pSection->pNextSection) != 0) {
            ++numSections;
        }
        DAT_011de45c->FUN_008579b0(&numSections, 2);
    }
    DAT_011de45c->FUN_008579b0(&cSectionX, 1);
    DAT_011de45c->FUN_008579b0(&cSectionY, 1);
    if (pNextSection) {
        reinterpret_cast<SeenSectionDispatcher*>(pNextSection)->FUN_0087a330(true);
    }
}