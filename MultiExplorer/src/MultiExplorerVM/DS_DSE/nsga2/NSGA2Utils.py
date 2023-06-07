# -*- coding: UTF-8 -*-

"""NSGA-II related functions"""
import sys, os

sys.path.append(os.path.dirname(os.path.realpath(__file__))+'/../../')
import functools, json
from nsga2.Population import Population
from MultiExplorer.src.MultiExplorerVM.DS_DSE.DbSelector import DbSelector
import random
from InOutVM import InOut

class NSGA2Utils(object):

    def __init__(self, problem, num_of_individuals, projectFolder, mutation_rate= 0.9 ,mutation_strength=0.01, num_of_genes_to_mutate=2, num_of_tour_particips=2):

        self.problem = problem
        self.num_of_individuals = num_of_individuals
        self.mutation_strength = mutation_strength
        self.mutation_rate= mutation_rate
        self.number_of_genes_to_mutate = num_of_genes_to_mutate
        self.num_of_tour_particips = num_of_tour_particips

        self.bd= json.loads(open(DbSelector(inputName=sys.argv[1]).select_db()).read())
        inputNsga= InOut(projectFolder)
        self.dict_entry= inputNsga.makeInputDict()

    def fast_nondominated_sort(self, population):
        population.fronts = []
        population.fronts.append([])
        for individual in population:
            individual.domination_count = 0
            individual.dominated_solutions = set()

            for other_individual in population:
                if individual.dominates(other_individual):
                    individual.dominated_solutions.add(other_individual)
                elif other_individual.dominates(individual):
                    individual.domination_count += 1
            if individual.domination_count == 0:
                population.fronts[0].append(individual)
                individual.rank = 0
        i = 0
        while len(population.fronts[i]) > 0:
            temp = []
            for individual in population.fronts[i]:
                for other_individual in individual.dominated_solutions:
                    other_individual.domination_count -= 1
                    if other_individual.domination_count == 0:
                        other_individual.rank = i+1
                        temp.append(other_individual)
            i = i+1
            population.fronts.append(temp)

    def __sort_objective(self, val1, val2, m):
        return cmp(val1.objectives[m], val2.objectives[m])

    def calculate_crowding_distance(self, front):
        if len(front) > 0:
            solutions_num = len(front)
            for individual in front:
                individual.crowding_distance = 0

            for m in range(len(front[0].objectives)):
		#print "AQUI", (self.problem.max_objectives[m], self.problem.min_objectives[m])
                front = sorted(front, cmp=functools.partial(self.__sort_objective, m=m))
                front[0].crowding_distance = self.problem.max_objectives[m]
                front[solutions_num-1].crowding_distance = self.problem.max_objectives[m]
                for index, value in enumerate(front[1:solutions_num-1]):
                    front[index].crowding_distance = (front[index+1].crowding_distance - front[index-1].crowding_distance) / (self.problem.max_objectives[m] - self.problem.min_objectives[m])

    def crowding_operator(self, individual, other_individual):
        if (individual.rank < other_individual.rank) or \
            ((individual.rank == other_individual.rank) and (individual.crowding_distance > other_individual.crowding_distance)):
            return 1
        else:
            return -1

    def create_initial_population(self):
        population = Population()
        for _ in range(self.num_of_individuals):
            individual = self.problem.generateIndividual()
            self.problem.calculate_objectives(individual)
            population.population.append(individual)

        return population

    def create_children(self, population):
        children = []
        ##########
        num_mutations= int(self.mutation_rate*len(population))
        cont_mutation=0
        ##########
        while len(children) < len(population):
            parent1 = self.__tournament(population)
            parent2 = parent1

            ###########################################################
            cont=0
            while parent1.features == parent2.features and cont<100: 
                parent2 = self.__tournament(population)
                if cont==99:
                    #print "\t\tevitou loop infinito"
                    pass
                cont=cont+1 #para evitar infinitas iterações, iterações infinitas ocorrem no caso em que toda a população é igual
                #isto ocorre por causa da invariabilidade de soluções boas para o problema em casos quando temos um
                #intervalo pequeno de qtde de nucleos originais e nucleos ips para variar.

            child1, child2 = self.__crossover(parent1, parent2)
            ################# MUTATION #######################
            if cont_mutation<num_mutations:
                self.__mutate(child1)
                cont_mutation=cont_mutation+1
            if cont_mutation<num_mutations:
                self.__mutate(child2)
                cont_mutation=cont_mutation+1
            ##################################################
            self.problem.calculate_objectives(child1)
            self.problem.calculate_objectives(child2)
            children.append(child1)
            children.append(child2)

        return children

    def __crossover(self, individual1, individual2):
        child1 = self.problem.generateIndividual()
        child2 = self.problem.generateIndividual()
        genes_indexes = [0, 1, 5] #0 : amount original cores ; 4 amount ip cores; 5 ip cores
        half_genes_indexes = random.sample(genes_indexes, 1)
        for i in genes_indexes:
            if i in half_genes_indexes:
                child1.features[i] = individual2.features[i]
                child2.features[i] = individual1.features[i]
            else:
                child1.features[i] = individual1.features[i]
                child2.features[i] = individual2.features[i]
        return child1, child2

    #original
    #def __mutate(self, child):
    #    genes_to_mutate = random.sample(range(0, len(child.features)), self.number_of_genes_to_mutate)
    #    for gene in genes_to_mutate:
    #        child.features[gene] = child.features[gene] - self.mutation_strength/2 + random.random() * self.mutation_strength
    #        if child.features[gene] < 0:
    #            child.features[gene] = 0
    #        elif child.features[gene] > 1:
    #            child.features[gene] = 1

    def __mutate(self, child):
        #0 : amount original cores ; 4 amount ip cores; 5 ip cores
        genes_to_mutate = random.sample([0,1,5], self.number_of_genes_to_mutate)
       
        for gene in genes_to_mutate:
            #quando for núcleo ip, substituir por algum do banco aleatoriamente
            if gene == 5:
                child.features[gene] = random.choice(self.bd["ipcores"])
            if gene == 0:
                child.features[gene] = random.randint(self.dict_entry["parameters"]["amount_original_vm"][0], self.dict_entry["parameters"]["amount_original_vm"][1])
            if gene == 1:
                child.features[gene]= random.randint(self.dict_entry["parameters"]["amount_sup_vm"][0], self.dict_entry["parameters"]["amount_sup_vm"][1])
   
    def __tournament(self, population):
        participants = random.sample(population, self.num_of_tour_particips)
        best = None
        for participant in participants:
            if best is None or self.crowding_operator(participant, best) == 1:
                best = participant
        return best
