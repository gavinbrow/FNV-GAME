struct AnimInfo { unsigned int count; int type; MyPosKey* keys; };
static __forceinline AnimInfo GetAnim(const MyPosData* data)
{ AnimInfo info; info.count=data->m_uiNumKeys; info.type=data->unk10; info.keys=data->m_pkKeys; return info; }
class NiStream { public: NiObj2* FUN_00a63430(); };
typedef float (*CurvatureFunction)(MyPosKey*, unsigned int);
extern CurvatureFunction DAT_011f3d38[];
struct PathInterpLink : public NiPathInterp
{
    unsigned short GetField(unsigned short mask,unsigned short pos) const
    { return (m_uFlags & mask) >> pos; }
    bool GetConstVelocity() const { return (GetField(0x10,4) & 1)!=0; }
    bool GetCVDataNeedsUpdate() const { return GetBit(1); }
    void SetCVDataNeedsUpdate(bool x) { SetBit(x,1); }
    void FUN_00a95ca0(NiStream&);
    float FUN_00a3e9a0();
    void FUN_00a3ee80(NiStream&);
};
void PathInterpLink::FUN_00a3ee80(NiStream& stream)
{
    FUN_00a95ca0(stream);
    m_spPathData=(NiPosData*)stream.FUN_00a63430();
    m_spPctData=(NiPosData*)stream.FUN_00a63430();
    SetCVDataNeedsUpdate(true);
    if(GetConstVelocity() && GetCVDataNeedsUpdate())
    { m_fTotalLength=FUN_00a3e9a0(); SetCVDataNeedsUpdate(false); }
    if(m_spPathData)
    {
        AnimInfo info=GetAnim((MyPosData*)(NiPosData*)m_spPathData);
        unsigned int count=info.count;
        int type=info.type;
        MyPosKey* keys=info.keys;
        if(count > 0)
        {
            CurvatureFunction curvature = DAT_011f3d38[type];
            *(float*)&unk34 = curvature(keys,count);
        }
    }
}