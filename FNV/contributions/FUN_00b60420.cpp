struct SweepBucketNode { SweepBucketNode* next; void* value; };
void __cdecl FUN_00aa10f0(void*);
struct FUN_00b580a0_base {
 virtual ~FUN_00b580a0_base();
};
struct FUN_00b60420 : FUN_00b580a0_base {
 unsigned int numBuckets;
 SweepBucketNode** buckets;
 unsigned int unk0c;
 bool freeEntries;
 virtual ~FUN_00b60420();
};
FUN_00b60420::~FUN_00b60420() {
 if (freeEntries) {
  for (unsigned int i=0; i<numBuckets; ++i) {
   SweepBucketNode* node = buckets[i];
   while (node) {
    SweepBucketNode* current = node;
    node = node->next;
    FUN_00aa10f0(current->value);
   }
  }
 }
}