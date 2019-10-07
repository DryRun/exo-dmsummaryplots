#!/bin/bash
python make_plot_cms.py --cms_text Preliminary --goms 0.05,0.1,0.3,0.5,1.0  --logy --save_tag "_eps2019" --conference_label "EPS 2019" --analyses "_GOM5,B2G17017_w0p01_obs,B2G17017_w0p01_exp,\
_GOM10,EXO17027_obs,EXO17027_exp,\
EXO18012_AK8_obs,EXO18012_AK8_exp,EXO18012_CA15_obs,EXO18012_CA15_exp,\
EXO16057_SR1_obs,EXO16057_SR1_exp,\
EXO16057_SR2_obs,EXO16057_SR2_exp,\
EXO14005_obs,EXO14005_exp,\
EXO16056_narrow_lowmass_obs,\
EXO16056_narrow_lowmass_exp,\
EXO19012_obs,EXO19012_exp,\
_GOM30,EXO16056_wide_obs,\
EXO16056_wide_exp,\
_GOM100,EXO16046_obs,\
EXO16046_exp"

python make_plot_cms.py --cms_text Preliminary --goms 0.05,0.1,0.3,0.5,1.0  --logy --logx --save_tag "_eps2019" --conference_label "EPS 2019"  --analyses "_GOM5,B2G17017_w0p01_obs,B2G17017_w0p01_exp,\
_GOM10,EXO17027_obs,EXO17027_exp,\
EXO18012_AK8_obs,EXO18012_AK8_exp,EXO18012_CA15_obs,EXO18012_CA15_exp,\
EXO16057_SR1_obs,EXO16057_SR1_exp,\
EXO16057_SR2_obs,EXO16057_SR2_exp,\
EXO14005_obs,EXO14005_exp,\
EXO16056_narrow_lowmass_obs,\
EXO16056_narrow_lowmass_exp,\
EXO19012_obs,EXO19012_exp,\
_GOM30,EXO16056_wide_obs,\
EXO16056_wide_exp,\
_GOM100,EXO16046_obs,\
EXO16046_exp"

python make_plot_all_2c.py --cms_text Preliminary --goms 0.05,0.1,0.3,0.5,1.0  --logy --logx --analyses \
_GOM100,ATLAS_EXOT1701_obs,\
EXO16046_obs,ATLAS_EXOT201805_best_PhoTrig_obs,ATLAS_EXOT201805_best_CombTrig_obs,\
_GOM30,ATLAS_EXOT2016020_low_obs,ATLAS_EXOT2016020_high_obs,\
EXO16056_wide_obs,ATLAS_EXOT1621_obs,\
_GOM10,EXO16057_SR1_obs,EXO16057_SR2_obs,\
EXO14005_obs,EXO16056_narrow_lowmass_obs,\
EXO19012_obs,EXO18012_AK8_obs,EXO18012_CA15_obs,\
UA2,EXO17027_obs,\
CDF_Run1,_GOM5,\
CDF_Run2,B2G17017_w0p01_obs \
--save_tag "_eps2019" \
--conference_label "EPS 2019"
# B2G17017_obs

python make_plot_all_2c.py --cms_text Preliminary --goms 0.05,0.1,0.3,0.5,1.0  --logy --analyses \
_GOM100,ATLAS_EXOT1701_obs,\
EXO16046_obs,ATLAS_EXOT201805_best_PhoTrig_obs,ATLAS_EXOT201805_best_CombTrig_obs,\
_GOM30,ATLAS_EXOT2016020_low_obs,ATLAS_EXOT2016020_high_obs,\
EXO16056_wide_obs,ATLAS_EXOT1621_obs,\
_GOM10,EXO16057_SR1_obs,EXO16057_SR2_obs,\
EXO14005_obs,EXO16056_narrow_lowmass_obs,\
EXO19012_obs,EXO18012_AK8_obs,EXO18012_CA15_obs,\
UA2,EXO17027_obs,\
CDF_Run1,_GOM5,\
CDF_Run2,B2G17017_w0p01_obs \
--save_tag "_eps2019" \
--conference_label "EPS 2019"

