#!/bin/bash
python plotMMNew.py --analyses boosted_dijet_isrj,dijetbb,trijet,dijet,monojet,monophoton,monoz --scenario V1 --relic --cms_label Preliminary --conference_label "LHCP 2020" --save_tag _lhcp2020
python plotMMNew.py --analyses boosted_dijet_isrj,dijetbb,trijet,dijet,monojet,monophoton,monoz --scenario A1 --relic --cms_label Preliminary --conference_label "LHCP 2020" --save_tag _lhcp2020

python plotMMNew.py --analyses dilepton,dijet,boosted_dijet_isrj --scenario V2 --relic --cms_label Internal --conference_label "LHCP 2020" --save_tag _lhcp2020
python plotMMNew.py --analyses dilepton,dijet,boosted_dijet_isrj --scenario A2 --relic --cms_label Internal --conference_label "LHCP 2020" --save_tag _lhcp2020

python plotMxNew.py --all_cms --scenario SI --cms_label Internal --conference_label "LHCP 2020" --save_tag "_lhcp2020" --formats "png,pdf" --extend
python plotMxNew.py --all_cms --scenario SD --cms_label Internal --conference_label "LHCP 2020" --save_tag "_lhcp2020" --formats "png,pdf" --extend

python plotMMNew.py --analyses boosted_dijet_isrj,dijetbb,trijet,dijet,monojet,monophoton,monoz --scenario V1 --relic --cms_label Preliminary --conference_label "LHCP 2020" --save_tag _lhcp2020 --logx
python plotMMNew.py --analyses boosted_dijet_isrj,dijetbb,trijet,dijet,monojet,monophoton,monoz --scenario A1 --relic --cms_label Preliminary --conference_label "LHCP 2020" --save_tag _lhcp2020 --logx
