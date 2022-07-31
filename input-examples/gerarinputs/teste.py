import json

with open('vm.json', 'r') as json_file:    
	dadosvm = json.load(json_file)
	
print(dadosvm['ipcores'][0]['id'])
print(len(dadosvm['ipcores']))


ref_arquivo = open("test3.sh","w")

ref_arquivo.write("#!/bin/bash\n")



instrucoes = [581290490, 1162275455, 9235513739, 37163572837, 140606854261, 2250662455635, 8046645362106,
		211359263, 424001419,	7528425804,	82643621399,	353084116647, 
		27294037,	459645874,	3390830496,	10665877998,	85291899624,
		17918186,	175699198,	1315048503,	5271666584,	19838440041,
		132784277,	810679775,	3078263459,	79594808563,	233806708944]
		
print(len(instrucoes))
	
constraints = {
	'maximum_cost':2.0,
	'maximum_time':1.0,
	'technology':'vm',
	'benchmark':'Experimentos',
	'application':'all_vm'
	}


	
	
	
	

for i in range(len(dadosvm['ipcores'])):


	general = {
		'model_name': dadosvm['ipcores'][i]['id'],
		'mips': dadosvm['ipcores'][i]['mips'],
		'coresVM': dadosvm['ipcores'][i]['coresVM'],
		'memory': dadosvm['ipcores'][i]['memory'],
		'price': dadosvm['ipcores'][i]['price']
	
		}
		
	for j in range(len(instrucoes)):
		preferences = {    
			'simtool': 'cloudsim',    
			'project_name': dadosvm['ipcores'][i]['id']+'-'+str(instrucoes[j]),
			'application': instrucoes[j],
			'DSE': 'true'
			}
		
		exploration = {
			'instructions_for_design': instrucoes[j],
			'corescloudlet_for_design': 32,
			'sup_vm_for_design': [1, 10],
			'original_vm_for_design': [1, 10]

			}
		
		dse = {
			'ExplorationSpace': exploration,
			'Constraints': constraints

			}

		saida = {    
			'Preferences': preferences,    
			'General_Modeling': general,
			'DSE': dse
			}

		with open(dadosvm['ipcores'][i]['id']+'-'+str(j)+'.json', 'w') as json_file:    
			json.dump(saida, json_file, indent=4)
			
			ref_arquivo.write("python MultiExplorer/src/MultiExplorer.py gerarinputs/"+dadosvm['ipcores'][i]['id']+'-'+str(j)+'.json\n')
			
ref_arquivo.write("echo \"FIM\"")
