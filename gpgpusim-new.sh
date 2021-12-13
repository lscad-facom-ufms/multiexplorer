#!/bin/bash
#!/bin/bash
# ./gpgpusim-new.sh Rundir Inputs/SM2_GTX480_clock_32768_8_65536_2048_32_ BFSOutput.txt BFSstderr.txt ~/Documentos/Benchmarks/clock
#./gpgpusim-new.sh Rundir Inputs/SM2_GTX480_bfs_100352_2_65536_1024_8_  SM2_GTX480_bfs_100352_2_65536_1024_8_.json BFSOutput.txt BFSstderr.txt Benchmarks/bfs Benchmarks/data/bfs/graph1MW_6.txt
CURRENTDATE=$(date +"%Y-%m-%d-%S-%X")
#RANDOM=$(date +"%s")

if [ "$1" = "-h" ]; then
    echo "$0 <rundir> <configs_folder> <output_name> <error_log_name> <application> <inputs*>"
    exit
fi

if [ -z $1 ] || [ -z $2 ] || [ -z $3 ] || [ -z $4 ];
then
    RUNDIR=$HOME/rundir
    CONFIGS_FOLDER=$HOME/gpgpu-sim_distribution/configs/tested-cfgs/SM2_GTX480
    BFSOUTUPUT=BFSOutput.txt
    BFSERROR=BFSstderr.txt
else
    RUNDIR="rundir/$1-$CURRENTDATE-$((RANDOM % 100000))"
    CONFIGS_FOLDER=$2
    BFSOUTUPUT=$4
    BFSERROR=$5
    
fi

if [ ! -d $RUNDIR ]; then
    mkdir $RUNDIR
fi

cp -a $CONFIGS_FOLDER/* $RUNDIR
#mv $JSONCONFIG  $RUNDIR
#cp -a $CONFIGS_FOLDER $RUNDIR
cd $RUNDIR
#rm -rf $CONFIGS_FOLDER
#cd $RUNDIR

if [ ! -d "output" ]; then
    mkdir "output"
fi

cnt=1
APPLICATION=""

for arg in "$@"
do
    if [ $cnt -gt 4 ]; then
	   if [ -z "$APPLICATION" ]; then
        APPLICATION="$PWD/../../$arg"
	   else
        APPLICATION="$APPLICATION $arg"
	   fi
    fi
    cnt=$((cnt+1))
done
echo ""
echo "****************************************************************************************************************"
echo "App: \"$APPLICATION\""
echo ""
##{ { nohup $APPLICATION; } | (tee BFSOutput.txt ); } 2>&1 &

{ { $APPLICATION; } > >(tee BFSOutput.txt ); } 2> >( tee BFSstderr.txt >&2 )

echo ""
#echo "****************************************************************************************************************"
echo "GPGPU-Sim finished running: \"$APPLICATION\"" 
echo "Input =$CONFIGS_FOLDER "
echo "Used rundir=$RUNDIR"
echo "Output is in $RUNDIR/$BFSOUTUPUT"
echo "Error log is in $RUNDIR/$BFSERROR"
echo ""

#pwd
mv $BFSOUTUPUT output/
mv $BFSERROR output/
#cp $MULTIEXPLORER_INPUT output/
cp *.log output/

# Atribui o diretorio de ambiente (RUNDIR=$HOME/...)
# Copia todas as configurações para o RUNDIR
# Acessa o RUNDIR
# Redireciona saidas para arquivos
# E finaliza citando o rundir onde os resultados estarao.