#!/bin/bash
python make_plot_cms.py --cms_text Internal --goms 0.05,0.1,0.3,0.5,1.0  --logy --save_tag "_fall18" --conference_label "Fall 2018"
python make_plot_cms.py --cms_text Internal --goms 0.05,0.1,0.3,0.5,1.0  --logy --logx --save_tag "_fall18" --conference_label "Fall 2018"
python make_plot_all_2c.py --cms_text Internal --goms 0.05,0.1,0.3,0.5,1.0  --logy --logx --analyses \
_GOM100,ATLAS_EXOT1701_obs,\
EXO16046_obs,ATLAS_EXOT1621_obs,\
_GOM30,ATLAS_EXOT2016020_low_obs,ATLAS_EXOT2016020_high_obs,\
EXO16056_wide_obs,ATLAS_CONF16070_ISRy_obs,\
_GOM10,ATLAS_CONF16070_ISRj_obs,\
EXO16056_narrow_obs,EXO17026_obs,\
EXO14005_obs,CDF_Run1,\
EXO16057_SR1_obs,EXO16057_SR2_obs,CDF_Run1,\
EXO17001_obs,UA2 \
--save_tag _fall18 \
--conference_label "Fall 2018"


# ATLAS_EXOT2016033_obs