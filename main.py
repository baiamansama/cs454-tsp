import math
import random


class Node:
  def __init__(self, i: int, x: float, y: float):
    self.i = i
    self.x = x
    self.y = y
  
  def dist(self, other) -> float:
    return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)

  def __str__(self):
    return str(self.i)  # + ' ' + str(self.x) + ' ' + str(self.y)


class Path:
  def __init__(self, path):
    self.path = path
    self._path = set(path)
    self.d = -1
    self.f = -1

  def gen(self):
    self.path = []
    self._path = set()
    for i in range(n):
      self.add(cities[i])
    random.shuffle(self.path)

    self.d = -1
    self.f = -1

  def dist(self):
    if self.d == -1:
      self.d = 0
      for i in range(len(self.path)):
        self.d += self.path[i].dist(self.path[(i + 1) % len(self.path)])
    return self.d
  
  def add(self, node: Node):
    self.path.append(node)
    self._path.add(node)
    
    self.d = -1
    self.f = -1
  
  def fitness(self) -> float:
    if self.f == -1:
      self.f = 1 / self.dist()
    return self.f
  
  def mutate(self):
    if random.random() < mutation_rate:
        i = random.randint(0, len(self.path) - 2)
        j = random.randint(i + 1, len(self.path) - 1)
        t = self.path[i]
        self.path[i] = self.path[j]
        self.path[j] = t

    self.d = -1
    self.f = -1
    # print("mutated")
  
  def __getitem__(self, position: int) -> Node:
    return self.path[position]
  
  def __setitem__(self, position: int, value: Node):
    self._path.remove(self.path[position])
    self.path[position] = value
    self._path.add(self.path[position])

    self.d = -1
    self.f = -1

  def __len__(self):
    return len(self.path)

  def __contains__(self, node: Node) -> bool:
    return node in self._path
  
  def __str__(self):
    result = ""
    for node in self.path:
      if not result:
        result = str(node.i)
      else:
        result = result + '\n' + str(node)
    return result


def best(population: 'list[Path]'):
  # print("choosing best")
  result = 0
  chosen = None
  for individual in population:
    if individual.fitness() > result:
      chosen = individual
      result = individual.fitness()
  # print("chose")
  return chosen

def select(population: 'list[Path]'):
  competitors = []
  for i in range(selection_size):
    j = int(random.random() * len(population))
    competitors.append(population[j])
  return best(competitors)

def crossover(a: Path, b: Path):
  # print('well')
  l = random.randint(0, n - 1)
  r = random.randint(l, n - 1)
  path = Path(list())
  # print(len(path))
  for i in range(l, r + 1):
    path.add(a[i])
  # print('well?')
  for i in range(len(b)):
    if b[i] in path:
      continue
    path.add(b[i])
  # print('well??')
  return path

def evolve(population: 'list[Path]'):
  # print('hello')
  next_population = [best(population)]
  # print('hello?')
  for i in range(1, len(population)):
    next_population.append(crossover(select(population), select(population)))
  # print('hello??')
  for i in range(1, len(next_population)):
    next_population[i].mutate()
  # print('hello???')
  return next_population


n = 11849
mutation_rate = 0.010
selection_size = 5
population_size = 50
generations = 400

cities = []
with open('rl11849.tsp', 'r') as f:
  for i in range(6 + n):
    line = f.readline()
    if i >= 6:
      j, x, y = map(float, line.split())
      j = int(j)
      cities.append(Node(j, x, y))

# print('hi')
population = []
for i in range(population_size):
  path = Path(list())
  path.gen()
  population.append(path)
  # print(len(path))

# print('hi?')
for i in range(generations):
  population = evolve(population)
  fittest = best(population)
  print(fittest.dist())
  # print(i + 1, 'evolved')

# print('hi??')
fittest = best(population)

def write_csv(solution):
    with open('solution.csv', mode='w') as f:
        for node in solution:
            f.write(str(node.i))
            f.write('\n')

# print(fittest)
print(fittest.dist())
write_csv(fittest)
# 85890556.74987312