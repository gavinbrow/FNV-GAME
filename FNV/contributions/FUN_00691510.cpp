struct AvoidNodeDescription {
 NiPoint3 point1, point2;
 float radius, cost;
 unsigned int type, flags;
 void FUN_00691590(void* source, unsigned short triangle, float radius, float cost);
};
struct EdgeInfoOps : EdgeExtraInfo { void FUN_00691570(); };
struct StaticAvoidOps : BSSimpleArray<NavMeshStaticAvoidNode,1024> {
 void FUN_00692000(AvoidNodeDescription* node);
};
struct NavMeshOps : NavMesh {
 void FUN_00691510(void* source,unsigned short triangle,float radius,float cost);
};
void NavMeshOps::FUN_00691510(void* source,unsigned short triangle,float radius,float cost) {
 AvoidNodeDescription newNode;
 newNode.FUN_00691590(source,triangle,radius,cost);
 static_cast<EdgeInfoOps*>(Triangles.FUN_00558dd0(triangle,-2147483647-1))->FUN_00691570();
 static_cast<StaticAvoidOps*>(&StaticAvoidNodes)->FUN_00692000(&newNode);
}