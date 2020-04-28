i=1

AXIAL=${!i}; i=$((i+1))
NJOBS=${!i}; i=$((i+1))
IJOB=${!i}; i=$((i+1))

GRIDPACK="/afs/cern.ch/user/d/dryu/MCI/DMSummaryPlots/src/ExoDMSummaryPlots/input/CMS/Dilepton/gridpack_dilepton.tgz"
if [ "$?" -ne 0 ] || [ ! -e $(basename ${GRIDPACK}) ]; then
   echo "ERROR in copying gridpack.";
   exit 1;
fi


### A2
if [ ${AXIAL} -eq 1 ]; then 
   GQA=0.1
   GDMA=1.0
   GLA=0.1
   
   GQV=0.0
   GDMV=0.0
   GLV=0.00
   
   GNU=0.1

   #~ MMEDARRAY=($(seq 2000 100 4000))
   #~ MDMARRAY=($(seq 0 200 4000))
   #~ MMEDARRAY=($(seq 200 100 2000))
   #~ MDMARRAY=($(seq 2000 200 4000))
   #~ MMEDARRAY=($(seq 100 50 200))
   #~ MDMARRAY=($(seq 0 100 500))
   MMEDARRAY=($(seq 4000 100 4500))
   MDMARRAY=($(seq 4000 1 4000))
else
   ### V2
   GQA=0.0
   GDMA=0.0
   GLA=0.0
   
   GQV=0.1
   GDMV=1.0
   GLV=0.01
   
   GNU=0.01

   #~ MMEDARRAY=($(seq 200 100 4000))
   #~ MDMARRAY=($(seq 0 200 4000))
   #~ MMEDARRAY=($(seq 100 50 200))
   #~ MDMARRAY=($(seq 0 100 500))
   MMEDARRAY=($(seq 2000 100 2500))
   MDMARRAY=($(seq 2000 1 2000))
fi



TOTAL=$((${#MMEDARRAY[@]}*${#MDMARRAY[@]}))
PERJOB=$(($TOTAL/$NJOBS+1))
LOWER=$(($PERJOB*$IJOB))
UPPER=$(($PERJOB*$IJOB+$PERJOB-1))

echo "NJOB" $NJOBS
echo "IJOB" $IJOB
echo "TOTAL" $TOTAL
echo "PERJOB" $PERJOB
echo "LOWER" $LOWER
echo "UPPER" $UPPER

counter=-1
for MMED in ${MMEDARRAY[@]}; do
   for MDM in ${MDMARRAY[@]}; do
      counter=$((counter+1));
      if [ $counter -lt ${LOWER} ] || [ ${counter} -gt ${UPPER} ]; then
         continue;
      fi
      echo "COUNTER="$counter
      echo "MMED="$MMED;
      echo "MDM="$MDM;
      LOG="log_gdmv${GDMV}_gqv${GQV}_gql${GLV}_gdma${GDMA}_gqa${GQA}_gql${GLA}_gnu${GNU}_mmed${MMED}_mdm${MDM}.txt";
      if [ -e ${LOG} ]; then
         echo "Log exists, skipping"
         continue
      else
         tar -xf  $(basename ${GRIDPACK});
         echo "START";
         sh run_single.sh ${GDMV} ${GQV} ${GLV} ${GDMA} ${GQA} ${GLA} ${GNU} ${MMED}.0 ${MDM} test123 500 test123 2>&1 > ${LOG};
         rm -rf MG5_aMC_v2_5_;
      fi
   done
done

