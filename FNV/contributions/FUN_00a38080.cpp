struct InterpolatorRegistry;
class NiStream {
public:
    unsigned int m_header0;
    unsigned int m_header4;
    unsigned short m_capacity;
    unsigned short m_used;
    unsigned short m_unusedC;
    unsigned short m_growth;
    void func_0x0096ad30(unsigned int required);
    void func_0x0096ae90(unsigned int index, const unsigned int* value);
    void AppendValue(const unsigned int& value) {
        unsigned int index = m_used;
        unsigned int capacity = m_capacity;
        if (index >= capacity)
            func_0x0096ad30(index + m_growth);
        func_0x0096ae90(index, &value);
    }
};
struct LinkedInterpolator {
    unsigned int m_first;
    unsigned int m_second;
    void* m_object;
};
extern "C" void* DAT_011f36fc;
extern "C" InterpolatorRegistry* DAT_011f36f4;
extern "C" InterpolatorRegistry* DAT_011f36f8;
extern "C" unsigned char DAT_011a83ff;
extern "C" char UNK_01096b68, UNK_01096b54, UNK_01096b40;
extern "C" char UNK_01096b2c, UNK_01096b1c, UNK_01096b08;
extern "C" char UNK_01096af4, UNK_01096adc, UNK_01096ac4;
extern "C" char UNK_01096ab4, UNK_01096aa4;
extern "C" char UNK_01095dbc, UNK_01096a98, UNK_01096a8c;
extern "C" char UNK_01096a78, UNK_01096a68;
extern "C" unsigned int __cdecl FUN_00a7d330(void*);
extern "C" unsigned int __cdecl FUN_00a7d410(const void*, unsigned int);
struct ViewerBool { bool flag; };
union ViewerValue { unsigned int value; ViewerBool boolean; };
extern "C" unsigned int __cdecl FUN_00a7d370(const void*, ViewerBool);
extern "C" unsigned int __cdecl FUN_00a7d4d0(const void*, int);
extern "C" unsigned int __cdecl FUN_00a7d550(const void*, float);
extern "C" unsigned int __cdecl FUN_00a7d5e0(const void*, void*);
struct InterpolatorRegistry { LinkedInterpolator* func_0x00a2e570(NiInterpolator*, unsigned int); };
class BlendSerializer : public NiBlendInterpolator {
public:
    void FUN_00a38080(NiStream* stream);
};
void BlendSerializer::FUN_00a38080(NiStream* stream) {
    this->NiInterpolator::GetViewerStrings((NiViewerStringsArray*)stream);
    unsigned int loopValue;
    {
    ViewerValue temp;
    temp.value = FUN_00a7d330(DAT_011f36fc); stream->AppendValue(temp.value);
    temp.value = FUN_00a7d410(&UNK_01096b68, this->m_ucArraySize); stream->AppendValue(temp.value);
    temp.value = FUN_00a7d410(&UNK_01096b54, DAT_011a83ff); stream->AppendValue(temp.value);
    temp.boolean.flag = (this->m_uFlags & 1) != 0;
    temp.value = FUN_00a7d370(&UNK_01096b40, temp.boolean); stream->AppendValue(temp.value);
    temp.value = FUN_00a7d550(&UNK_01096b2c, this->m_fWeightThreshold); stream->AppendValue(temp.value);
    temp.value = FUN_00a7d4d0(&UNK_01096b1c, this->m_cHighPriority); stream->AppendValue(temp.value);
    temp.value = FUN_00a7d4d0(&UNK_01096b08, this->m_cNextHighPriority); stream->AppendValue(temp.value);
    temp.value = FUN_00a7d550(&UNK_01096af4, this->m_fHighSumOfWeights); stream->AppendValue(temp.value);
    temp.value = FUN_00a7d550(&UNK_01096adc, this->m_fNextHighSumOfWeights); stream->AppendValue(temp.value);
    temp.boolean.flag = ((this->m_uFlags >> 1) & 1) != 0;
    temp.value = FUN_00a7d370(&UNK_01096ac4, temp.boolean); stream->AppendValue(temp.value);
    temp.value = FUN_00a7d410(&UNK_01096ab4, this->m_ucInterpCount); stream->AppendValue(temp.value);
    temp.value = FUN_00a7d410(&UNK_01096aa4, this->m_ucSingleIdx); stream->AppendValue(temp.value);
    }
    for (unsigned int index = 0; index < this->m_ucArraySize; ++index) {
        if (this->m_pkInterpArray[index].m_spInterpolator.m_pObject && DAT_011f36f4) {
            LinkedInterpolator* linked = DAT_011f36f4->func_0x00a2e570(this->m_pkInterpArray[index].m_spInterpolator.m_pObject, 1);
            if (!linked && DAT_011f36f8) {
 NiInterpolator* retryInterpolator = this->m_pkInterpArray[index].m_spInterpolator.m_pObject;
 linked = DAT_011f36f8->func_0x00a2e570(retryInterpolator, 1);
 }
            if (linked) {
                void* linkedObject = linked->m_object;
                loopValue = FUN_00a7d5e0(&UNK_01095dbc, linkedObject); stream->AppendValue(loopValue);
                loopValue = FUN_00a7d410(&UNK_01096a98, (unsigned char)this->m_pkInterpArray[index].m_cPriority); stream->AppendValue(loopValue);
                loopValue = FUN_00a7d550(&UNK_01096a8c, this->m_pkInterpArray[index].m_fWeight); stream->AppendValue(loopValue);
                loopValue = FUN_00a7d550(&UNK_01096a78, this->m_pkInterpArray[index].m_fNormalizedWeight); stream->AppendValue(loopValue);
                loopValue = FUN_00a7d550(&UNK_01096a68, this->m_pkInterpArray[index].m_fEaseSpinner); stream->AppendValue(loopValue);
                NiInterpolator* finalInterpolator = this->m_pkInterpArray[index].m_spInterpolator.m_pObject;
                finalInterpolator->GetViewerStrings((NiViewerStringsArray*)stream);
            }
        }
    }
}
