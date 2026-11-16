
struct DepthSurfaceDescription {
    unsigned int format; unsigned int type; unsigned int usage; unsigned int pool;
    unsigned int multisampleType; unsigned int multisampleQuality;
    unsigned int width; unsigned int height;
};
struct AdditionalDepthDevice { void** vtable; };
typedef unsigned long (__stdcall *DepthAddRef)(void*);
typedef long (__stdcall *DepthAcquireSurface)(void*, void*, int, D3DSurface_e7d250**);
typedef long (__stdcall *DepthGetDescription)(void*, DepthSurfaceDescription*);
class AdditionalDepthData : public NiDX92DBufferDataStub {
public:
    AdditionalDepthDevice* device;
    AdditionalDepthData() throw() : device(0) {}
    virtual ~AdditionalDepthData() {}
};
extern char DAT_010ef028;
AdditionalDepthData* __cdecl FUN_00e7d390(
    AdditionalDepthDevice* device, void* surfaceSource, int, int,
    Ni2DBufferStub** buffer) {
    AdditionalDepthData* result = new AdditionalDepthData;
    result->device = device;
    DepthAddRef addRef = reinterpret_cast<DepthAddRef>(result->device->vtable[1]);
    addRef(result->device);
    long status = reinterpret_cast<DepthAcquireSurface>(result->device->vtable[18])(
        result->device, surfaceSource, 0, &result->m_pkSurface);
    if (status < 0) {
        FUN_00a29680(&DAT_010ef028, NiDX9ErrorString(status));
        result->m_pkSurface = 0;
    } else {
        DepthSurfaceDescription description;
        status = reinterpret_cast<DepthGetDescription>(
            reinterpret_cast<AdditionalDepthDevice*>(result->m_pkSurface)->vtable[12])(
                result->m_pkSurface, &description);
        if (status >= 0) {
            result->m_pkPixelFormat = FUN_00e7c500(description.format);
            if (*buffer == 0) *buffer = Ni2DBufferStub::Create(description.width, description.height, result);
            else (*buffer)->SetRendererData(result);
            result->m_pkBuffer = *buffer;
            return result;
        }
    }
    delete result;
    return 0;
}