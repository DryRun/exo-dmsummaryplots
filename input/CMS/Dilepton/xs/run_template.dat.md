import model DMsimp_s_spin1_v2_0
define l+ = mu+ e+ ta+
define l- = mu- e- ta-
generate p p > Y1 > l+ l- [QCD]
output /home/dryu/Dijets/data/EightTeeEeVeeBee/ZPrime/MG5_aMC_v2_5_5/ll/1000_pp_gq0p1_gl0p01_DMSimpNLO
launch
set MY1 1000
set MXd 2000
set gVh 0
set gAd11 0
set gAd22 0
set gAd33 0
set gAu11 0
set gAu22 0
set gAu33 0
set gaxc 0
set gaxd 0
set gVd11 0.1
set gVd22 0.1
set gVd33 0.1
set gVu11 0.1
set gVu22 0.1
set gVu33 0.1
set gVl11 0.01
set gVl22 0.01
set gVl33 0.01
set gnu11 0.01
set gnu22 0.01
set gnu33 0.01
set gVu31 0
set gAu31 0
set gVd31 0
set gAd31 0
set gVxc 0
set gVxd 1
set nevents 2500
set ebeam1 6500
set ebeam2 6500
set WY1 auto
launch /home/dryu/Dijets/data/EightTeeEeVeeBee/ZPrime/MG5_aMC_v2_5_5/ll/1000_pp_gq0p1_gl0p01_DMSimpNLO -i
#print_results --format=short
#print_results --path=/home/dryu/Dijets/data/EightTeeEeVeeBee/ZPrime/MG5_aMC_v2_5_5/ll/1000_pp_gq0p1_gl0p01_DMSimpNLO/cross_section.txt --format=short
exit
