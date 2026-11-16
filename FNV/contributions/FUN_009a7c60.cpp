float FUN_004579e0(float);
float FUN_00404010(float, float);
float FUN_0040ebd0(float, float);
float FUN_00755660(float);
extern float runtimeInitializationFloat1935;
float FUN_009a7c60(float distance, float height, float speed, float gravity, bool lowArc) {
    float squared = speed * speed;
    float discriminant = squared * squared - (gravity * distance * distance + 2.0 * height * squared) * gravity;
    if (discriminant > 0.0) {
        float lower;
        float selected = FUN_004579e0(discriminant);
        float angle = (squared - selected) / (distance * gravity);
        lower = (squared + selected) / (distance * gravity);
        float root;
        if (lowArc) root = FUN_00404010(angle, lower);
        else root = FUN_0040ebd0(angle, lower);
        float upper = FUN_00755660(root);
        return upper;
    }
    return runtimeInitializationFloat1935 * 0.25;
}
