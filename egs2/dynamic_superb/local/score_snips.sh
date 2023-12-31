#!/usr/bin/env bash
# Copyright Yuekai Zhang, 2021.  Apache 2.0.

# begin configuration section.
cmd=run.pl
stage=0


[ -f ./path.sh ] && . ./path.sh
. parse_options.sh || exit 1;

asr_expdir=$1

for dir in ${asr_expdir}/decode_*/; do
    score_dir=${asr_expdir}/decode_asr_ic1_asr_model_valid.acc.ave/score_f1
    mkdir -p ${score_dir}
    python local/compute_f1.py --hyp_trn ${asr_expdir}/decode_asr_ic1_asr_model_valid.acc.ave/test_snips/score_wer/hyp.trn \
                               --ref_trn ${asr_expdir}/decode_asr_ic1_asr_model_valid.acc.ave/test_snips/score_wer/ref.trn \
              > ${score_dir}/f1_score

done
exit 0