# For understanding Z'(tt)
python make_plot_all_2c.py --cms_text Preliminary --goms 0.05,0.1,0.3,0.5,1.0  --logy --logx --analyses \
_GOM100,ATLAS_EXOT1701_obs,\
EXO16046_obs,ATLAS_EXOT201805_incl_PhoTrig_obs,ATLAS_EXOT201805_incl_CombTrig_obs,\
_GOM30,ATLAS_EXOT201805_btag_PhoTrig_obs,ATLAS_EXOT201805_btag_CombTrig_obs,\
EXO16056_wide_obs,ATLAS_EXOT2016020_low_obs,ATLAS_EXOT2016020_high_obs,\
_GOM10,ATLAS_EXOT1621_obs,\
EXO14005_obs,EXO16057_SR1_obs,EXO16057_SR2_obs,\
EXO16056_narrow_lowmass_obs,EXO19012_obs,\
EXO18012_AK8_obs,EXO18012_CA15_obs,EXO17027_obs,\
B2G17017_w0p01_obs,B2G17017_w0p1_obs,B2G17017_w0p3_obs,UA2,\
CDF_Run1,CDF_Run2 \
--save_tag "_eps2019_ztt" \
--conference_label "EPS 2019"



# Selective plots

python make_plot_all_2c.py --cms_text Preliminary --goms 0.05,0.1,0.3,0.5,1.0  --logy --logx --analyses \
_GOM100,ATLAS_EXOT1701_obs,\
EXO16046_obs,ATLAS_EXOT201805_best_PhoTrig_obs,ATLAS_EXOT201805_best_CombTrig_obs,\
_GOM30,ATLAS_EXOT2016020_low_obs,ATLAS_EXOT2016020_high_obs,\
EXO16056_wide_obs,ATLAS_EXOT1621_obs,\
_GOM10,EXO16057_SR1_obs,EXO16057_SR2_obs,\
EXO14005_obs,EXO16056_narrow_lowmass_obs,\
EXO19012_obs,EXO18012_AK8_obs,EXO18012_CA15_obs,\
UA2,EXO17027_obs,\
CDF_Run1,_GOM5,\
CDF_Run2,B2G17017_w0p01_obs \
--save_tag "_eps2019_dijet" \
--conference_label "EPS 2019" \
--highlighted EXO16057_SR1_obs,EXO16057_SR2_obs,\
EXO14005_obs,EXO16056_narrow_lowmass_obs,\
EXO19012_obs

python make_plot_all_2c.py --cms_text Preliminary --goms 0.05,0.1,0.3,0.5,1.0  --logy --logx --analyses \
_GOM100,ATLAS_EXOT1701_obs,\
EXO16046_obs,ATLAS_EXOT201805_best_PhoTrig_obs,ATLAS_EXOT201805_best_CombTrig_obs,\
_GOM30,ATLAS_EXOT2016020_low_obs,ATLAS_EXOT2016020_high_obs,\
EXO16056_wide_obs,ATLAS_EXOT1621_obs,\
_GOM10,EXO16057_SR1_obs,EXO16057_SR2_obs,\
EXO14005_obs,EXO16056_narrow_lowmass_obs,\
EXO19012_obs,EXO18012_AK8_obs,EXO18012_CA15_obs,\
UA2,EXO17027_obs,\
CDF_Run1,_GOM5,\
CDF_Run2,B2G17017_w0p01_obs \
--save_tag "_eps2019_dazsle" \
--conference_label "EPS 2019" \
--highlighted EXO18012_AK8_obs,EXO18012_CA15_obs,EXO17027_obs

python make_plot_all_2c.py --cms_text Preliminary --goms 0.05,0.1,0.3,0.5,1.0  --logy --logx --analyses \
_GOM100,ATLAS_EXOT1701_obs,\
EXO16046_obs,ATLAS_EXOT201805_best_PhoTrig_obs,ATLAS_EXOT201805_best_CombTrig_obs,\
_GOM30,ATLAS_EXOT2016020_low_obs,ATLAS_EXOT2016020_high_obs,\
EXO16056_wide_obs,ATLAS_EXOT1621_obs,\
_GOM10,EXO16057_SR1_obs,EXO16057_SR2_obs,\
EXO14005_obs,EXO16056_narrow_lowmass_obs,\
EXO19012_obs,EXO18012_AK8_obs,EXO18012_CA15_obs,\
UA2,EXO17027_obs,\
CDF_Run1,_GOM5,\
CDF_Run2,B2G17017_w0p01_obs \
--save_tag "_eps2019_zpjet" \
--conference_label "EPS 2019" \
--highlighted EXO18012_AK8_obs,EXO18012_CA15_obs

