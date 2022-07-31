# -*- coding: UTF-8 -*-
import math
from nsga2 import seq
from nsga2.problems.ProblemDefinitions import ProblemDefinitions
from PerformancePredictorVM import PerformancePredictor

class Definitions(ProblemDefinitions):

    def __init__(self):
        self.n = 10
	self.contador = 0



    #features[0] é "amount_original_vm"
    #features[1] é "amount_sup_vm"
    #features[2] é "instructions"
    #features[3] é "corescloudlet"
    #features[4] é "orig_vm"
    #features[5] é "ipcore"

 

    #restriction


    def totalTime(self, individual):
	amount_orig_vm = individual.features[0]
	amount_sup_vm = individual.features[1]

	instructions = individual.features[2]
	corescloudlet = individual.features[3]

	mips_orig = individual.features[4]["mips"]
	coresvm_orig = individual.features[4]["coresVM"]

	mips_sup = individual.features[5]["mips"]
	coresvm_sup = individual.features[5]["coresVM"]
	

	cores_cloudlet_orig = round(amount_orig_vm*coresvm_orig*corescloudlet/(coresvm_orig*amount_orig_vm+coresvm_sup*amount_sup_vm))
	cores_cloudlet_sup = corescloudlet - cores_cloudlet_orig

	instructions_orig = round(instructions*cores_cloudlet_orig/corescloudlet)
	instructions_sup = instructions - instructions_orig

	time_vm_orig = ((((instructions_orig/1000000)/amount_orig_vm)*(cores_cloudlet_orig/amount_orig_vm))/(mips_orig*coresvm_orig))/3600

	time_vm_sup = ((((instructions_sup/1000000)/amount_sup_vm)*(cores_cloudlet_sup/amount_sup_vm))/(mips_sup*coresvm_sup))/3600

	if time_vm_orig > time_vm_sup:
		totalTime = time_vm_orig
	else:
		totalTime = time_vm_sup

        return totalTime
        
    def totalCost(self, individual):
	amount_orig_vm = individual.features[0]
	amount_sup_vm = individual.features[1]

	instructions = individual.features[2]
	corescloudlet = individual.features[3]

	mips_orig = individual.features[4]["mips"]
	coresvm_orig = individual.features[4]["coresVM"]
	price_orig = individual.features[4]["price_orig"]

	mips_sup = individual.features[5]["mips"]
	coresvm_sup = individual.features[5]["coresVM"]
	price_sup = individual.features[5]["price"]
	

	cores_cloudlet_orig = round(amount_orig_vm*coresvm_orig*corescloudlet/(coresvm_orig*amount_orig_vm+coresvm_sup*amount_sup_vm))
	cores_cloudlet_sup = corescloudlet - cores_cloudlet_orig

	instructions_orig = round(instructions*cores_cloudlet_orig/corescloudlet)
	instructions_sup = instructions - instructions_orig

	time_vm_orig = ((((instructions_orig/1000000)/amount_orig_vm)*(cores_cloudlet_orig/amount_orig_vm))/(mips_orig*coresvm_orig))/3600
	if math.ceil(time_vm_orig) == 0:
		cost_vm_orig = 1*price_orig*amount_orig_vm
	else:
		cost_vm_orig = math.ceil(time_vm_orig)*price_orig*amount_orig_vm


	time_vm_sup = ((((instructions_sup/1000000)/amount_sup_vm)*(cores_cloudlet_sup/amount_sup_vm))/(mips_sup*coresvm_sup))/3600

	if math.ceil(time_vm_sup) == 0:
		cost_vm_sup = 1*price_sup*amount_sup_vm
	else:
		cost_vm_sup = math.ceil(time_vm_sup)*price_sup*amount_sup_vm

	totalCost = cost_vm_orig + cost_vm_sup

        return totalCost

    def perfect_pareto_front(self):
        pass
