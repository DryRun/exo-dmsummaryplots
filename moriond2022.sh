#!/bin/bash
python plotMMNew.py --analyses boosted_dijet_isrj,dijetbb,trijet,dijet,monojet,monophoton,monoz --scenario V1 --relic --cms_label Preliminary --conference_label "Moriond 2022" --save_tag _moriond2022
python plotMMNew.py --analyses boosted_dijet_isrj,dijetbb,trijet,dijet,monojet,monophoton,monoz --scenario A1 --relic --cms_label Preliminary --conference_label "Moriond 2022" --save_tag _moriond2022

python plotMMNew.py --analyses dilepton,dijet,boosted_dijet_isrj --scenario V2 --relic --cms_label Preliminary --conference_label "Moriond 2022" --save_tag _moriond2022
python plotMMNew.py --analyses dilepton,dijet,boosted_dijet_isrj --scenario A2 --relic --cms_label Preliminary --conference_label "Moriond 2022" --save_tag _moriond2022

python plotMxNew.py --all_cms --scenario SI --cms_label Preliminary --conference_label "Moriond 2022" --save_tag "_moriond2022" --formats "png,pdf" --extend
python plotMxNew.py --all_cms --scenario SD --cms_label Preliminary --conference_label "Moriond 2022" --save_tag "_moriond2022" --formats "png,pdf" --extend

python plotMMNew.py --analyses boosted_dijet_isrj,dijetbb,trijet,dijet,monojet,monophoton,monoz --scenario V1 --relic --cms_label Preliminary --conference_label "Moriond 2022" --save_tag _moriond2022 --logx
python plotMMNew.py --analyses boosted_dijet_isrj,dijetbb,trijet,dijet,monojet,monophoton,monoz --scenario A1 --relic --cms_label Preliminary --conference_label "Moriond 2022" --save_tag _moriond2022 --logx
