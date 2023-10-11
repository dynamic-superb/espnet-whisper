#!/usr/bin/env bash
# Set bash to 'debug' mode, it will exit on :
# -e 'error', -u 'undefined variable', -o ... 'error in pipeline', -x 'print commands',
set -e
set -u
set -o pipefail

# train_set="train_combined"
# valid_set="valid"
# test_sets="test_snips"
train_set="train"
valid_set="valid"
test_sets="test"
asr_config=conf/train_asr_whisper_full_correct_specaug.yaml

./asr.sh \
    --lang en \
    --ngpu 4 \
    --use_lm false \
    --use_prompt true \
    --use_nlp_prompt true \
    --token_type whisper_multilingual \
    --feats_normalize '' \
    --feats_type raw \
    --max_wav_duration 50 \
    --audio_format "flac.ark" \
    --inference_nj 24 \
    --inference_asr_model valid.acc.ave.pth \
    --gpu_inference true \
    --inference_config conf/decode_asr_fsd.yaml \
    --asr_config "${asr_config}" \
    --train_set "${train_set}" \
    --valid_set "${valid_set}" \
    --test_sets "${test_sets}" "$@"
