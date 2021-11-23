#!/bin/bash


sim_path="/home/gpgpu-sim/sniper/config"
sim_run="/home/gpgpu-sim/sniper/benchmarks"
sim_data="/home/gpgpu-sim/sniper/experimentos"
nome=smithfield_
tmp=0
tmpfreq=0
freqS=2.8
CURRENT_DIR=$(pwd)

#output="$CURRENT_DIR/output_$processor.txt"


function testar()
{

	
	cd "$sim_path/$processor"


	perl -p -i  -e 's/\$\{([^}]+)\}/defined $ENV{$1} ? $ENV{$1} : $&/eg' > SmithField.cfg < SmithField.cfg.template

	cd $CURRENT_DIR
	
	
	echo "$processor">>$output
	
	cd "$sim_run"
	timeout 3600 ./run-sniper -p parsec-blackscholes -n 32 -i test -c /home/gpgpu-sim/sniper/config/SmithField.cfg -d /home/gpgpu-sim/sniper/experimentos/
	#./singleCoresTests.sh $frequency $output2
	mv $sim_data/sim.out $sim_data/$nome$i$proc$j.txt

	cd $CURRENT_DIR
}

freqp=2.8
proc=_SM_

i=0
#for j in {28..30}
for ((j=1; j<=32-$i; j++))
do
	tmpfreq=$freqp
	tmp=$(expr $i + $j)
	export totalcores=$tmp
	echo $totalcores
	for ((f=0; f<$i; f++))
	do
		tmpfreq="$tmpfreq,$freqS"
	done
	for ((f=2; f<=$j; f++))
	do
		tmpfreq="$tmpfreq,$freqp"
	done
	echo $tmpfreq
	export frequencia=$tmpfreq
	testar
done	


freqp=0.5
proc=_atom_

for i in {1..32}
do
	#for j in {28..30}
	for ((j=1; j<=32-$i; j++))
	do
		tmpfreq=$freqp
		tmp=$(expr $i + $j)
		export totalcores=$tmp
		echo $totalcores
		for ((f=0; f<$i; f++))
		do
			tmpfreq="$tmpfreq,$freqS"
		done
		for ((f=2; f<=$j; f++))
		do
			tmpfreq="$tmpfreq,$freqp"
		done
		echo $tmpfreq
		export frequencia=$tmpfreq
		testar
	done	
done


freqp=1.6
proc=_arm53_

for i in {1..32}
do
	#for j in {28..30}
	for ((j=1; j<=32-$i; j++))
	do
		tmpfreq=$freqp
		tmp=$(expr $i + $j)
		export totalcores=$tmp
		echo $totalcores
		for ((f=0; f<$i; f++))
		do
			tmpfreq="$tmpfreq,$freqS"
		done
		for ((f=2; f<=$j; f++))
		do
			tmpfreq="$tmpfreq,$freqp"
		done
		echo $tmpfreq
		export frequencia=$tmpfreq
		testar
	done	
done


freqp=2.0
proc=_arm57_

for i in {1..32}
do
	#for j in {28..30}
	for ((j=1; j<=32-$i; j++))
	do
		tmpfreq=$freqp
		tmp=$(expr $i + $j)
		export totalcores=$tmp
		echo $totalcores
		for ((f=0; f<$i; f++))
		do
			tmpfreq="$tmpfreq,$freqS"
		done
		for ((f=2; f<=$j; f++))
		do
			tmpfreq="$tmpfreq,$freqp"
		done
		echo $tmpfreq
		export frequencia=$tmpfreq
		testar
	done	
done

freqp=0.4
proc=_quark_

for i in {1..32}
do
	#for j in {28..30}
	for ((j=1; j<=32-$i; j++))
	do
		tmpfreq=$freqp
		tmp=$(expr $i + $j)
		export totalcores=$tmp
		echo $totalcores
		for ((f=0; f<$i; f++))
		do
			tmpfreq="$tmpfreq,$freqS"
		done
		for ((f=2; f<=$j; f++))
		do
			tmpfreq="$tmpfreq,$freqp"
		done
		echo $tmpfreq
		export frequencia=$tmpfreq
		testar
	done	
done


freqp=2.5
proc=_WOLFDALE_

for i in {1..32}
do
	#for j in {28..30}
	for ((j=1; j<=32-$i; j++))
	do
		tmpfreq=$freqp
		tmp=$(expr $i + $j)
		export totalcores=$tmp
		echo $totalcores
		for ((f=0; f<$i; f++))
		do
			tmpfreq="$tmpfreq,$freqS"
		done
		for ((f=2; f<=$j; f++))
		do
			tmpfreq="$tmpfreq,$freqp"
		done
		echo $tmpfreq
		export frequencia=$tmpfreq
		testar
	done	
done


freqp=1.6
proc=_ALLENDALE_

for i in {1..32}
do
	#for j in {28..30}
	for ((j=1; j<=32-$i; j++))
	do
		tmpfreq=$freqp
		tmp=$(expr $i + $j)
		export totalcores=$tmp
		echo $totalcores
		for ((f=0; f<$i; f++))
		do
			tmpfreq="$tmpfreq,$freqS"
		done
		for ((f=2; f<=$j; f++))
		do
			tmpfreq="$tmpfreq,$freqp"
		done
		echo $tmpfreq
		export frequencia=$tmpfreq
		testar
	done	
done


freqp=3.2
proc=_SANTA_ROSA_

for i in {1..32}
do
	#for j in {28..30}
	for ((j=1; j<=32-$i; j++))
	do
		tmpfreq=$freqp
		tmp=$(expr $i + $j)
		export totalcores=$tmp
		echo $totalcores
		for ((f=0; f<$i; f++))
		do
			tmpfreq="$tmpfreq,$freqS"
		done
		for ((f=2; f<=$j; f++))
		do
			tmpfreq="$tmpfreq,$freqp"
		done
		echo $tmpfreq
		export frequencia=$tmpfreq
		testar
	done	
done

#testar
