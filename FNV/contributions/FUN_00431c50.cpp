struct ExtraCountShim : public ExtraCount {
    bool FUN_00431c50(BSExtraData* compare);
};
bool ExtraCountShim::FUN_00431c50(BSExtraData* compare)
{
    ExtraCount* other = dynamic_cast<ExtraCount*>(compare);
    if (other == 0)
        return true;
    if (BSExtraData::Compare(compare))
        return true;
    if (iCount != other->iCount)
        return true;
    return false;
}