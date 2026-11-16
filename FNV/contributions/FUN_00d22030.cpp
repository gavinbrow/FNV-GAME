struct ConstraintAtom;
struct ConstraintInfo {
    int maxSizeOfSchema;
    int sizeOfSchemas;
    int numSolverResults;
    int numSolverElemTemps;
    ConstraintAtom* atoms;
    unsigned int sizeOfAllAtoms;
};
struct ConstraintAtom {
    unsigned short type;
    unsigned short unk02;
    int unk04;
    int unk08;
    int unk0C;
    unsigned short unk10;
    unsigned short count;
    ConstraintAtom* next;
    int FUN_00d22030(ConstraintInfo* info);
};
void __cdecl FUN_00d21a60(ConstraintAtom* atom, unsigned int count, ConstraintInfo* result);

int ConstraintAtom::FUN_00d22030(ConstraintInfo* info)
{
    ConstraintAtom* atom = this;
    unsigned int count = 0;
    while (atom->type >= 23) {
        count = atom->count;
        atom = atom->next;
    }
    if (atom->type != 22 && atom->type != 1) {
        ConstraintInfo partial;
        FUN_00d21a60(atom, count, &partial);
        info->numSolverElemTemps -= partial.numSolverElemTemps;
        info->numSolverResults -= partial.numSolverResults;
        info->sizeOfSchemas -= partial.sizeOfSchemas;
    }
    return 0;
}