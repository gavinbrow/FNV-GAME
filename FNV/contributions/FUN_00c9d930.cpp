#include "h_82293b07639f.h"
struct ReferencedShape {
    void FUN_00c905b0() throw();
};
struct ShapeBase {
    unsigned short memoryFlags;
    short referenceCount;
    unsigned int userData;
    unsigned int shapeType;
    virtual ~ShapeBase() throw() {}
};
struct ShapeContainerBase {
    virtual ~ShapeContainerBase() throw() {}
};
struct SingleShapeContainer : ShapeContainerBase {
    ReferencedShape* childShape;
    __forceinline ~SingleShapeContainer() throw() {
        if (childShape)
            childShape->FUN_00c905b0();
    }
};
struct BoundingVolumeShape : ShapeBase {
    ReferencedShape* boundingVolume;
    SingleShapeContainer childContainer;
    __forceinline ~BoundingVolumeShape() throw() {
        boundingVolume->FUN_00c905b0();
    }
};
void FUN_00c9d930StandIn::FUN_00c9d930() {
    ((BoundingVolumeShape*)this)->BoundingVolumeShape::~BoundingVolumeShape();
}
