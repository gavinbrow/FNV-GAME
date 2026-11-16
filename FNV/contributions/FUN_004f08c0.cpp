class FUN_00483630 : public BaseFormComponent {
public:
    unsigned char cFormType;
    unsigned int iFormFlags;
    unsigned int iFormID;
    TESFile* firstSourceFile;
    BSSimpleList<TESFile*>* nextSourceFile;
    ~FUN_00483630();
};
class FUN_004f08c0 : public FUN_00483630 {
public:
    TESRegionDataList* pDataList;
    BSSimpleList<TESRegionPointList*>* pPointLists;
    TESWorldSpace* pWorldSpace;
    TESWeather* pCurrentWeather;
    float fLastWeatherUpdate;
    NiColor EmittanceColor;
    virtual ~FUN_004f08c0();
};

FUN_004f08c0::~FUN_004f08c0()
{
    if (pDataList != 0) {
        delete pDataList;
    }
    if (pPointLists != 0) {
        TESRegionPointList* pointList = pPointLists->GetItem();
        while (pointList != 0) {
            pPointLists->RemoveHead();
            delete pointList;
            pointList = pPointLists->GetItem();
        }
        delete pPointLists;
    }
}