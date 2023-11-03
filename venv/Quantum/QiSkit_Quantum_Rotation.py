import math

#==================================================================================
#                  This is for finding a rotated position easily
#==================================================================================

# Changeable variables
value = math.pi / 4 # replace with value to input divided by π

print("π /", round(value, 3), "\t", end = " | ")
print(round(pow(math.cos(value / 2), 2), 3), "  \t|0> +", round(pow(math.sin(value / 2), 2), 3), "  \t|1>")

step1 = pow(math.cos(value/2), 2)
step2 = math.cos(value/2)
step3 = value/2

print(round(step1, 3))
print(pow(step2, 2))
print(math.cos(step3))

print(math.acos(0.5/0.9238795325112867))

print("\n\t[Basic superpositions]:")

for i in range(5): # Looped version to show multiple values
    value = math.pi/((i + 1) * 0.1)
    print("π /", round(((i + 1) * 0.1), 3), "->\t", end = " | ")
    print(round(pow(math.cos(value / 2), 2), 3), "  \t|0> +", round(pow(math.sin(value / 2), 2), 3), "  \t|1>") # Returns each percentage of both sides 
#print(math.asin(math.sqrt(pow(math.sin(0.5), 2))), " ") # Inverse sin to test