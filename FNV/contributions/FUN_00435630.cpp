class MultiBoundMarkerData {
public:
    bool FUN_00439060(MultiBoundMarkerData* other);
};

class FUN_00435630_shell : public ExtraMultiBoundData {
public:
    bool FUN_00435630(BSExtraData* apCompare);
};

bool FUN_00435630_shell::FUN_00435630(BSExtraData* apCompare)
{
    ExtraMultiBoundData* pOther = dynamic_cast<ExtraMultiBoundData*>(apCompare);
    if (pOther == 0)
        return true;
    if (pBound->FUN_00439060(pOther->pBound))
        return true;
    return false;
}