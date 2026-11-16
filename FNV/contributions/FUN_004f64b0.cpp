struct IntList {void* first;void* last;~IntList();};
struct Cache {virtual ~Cache();};
struct CachePair {Cache* first;Cache* second;};
extern CachePair caches[9];
extern unsigned int instanceCount;
struct FUN_004f64b0 {virtual ~FUN_004f64b0();IntList regions;bool ownsCache;void FUN_004f6640();};
FUN_004f64b0::~FUN_004f64b0() {
 FUN_004f6640();
 if(ownsCache && --instanceCount==0) {
  Cache* second=0;
  Cache* first=0;
  for(unsigned int i=0;i<9;++i) {
   first=caches[i].first;
   if(first) {caches[i].first=0;delete first;}
   second=caches[i].second;
   if(second) {caches[i].second=0;delete second;}
  }
 }
}
