#!/bin/bash
python plotMMNew.py --analyses boosted_dijet_isrj,dijetbb,dijet,monojet,monophoton,monoz --scenario V1 --relic --cms_label Preliminary --conference_label LP\ 2019 --save_tag _lp2019
python plotMMNew.py --analyses boosted_dijet_isrj,dijet --scenario V2 --relic --cms_label Preliminary --conference_label LP\ 2019 --save_tag _lp2019
python plotMMNew.py --analyses boosted_dijet_isrj,dijetbb,dijet,monojet,monophoton,monoz --scenario A1 --relic --cms_label Preliminary --conference_label LP\ 2019 --save_tag _lp2019
python plotMMNew.py --analyses boosted_dijet_isrj,dijet --scenario A2 --relic --cms_label Preliminary --conference_label LP\ 2019 --save_tag _lp2019
