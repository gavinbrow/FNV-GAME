template<class T>
static T& member_at(void* object, unsigned int offset) {
    return *reinterpret_cast<T*>(reinterpret_cast<unsigned char*>(object) + offset);
}

extern const double DAT_010290b0;

struct FUN_00c759f0_Class {
    void FUN_00c759f0();
};

void FUN_00c759f0_Class::FUN_00c759f0() {
    void* sourceOwner = member_at<void*>(this, 0x2a4);
    void* source = member_at<void*>(sourceOwner, 0x18);
    if (source) {
        void* destination = *member_at<void**>(this, 0x4c);
        member_at<float>(destination, 0x0c) = member_at<float>(source, 0x10);
        member_at<float>(destination, 0x10) =
            member_at<float>(member_at<void*>(member_at<void*>(this, 0x2a4), 0x18), 0x0c);
        member_at<float>(destination, 0x1c) =
            member_at<float>(member_at<void*>(member_at<void*>(this, 0x2a4), 0x18), 0x18);
        member_at<float>(this, 0x290) =
            member_at<float>(member_at<void*>(member_at<void*>(this, 0x2a4), 0x18), 0x04);
        double scale = 0.25;
        member_at<unsigned int>(this, 0x29c) =
            static_cast<unsigned int>(static_cast<float>(member_at<unsigned int>(
                member_at<void*>(member_at<void*>(this, 0x2a4), 0x18), 0x38)) * scale);
        member_at<unsigned int>(this, 0x298) =
            static_cast<unsigned int>(static_cast<float>(member_at<unsigned int>(
                member_at<void*>(member_at<void*>(this, 0x2a4), 0x18), 0x3c)) * scale);
    }
}
