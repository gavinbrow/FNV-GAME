// @fnv 0x00fdc4d0
namespace fnv_00b31c70 {
class ElQ {
public:
    void* buffer;
    void Tidy();
    ~ElQ() { delete static_cast<unsigned char*>(buffer); }
};
}
struct IndexSet : public fnv_00b31c70::ElQ {
    ~IndexSet() {
        int cleanup_frame[7];
        Tidy();
    }
};
IndexSet DAT_011f8c68;