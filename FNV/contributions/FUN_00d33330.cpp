#include <xmmintrin.h>
#include <string.h>
struct __declspec(align(16)) FUN_00d33330_t {
 __m128 first; __m128 second; int alpha,beta; int reserved28,reserved2c;
int gamma,delta; volatile int epsilon,zeta;
 int coefficients[12]; FUN_00d33330_t& FUN_00d33330(const FUN_00d33330_t& other);
};
FUN_00d33330_t& FUN_00d33330_t::FUN_00d33330(const FUN_00d33330_t& other) {
 first=other.first; second=other.second;
 alpha=other.alpha; beta=other.beta; gamma=other.gamma; delta=other.delta;
 epsilon=other.epsilon; zeta=other.zeta;
 memcpy(coefficients,other.coefficients,48);
 return *this;
}