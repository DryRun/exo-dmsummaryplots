#!/bin/bash
python make_plot_cms.py --cms_text Preliminary --goms 0.05,0.1,0.3,0.5,1.0  --logy
python make_plot_cms.py --cms_text Preliminary --goms 0.05,0.1,0.3,0.5,1.0  --logy --logx
python make_plot_all_2c.py --cms_text Preliminary --goms 0.05,0.1,0.3,0.5,1.0  --logy --logx --analyses _GOM100,ATLAS_EXOT1701_obs,\
EXO16046_obs,ATLAS_EXOT1621_obs,\
_GOM10,ATLAS_CONF16030_low_obs,ATLAS_CONF16030_high_obs,\
EXO16056_narrow_obs,EXO16056_wide_obs,ATLAS_CONF16070_ISRy_obs,\
EXO14005_obs,ATLAS_CONF16070_ISRj_obs,\
EXO16057_SR1_obs,UA2,\
EXO17001_obs,CDF_Run1,\
CDF_Run2,EXO16057_SR2_obs", 

