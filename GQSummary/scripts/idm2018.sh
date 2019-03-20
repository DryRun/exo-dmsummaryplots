python make_plot_all_selective.py --cms_text Preliminary --goms 0.05,0.1,0.3,0.5,1.0  --logy --logx --analyses \
_GOM100,ATLAS_EXOT1701_obs,\
EXO16046_obs,ATLAS_EXOT1621_obs,\
_GOM30,ATLAS_EXOT2016020_low_obs,ATLAS_EXOT2016020_high_obs,\
EXO16056_wide_obs,ATLAS_CONF16070_ISRy_obs,\
_GOM10,ATLAS_CONF16070_ISRj_obs,\
EXO16056_narrow_obs,CDF_Run1,\
EXO14005_obs,CDF_Run2,\
EXO16057_SR1_obs,EXO16057_SR2_obs,UA2,\
EXO17001_obs\
 --greyed ATLAS_EXOT1701_obs,\
EXO16046_obs,ATLAS_EXOT1621_obs,\
ATLAS_EXOT2016020_low_obs,ATLAS_EXOT2016020_high_obs,\
EXO16056_wide_obs,ATLAS_CONF16070_ISRy_obs,\
ATLAS_CONF16070_ISRj_obs,\
EXO16056_narrow_obs,\
EXO14005_obs,\
EXO16057_SR1_obs,EXO16057_SR2_obs,\
EXO17001_obs\
 --save_tag _pre_LHC

python make_plot_all_selective.py --cms_text Preliminary --goms 0.05,0.1,0.3,0.5,1.0  --logy --logx --analyses \
_GOM100,ATLAS_EXOT1701_obs,\
EXO16046_obs,ATLAS_EXOT1621_obs,\
_GOM30,ATLAS_EXOT2016020_low_obs,ATLAS_EXOT2016020_high_obs,\
EXO16056_wide_obs,ATLAS_CONF16070_ISRy_obs,\
_GOM10,ATLAS_CONF16070_ISRj_obs,\
EXO16056_narrow_obs,CDF_Run1,\
EXO14005_obs,CDF_Run2,\
EXO16057_SR1_obs,EXO16057_SR2_obs,UA2,\
EXO17001_obs\
 --greyed ATLAS_EXOT1701_obs,\
ATLAS_CONF16070_ISRy_obs,\
ATLAS_CONF16070_ISRj_obs,\
CDF_Run1,\
CDF_Run2,\
EXO16057_SR1_obs,EXO16057_SR2_obs,UA2,\
EXO17001_obs\
 --save_tag _LHC_dijet

python make_plot_all_selective.py --cms_text Preliminary --goms 0.05,0.1,0.3,0.5,1.0  --logy --logx --analyses \
_GOM100,ATLAS_EXOT1701_obs,\
EXO16046_obs,ATLAS_EXOT1621_obs,\
_GOM30,ATLAS_EXOT2016020_low_obs,ATLAS_EXOT2016020_high_obs,\
EXO16056_wide_obs,ATLAS_CONF16070_ISRy_obs,\
_GOM10,ATLAS_CONF16070_ISRj_obs,\
EXO16056_narrow_obs,CDF_Run1,\
EXO14005_obs,CDF_Run2,\
EXO16057_SR1_obs,EXO16057_SR2_obs,UA2,\
EXO17001_obs\
 --greyed EXO16046_obs,ATLAS_EXOT1621_obs,\
ATLAS_EXOT2016020_low_obs,ATLAS_EXOT2016020_high_obs,\
EXO16056_wide_obs,\
EXO16056_narrow_obs,CDF_Run1,\
EXO14005_obs,CDF_Run2,\
EXO16057_SR1_obs,EXO16057_SR2_obs,UA2\
 --save_tag _LHC_ISR

python make_plot_all_selective.py --cms_text Preliminary --goms 0.05,0.1,0.3,0.5,1.0  --logy --logx --analyses \
_GOM100,ATLAS_EXOT1701_obs,\
EXO16046_obs,ATLAS_EXOT1621_obs,\
_GOM30,ATLAS_EXOT2016020_low_obs,ATLAS_EXOT2016020_high_obs,\
EXO16056_wide_obs,ATLAS_CONF16070_ISRy_obs,\
_GOM10,ATLAS_CONF16070_ISRj_obs,\
EXO16056_narrow_obs,CDF_Run1,\
EXO14005_obs,CDF_Run2,\
EXO16057_SR1_obs,EXO16057_SR2_obs,UA2,\
EXO17001_obs\
 --greyed ATLAS_EXOT1701_obs,\
EXO16046_obs,ATLAS_EXOT1621_obs,\
ATLAS_EXOT2016020_low_obs,ATLAS_EXOT2016020_high_obs,\
EXO16056_wide_obs,ATLAS_CONF16070_ISRy_obs,\
ATLAS_CONF16070_ISRj_obs,\
EXO16056_narrow_obs,CDF_Run1,\
EXO14005_obs,CDF_Run2,\
UA2,\
EXO17001_obs\
 --save_tag _LHC_bb