python make_plot_all_2c.py --cms_text Preliminary --goms 0.05,0.1,0.3,0.5,1.0  --logy --logx --analyses \
_GOM100,ATLAS_EXOT1701_obs,\
EXO16046_obs,ATLAS_EXOT201805_best_PhoTrig_obs,ATLAS_EXOT201805_best_CombTrig_obs,\
_GOM30,ATLAS_EXOT2016020_low_obs,ATLAS_EXOT2016020_high_obs,\
EXO16056_wide_obs,ATLAS_EXOT1621_obs,\
_GOM10,EXO16057_SR1_obs,EXO16057_SR2_obs,\
EXO14005_obs,EXO16056_narrow_lowmass_obs,\
EXO19012_obs,EXO18012_AK8_obs,EXO18012_CA15_obs,\
UA2,EXO17027_obs,\
CDF_Run1,_GOM5,\
CDF_Run2,B2G17017_w0p01_obs \
--save_tag "_eps2019_prelhc" \
--conference_label "EPS 2019" \
--highlighted UA2,CDF_Run1,CDF_Run2

python make_plot_cms.py --cms_text Preliminary --goms 0.05,0.1,0.3,0.5,1.0  --logy --logx --save_tag "_eps2019_no16dijet" --conference_label "EPS 2019" --analyses \
_GOM5,B2G17017_w0p01_obs,B2G17017_w0p01_exp,\
_GOM10,EXO17027_obs,EXO17027_exp,\
EXO18012_AK8_obs,EXO18012_AK8_exp,EXO18012_CA15_obs,EXO18012_CA15_exp,\
EXO16057_SR1_obs,EXO16057_SR1_exp,\
EXO16057_SR2_obs,EXO16057_SR2_exp,\
EXO14005_obs,EXO14005_exp,\
EXO16056_narrow_lowmass_obs,\
EXO16056_narrow_lowmass_exp,\
EXO19012_obs,EXO19012_exp,\
_GOM30,EXO16056_wide_obs,\
EXO16056_wide_exp,\
_GOM100,EXO16046_obs,\
EXO16046_exp

python make_plot_cms.py --cms_text Preliminary --goms 0.05,0.1,0.3,0.5,1.0  --logy --logx --save_tag "_eps2019_yes16dijet" --conference_label "EPS 2019" --analyses \
_GOM5,B2G17017_w0p01_obs,B2G17017_w0p01_exp,\
_GOM10,EXO17027_obs,EXO17027_exp,\
EXO18012_AK8_obs,EXO18012_AK8_exp,EXO18012_CA15_obs,EXO18012_CA15_exp,\
EXO16057_SR1_obs,EXO16057_SR1_exp,\
EXO16057_SR2_obs,EXO16057_SR2_exp,\
EXO14005_obs,EXO14005_exp,\
EXO16056_narrow_lowmass_obs,\
EXO16056_narrow_lowmass_exp,\
EXO16056_narrow_highmass_obs,\
EXO16056_narrow_highmass_exp,\
EXO19012_obs,EXO19012_exp,\
_GOM30,EXO16056_wide_obs,\
EXO16056_wide_exp,\
_GOM100,EXO16046_obs,\
EXO16046_exp

python make_plot_cms_dijetlumi.py --cms_text Preliminary --goms 0.05,0.1  --logy --logx --save_tag "_eps2019_dijetlumi" --conference_label "EPS 2019" --analyses \
EXO16056_narrow_lowmass_obs,\
EXO16056_narrow_lowmass_exp,\
EXO16056_narrow_highmass_obs,\
EXO16056_narrow_highmass_exp,\
EXO19012_obs,EXO19012_exp\



convert -density 300 c_gq_cms_eps2019_logx_logy.eps c_gq_cms_eps2019_logx_logy.png
convert -density 300 c_gq_cms_eps2019_linearx_logy.eps c_gq_cms_eps2019_linearx_logy.png
convert -density 300 c_gq_all_2c_eps2019_logx_logy.eps c_gq_all_2c_eps2019_logx_logy.png
convert -density 300 c_gq_all_2c_eps2019_linearx_logy.eps c_gq_all_2c_eps2019_linearx_logy.png
