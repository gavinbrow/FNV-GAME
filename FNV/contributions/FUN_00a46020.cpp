
struct OutputWriter {
    int reserved00;
    int writtenBytes;
    int (__cdecl* writeCallback)(OutputWriter*, void*, unsigned int, unsigned int*, unsigned int);
    int Write(void* bytes, unsigned int count) {
        unsigned int written = count;
        int result = writeCallback(this, bytes, count, &written, 1);
        writtenBytes += result;
        return result;
    }
};
struct MyStreamWriter : MyStream {
    void FUN_00a645b0();
    OutputWriter* Output() {
        return *reinterpret_cast<OutputWriter**>(&_004[0x248]);
    }
};
struct MyUVController : MyCtrl {
    void FUN_00a6d5e0(MyStreamWriter* stream);
    void FUN_00a46020(MyStreamWriter* stream);
};

void MyUVController::FUN_00a46020(MyStreamWriter* stream) {
    FUN_00a6d5e0(stream);
    stream->Output()->Write(&m_usTextureSet, sizeof(m_usTextureSet));
    stream->FUN_00a645b0();
}
