# Movie Gen

This repository implements the [Movie Gen](https://arxiv.org/abs/2410.13720) model presented by Meta.

Movie Gen is a family of foundation models that can natively generate high-fidelity images and videos
while also possessing the abilities to edit and personalize the videos.

Meta researchers found that scaling the training data, compute, and model parameters of a simple
Transformer-based ([LLaMa3](https://arxiv.org/abs/2407.21783)) model trained with
[Flow Matching](https://arxiv.org/abs/2210.02747) yields high quality generative models for video or audio.

### Features

1. :white_check_mark: Text-to-Video synthesis
2. \[Coming soon] Video personalization
3. \[Coming soon] Video editing

<details>
<summary>TODO</summary>

- [ ] Fix EMA.
- [ ] Use ByT5 for encoding visual text only (i.e., text within quotes).
- [ ] CFG inference.
- [ ] Multi-aspect and variable length video training (including PE interpolation).
- [ ] Fix Model Parallel training.
- [ ] Add FPS conditioning.

</details>

## Demo

|                                                                                                                                                                                                                                                                                                                                                                             32x256x455                                                                                                                                                                                                                                                                                                                                                                              |                                                                                                                                                                                                                                                                                                                                                              32x256x455                                                                                                                                                                                                                                                                                                                                                              |
|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------:|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------:|
|                                                                                                                                                                                                                                                                                                                                   <video src="https://github.com/user-attachments/assets/d9edce76-5301-4171-987c-874f38171cf4" />                                                                                                                                                                                                                                                                                                                                   |                                                                                                                                                                                                                                                                                                                   <video src="https://github.com/user-attachments/assets/703fee8e-2c5d-413c-913c-3e4bbdf72df9" />                                                                                                                                                                                                                                                                                                                    |
|                                                                                                            <details><summary>Caption</summary>The video showcases a person in a black jacket crouching down and embracing a light brown dog against an orange wall. The setting is outdoors, with a white wall and a shadow cast by a tree branch visible in the background, along with trees and an orange railing or fence. The scene captures a warm, affectionate moment shared between the person and their dog, with no noticeable changes in their actions, behaviors, or the surrounding environment between the two frames depicted.</details>                                                                                                             | <details><summary>Caption</summary>The video features a close-up view of a cat with striking blue eyes and a white furry face adorned with brown and black stripes on its head. Initially, the cat is seen looking directly at the camera with an attentive expression, held gently by a human hand around its neck area against a blurred indoor background with a brown surface. As the video progresses, the cat's gaze becomes more intense and focused, with its whiskers appearing more prominent and alert. The camera zooms in slightly, cropping out some of the surrounding area to bring the cat's face into closer view, maintaining the attentive and engaged demeanor of the feline throughout the sequence.</details> |
|                                                                                                                                                                                                                                                                                                                                   <video src="https://github.com/user-attachments/assets/726d3f4c-9be6-4359-923a-62adacd51b69" />                                                                                                                                                                                                                                                                                                                                   |                                                                                                                                                                                                                                                                                                                   <video src="https://github.com/user-attachments/assets/aee3cb34-b868-4c52-a6b7-d1dba3293da5" />                                                                                                                                                                                                                                                                                                                    |
| <details><summary>Caption</summary>The video begins with a solid red background that transitions subtly from a darker shade at the top to a lighter shade at the bottom. Initially, the scene is static with no objects or figures present. As the video progresses, several delicate, translucent rose petals appear against the red backdrop. These petals are in various states of motion; some are suspended in mid-air, while others have fallen and rest on the surface below. The lighting accentuates the soft textures of the petals, creating a contrast with the stark red background. Throughout this transition, there is no clear indication of camera movement, but the positioning of the petals suggests a dynamic entry into the scene.</details> |                                      <details><summary>Caption</summary>The video showcases a majestic snow-capped mountain range against a cloudy sky, with the peaks covered in pristine white snow and jagged rocky outcrops protruding from the slopes. The mountains cast long shadows across the snow-covered terrain below. Initially, the sky is a vivid blue with wispy white clouds, but as the video progresses, the clouds become slightly more dispersed, revealing more of the blue sky. Throughout the video, the overall composition and grandeur of the mountain vistas remain consistent, maintaining the serene and awe-inspiring natural beauty of the landscape.</details>                                      |

## Requirements

<div align="center">

| MindSpore | Ascend Driver |  Firmware   | CANN toolkit/kernel |
|:---------:|:-------------:|:-----------:|:-------------------:|
|   2.3.1   |   24.1.RC2    | 7.3.0.1.231 |    8.0.RC2.beta1    |

</div>

1. Install
   [CANN 8.0.RC2.beta1](https://www.hiascend.com/developer/download/community/result?module=cann&cann=8.0.RC2.beta1)
   and MindSpore according to the [official instructions](https://www.mindspore.cn/install).
2. Install requirements
    ```shell
    pip install -r requirements.txt
    ```

## Model Weights

<details>
<summary><b>TAE</b></summary>

You can download the TAE weights from [here]().

</details>

<details>
<summary><b>Text Encoders</b></summary>

Downloading and conversion of the text encoders' weights to the `.safetensors` format can be done automatically by using
the following commands:

```shell
python tools/download_convert_st.py "google/byt5-small"
python tools/download_convert_st.py "google/ul2"
```

If you face an SSL certificate verification error, you can add `--disable_ssl_verify` option.

</details>

## Inference

### Generating Text Embeddings

Due to the large memory footprint of the text encoders, the inference and training pipelines don't support generating
text embeddings online. Therefore, you need to prepare them in advance by running the following command:

```shell
python inference_text_enc.py \
--model_name google/ul2 \
--prompts_file /path/to/prompts.csv \
--output_path /path/to/output/directory \
--model_max_length 512
```

> [!NOTE]
> We use the sequence length of 512 tokens for UL2, 256 for MetaCLIP, and 100 for ByT5.

### Text-to-Image

For more detailed instructions, please run `python inference.py --help`.

```shell
python inference.py \
--config configs/inference/moviegen_t2i_256x256.yaml \
--model.name llama-5B \
--model.pretrained_model_path /path/to/llama-5B.ckpt \
--text_emb.ul2_dir /path/to/ul2_embeddings \
--text_emb.metaclip_dir /path/to/metaclip_embeddings \
--text_emb.byt5_dir /path/to/byt5_embeddings \
--image_size 256 455 \
--batch_size 2
```

### Text-to-Video

```shell
python inference.py \
--config configs/inference/moviegen_t2i_256x256.yaml \
--model.name llama-5B \
--model.pretrained_model_path /path/to/llama-5B.ckpt \
--text_emb.ul2_dir /path/to/ul2_embeddings \
--text_emb.metaclip_dir /path/to/metaclip_embeddings \
--text_emb.byt5_dir /path/to/byt5_embeddings \
--image_size 256 455 \
--num_frames 32 \
--batch_size 2 \
--save_format mp4
```

### Gradio Demo

To launch the web demo, follow these steps:

1. Install Gradio:

```shell
pip install gradio
```

2. Run the demo script with the following configuration. The demo provides 80 pre-computed text prompts to choose from:

```shell
python gradio_demo.py \
--config configs/inference/moviegen_t2i_256x256.yaml \
--model.name llama-5B \
--model.pretrained_model_path /path/to/llama-5B.ckpt \
--text_emb.ul2_dir /path/to/ul2-embedding.ckpt \
--text_emb.metaclip_dir /path/to/metaclip-embedding.ckpt \
--text_emb.byt5_dir /path/to/byt5-embedding.ckpt \
--image_size 256 455  
--num_frames 32  
--save_format mp4
```

Note: Make sure to replace the `/path/to/` placeholders with your actual model and embedding paths.

## Training

Movie Gen is trained jointly on images and videos in 4 stages:

1. Training on images at 256 px resolution.
2. Joint training on images and videos at 256 px resolution.
3. Joint training at 768 px resolution.
4. Fine-tune the model on high quality videos.

Images are treated as single frame videos, enabling the use of the same model to generate both images and videos.
Compared to video data, paired image-text datasets are easier to scale with diverse concepts and styles,
and thus joint modeling of image and video leads to better generalization.

To train Movie Gen, run the following commands:

```shell
scripts/stage1_train.sh # for stage 1 training
scripts/stage2_train.sh # for stage 2 training
scripts/stage3_train.sh # for stage 3 training (currently under verification)
```

### Dataset Preparation

Paths to videos and their corresponding captions should be stored in a CSV file with two columns: `video` and `caption`.
For example:

```text
video,caption
video_folder/part01/vid001.mp4,a cartoon character is walking through
video_folder/part01/vid002.mp4,a red and white ball with an angry look on its face
```

### Generating Text Embeddings

Due to the large memory footprint of the text encoders, the inference and training pipelines don't support generating
text embeddings online. Please refer to the [Generating Text Embeddings](#generating-text-embeddings) section under the
Inference section for details.

### Cache Video Embedding (Optional)

If you have sufficient storage budget, you can cache the video embeddings to speed up training by using the following
command:

```shell
python inference_tae_enc.py \
--tae.pretrained=/path/to/tae.ckpt \
--tae.dtype=bf16 \
--data.folder=/path/to/folder/with/videos/ \
--output_path=/path/to/output/directory/ \
--data.size=256 \
--data.crop_size=[256,455]
```

### Performance

Experiments were conducted on Ascend 910* using MindSpore 2.3.1 in Graph mode.

> [!NOTE]
> We trained all the models using BF16 precision.

| Model | Cards |   Stage   |       Batch size        |       Resolution        | Jit level | Compile time |        Recompute        | Gradient Acc | TAE Cache | Time (s/step) |                             Config                             |
|:-----:|:-----:|:---------:|:-----------------------:|:-----------------------:|:---------:|:------------:|:-----------------------:|:------------:|:---------:|:-------------:|:--------------------------------------------------------------:|
|  5B   |   8   |  1 (T2I)  |           10            |         256x455         |    O1     |    3m 40s    |           ON            |      1       |    Yes    |     1.29      |  [stage1_t2i_256px.yaml](configs/train/stage1_t2i_256px.yaml)  |
|  5B   |   8   | 2 (T2I/V) |  Image: 1<br/>Video: 1  | 256x455<br/>256 frames  |    O1     |      6m      | ON<br/>(Every 2 blocks) |      5       |    Yes    |     5.09      | [stage2_t2iv_256px.yaml](configs/train/stage2_t2iv_256px.yaml) |
|  5B   |   8   | 3 (T2I/V) |  Image: 1<br/>Video: 1  | 576x1024<br/>256 frames |    O1     |    7m 30s    |           ON            |      5       |    Yes    |     88.5      | [stage3_t2iv_768px.yaml](configs/train/stage3_t2iv_768px.yaml) |
|  1B   |   8   |  1 (T2I)  |           10            |         256x455         |    O1     |    2m 15s    |           ON            |      1       |    Yes    |     0.53      |  [stage1_t2i_256px.yaml](configs/train/stage1_t2i_256px.yaml)  |
|  1B   |   8   | 2 (T2I/V) | Image: 10<br/>Video: 10 |  256x455<br/>32 frames  |    O0     |    1m 55s    |           ON            |      1       |    Yes    |     2.07      | [stage2_t2iv_256px.yaml](configs/train/stage2_t2iv_256px.yaml) |

### Validation During Training

Validation can be enabled by either setting parameters in the `valid` field of the configuration file
([example](configs/train/stage1_t2i_256px.yaml)) or by supplying the following arguments to `train.py`:

```shell
--valid.sampling_steps 10 \
--valid.frequency 100 \
--valid.dataset.csv_path /path/to/valid_dataset.csv \
--valid.dataset.video_folder /path/to/videos \
--valid.dataset.text_emb_folder.ul2 /path/to/ul2_embeddings \
--valid.dataset.text_emb_folder.metaclip /path/to/metaclip_embeddings \
--valid.dataset.text_emb_folder.byt5 /path/to/byt5_embeddings
```

## Evaluation

Coming soon.

## TAE Training & Evaluation

### Dataset Preparation

We need to prepare a csv annotation file listing the path to each input video related to the root folder, indicated by
the `video_folder` argument. An example is

```
video
dance/vid001.mp4
dance/vid002.mp4
dance/vid003.mp4
...
```

Taking UCF-101, for example, please download the [UCF-101](https://www.crcv.ucf.edu/data/UCF101.php) dataset and extract
it to `datasets/UCF-101` folder.

### Training

TAE is trained to optimize the reconstruction loss, perceptual loss, and the outlier penalty loss (OPL) proposed in the
MovieGen paper.

To launch training, please run

```shell
python train_tae.py \
--config configs/tae/train/mixed_256x256x32.yaml \
--output_path /path/to/save_ckpt_and_log \
--csv_path /path/to/video_train.csv  \
--folder /path/to/video_root_folder  \
```

Different from the paper, we found that OPL loss doesn't benefit the training outcome in our ablation study (reducing in
lower PSNR decreased). Thus, we disable OPL loss by default. You may enable it by appending
`--use_outlier_penalty_loss True`

For more details on the arguments, please run `python scripts/train_tae.py --help`

### Evaluation

To run video reconstruction with the trained TAE model and evaluate the PSNR and SSIM on the test set, please run

```shell
python eval_tae.py \
--ckpt_path /path/to/tae.ckpt \
--batch_size 2 \
--num_frames 32  \
--image_size 256 \
--csv_path  /path/to/video_test.csv  \
--folder /path/to/video_root_folder  \
```

The reconstructed videos will be saved in `samples/recons`.

### Performance

Here, we report the training performance and evaluation results on the UCF-101 dataset.

Experiments are tested on ascend 910* with mindspore 2.3.1 graph mode.

| model name | cards | batch size | resolution | precision | jit level | graph compile | s/step | PSNR  | SSIM |                      recipe                       |
|:----------:|:-----:|:----------:|:----------:|:---------:|:---------:|:-------------:|:------:|:-----:|:----:|:-------------------------------------------------:|
|    TAE     |   1   |     1      | 256x256x32 |   bf16    |    O0     |     2 min     |  2.18  | 31.35 | 0.92 | [config](configs/tae/train/mixed_256x256x32.yaml) |