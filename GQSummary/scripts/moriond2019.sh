#!/bin/bash
python make_plot_cms.py --cms_text Preliminary --goms 0.05,0.1,0.3,0.5,1.0  --logy --save_tag "_moriond19" --conference_label "Moriond 2019"
python make_plot_cms.py --cms_text Preliminary --goms 0.05,0.1,0.3,0.5,1.0  --logy --logx --save_tag "_moriond19" --conference_label "Moriond 2019"
python make_plot_all_2c.py --cms_text Preliminary --goms 0.05,0.1,0.3,0.5,1.0  --logy --logx --analyses \
_GOM100,ATLAS_EXOT1701_obs,\
EXO16046_obs,ATLAS_EXOT201805_incl_PhoTrig_obs,ATLAS_EXOT201805_incl_CombTrig_obs,\
_GOM30,ATLAS_EXOT201805_btag_PhoTrig_obs,ATLAS_EXOT201805_btag_CombTrig_obs,\
EXO16056_wide_obs,ATLAS_EXOT2016020_low_obs,ATLAS_EXOT2016020_high_obs,\
_GOM10,ATLAS_EXOT1621_obs,\
EXO14005_obs,EXO16057_SR1_obs,EXO16057_SR2_obs,\
EXO16056_narrow_lowmass_obs,EXO16056_narrow_highmass_obs,\
EXO17001_obs,EXO17026_obs,\
EXO17027_obs,UA2,\
CDF_Run1,CDF_Run1 \
--save_tag _moriond19 \
--conference_label "Moriond 2019"

python make_plot_all_2c.py --cms_text Preliminary --goms 0.05,0.1,0.3,0.5,1.0  --logy --analyses \
_GOM100,ATLAS_EXOT1701_obs,\
EXO16046_obs,ATLAS_EXOT201805_incl_PhoTrig_obs,ATLAS_EXOT201805_incl_CombTrig_obs,\
_GOM30,ATLAS_EXOT201805_btag_PhoTrig_obs,ATLAS_EXOT201805_btag_CombTrig_obs,\
EXO16056_wide_obs,ATLAS_EXOT2016020_low_obs,ATLAS_EXOT2016020_high_obs,\
_GOM10,ATLAS_EXOT1621_obs,\
EXO14005_obs,EXO16057_SR1_obs,EXO16057_SR2_obs,\
EXO16056_narrow_lowmass_obs,EXO16056_narrow_highmass_obs,\
EXO17001_obs,EXO17026_obs,\
EXO17027_obs,UA2,\
CDF_Run1,CDF_Run1 \
--save_tag _moriond19 \
--conference_label "Moriond 2019"


# ATLAS_EXOT2016033_obs
