import random

POPULATION_SIZE = 10
MUTATION_RATE = 0.2
MAX_GENERATIONS = 1000  

def create_chromosome():
    return [random.randint(-10, 10) for _ in range(3)]

def fitness(chromosome, target_value, coefficients, sign):
    x, y, z = chromosome
    result = coefficients[0] * x
    result += coefficients[1] * y if sign[0] == '+' else -coefficients[1] * y
    result += coefficients[2] * z if sign[1] == '+' else -coefficients[2] * z
    return -abs(target_value - result)

def select(population, target_value, coefficients, sign):
    population.sort(key=lambda chromosome: fitness(chromosome, target_value, coefficients, sign), reverse=True)
    return population[:2]

def crossover(parent1, parent2):
    point = random.randint(1, 2)
    child1 = parent1[:point] + parent2[point:]
    child2 = parent2[:point] + parent1[point:]
    return child1, child2

def mutate(chromosome):
    if random.random() < MUTATION_RATE:
        index = random.randint(0, 2)
        chromosome[index] += random.choice([-1, 1])
        chromosome[index] = max(-10, min(10, chromosome[index]))
    return chromosome

def genetic_algorithm(target_value, coefficients, sign):
    population = [create_chromosome() for _ in range(POPULATION_SIZE)]
    generation = 0

    while generation < MAX_GENERATIONS:
        selected = select(population, target_value, coefficients, sign)
        best_chromosome = max(population, key=lambda chromo: fitness(chromo, target_value, coefficients, sign))
        best_fitness = fitness(best_chromosome, target_value, coefficients, sign)
        

        if best_fitness == 0:
            break

        new_population = selected[:]
        while len(new_population) < POPULATION_SIZE:
            parent1, parent2 = random.sample(selected, 2)
            child1, child2 = crossover(parent1, parent2)
            new_population.append(mutate(child1))
            new_population.append(mutate(child2))

        population = new_population[:POPULATION_SIZE]
        generation += 1

    return best_chromosome, best_fitness, generation

def main():
    target_value = int(input("Enter the target value: "))
    coefficients = []
    sign = []
    for i in range(3):
        coeff = int(input(f"Enter the coefficient for variable {chr(120 + i)} (x, y, z): "))
        coefficients.append(coeff)

    for i in range(2):
        sig = input(f"Enter the sign between var {chr(120 + i)} {chr(120 + i + 1)} (x, y, z): ")
        sign.append(sig)

    print(f"\n The equation is: {coefficients[0]}x {sign[0]} {coefficients[1]}y {sign[1]} {coefficients[2]}z = {target_value}")

    best_solution, best_fitness, generation = genetic_algorithm(target_value, coefficients, sign)

    # Compute the final answer using the coefficients, best_solution, and sign
    result = coefficients[0] * best_solution[0]
    result += coefficients[1] * best_solution[1] if sign[0] == '+' else -coefficients[1] * best_solution[1]
    result += coefficients[2] * best_solution[2] if sign[1] == '+' else -coefficients[2] * best_solution[2]

    print(f"\nBest solution found: x = {best_solution[0]}, y = {best_solution[1]}, z = {best_solution[2]} with answer: "
          f"{result}, generation: {generation + 1} and fitness: {best_fitness}")

if __name__ == "__main__":
    main()