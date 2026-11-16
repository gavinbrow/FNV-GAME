struct PathCoordinate {
    NiPoint3* FUN_005c3420();
};
struct PathQuery {
    PathCoordinate* FUN_00717e50(NiPoint3*);
};
struct PathNode : NiNode {
    PathQuery* FUN_009ddb30();
};
struct FUN_009de2b0_shell : ActorMover {
    bool FUN_009de2b0(NiPoint3* position);
};

bool FUN_009de2b0_shell::FUN_009de2b0(NiPoint3* position) {
    if (spCurrentPath.operator->() && spCurrentPath.operator->()->FUN_009dc530()) {
        PathQuery* query = reinterpret_cast<PathNode*>(spCurrentPath.operator->())->FUN_009ddb30();
        if (query) {
            NiPoint3 coordinate;
            *position = *query->FUN_00717e50(&coordinate)->FUN_005c3420();
            return true;
        }
    }
    return false;
}
