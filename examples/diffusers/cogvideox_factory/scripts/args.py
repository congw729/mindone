import argparse


def str2bool(b):
    if b.lower() not in ["false", "true"]:
        raise Exception("Invalid Bool Value")
    if b.lower() in ["false"]:
        return False
    return True


def _get_model_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--pretrained_model_name_or_path",
        type=str,
        default=None,
        required=True,
        help="Path to pretrained model or model identifier from huggingface.co/models.",
    )
    parser.add_argument(
        "--transformer_config",
        type=str,
        default=None,
        help="Config of transformers. If set it, not use the pretrained_model_name_or_path transformer config.",
    )
    parser.add_argument(
        "--transformer_ckpt_path",
        type=str,
        default=None,
        help="Path to the transformer checkpoint. Only effective when set transformer_config.",
    )
    parser.add_argument(
        "--revision",
        type=str,
        default=None,
        required=False,
        help="Revision of pretrained model identifier from huggingface.co/models.",
    )
    parser.add_argument(
        "--variant",
        type=str,
        default=None,
        help="Variant of the model files of the pretrained model identifier from huggingface.co/models, 'e.g.' fp16",
    )
    parser.add_argument(
        "--cache_dir",
        type=str,
        default=None,
        help="The directory where the downloaded models and datasets will be stored.",
    )


def _get_dataset_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--data_root",
        type=str,
        default=None,
        help=("A folder containing the training data."),
    )
    parser.add_argument(
        "--dataset_file",
        type=str,
        default=None,
        help=("Path to a CSV file if loading prompts/video paths using this format."),
    )
    parser.add_argument(
        "--video_column",
        type=str,
        default="video",
        help="The column of the dataset containing videos. Or, the name of the file in `--data_root` folder containing the line-separated path to video data.",
    )
    parser.add_argument(
        "--caption_column",
        type=str,
        default="text",
        help="The column of the dataset containing the instance prompt for each video. Or, the name of the file in `--data_root` folder containing the line-separated instance prompts.",  # noqa: E501
    )
    parser.add_argument(
        "--id_token",
        type=str,
        default=None,
        help="Identifier token appended to the start of each prompt if provided.",
    )
    parser.add_argument(
        "--height_buckets",
        nargs="+",
        type=int,
        default=[480],
    )
    parser.add_argument(
        "--width_buckets",
        nargs="+",
        type=int,
        default=[720],
    )
    parser.add_argument(
        "--frame_buckets",
        nargs="+",
        type=int,
        default=[49],
        help="CogVideoX1.5 need to guarantee that ((num_frames - 1) // self.vae_scale_factor_temporal + 1) % patch_size_t == 0, such as 53",
    )
    parser.add_argument(
        "--vae_cache",
        action="store_true",
        help="Whether to use a pre-encoded tensor dataset of latents instead of videos. "
        "The expected format is that saved by running the `prepare_dataset.py` script.",
    )
    parser.add_argument(
        "--embeddings_cache",
        action="store_true",
        help="Whether to use a pre-encoded tensor dataset of prompt embeddings instead of text prompts. "
        "The expected format is that saved by running the `prepare_dataset.py` script.",
    )
    parser.add_argument(
        "--random_flip",
        type=float,
        default=None,
        help="If random horizontal flip augmentation is to be used, this should be the flip probability.",
    )
    parser.add_argument(
        "--dataloader_num_workers",
        type=int,
        default=1,
        help="Number of subprocesses to use for data loading. 0 means that the data will be loaded in the main process.",
    )
    parser.add_argument(
        "--pin_memory",
        action="store_true",
        help="Whether or not to use the pinned memory setting in dataloader.",
    )
    parser.add_argument(
        "--dynamic_shape",
        action="store_true",
        help="Whether or not to dynamically shape the input images before they are fed to the model.",
    )
    parser.add_argument(
        "--bucket_config",
        default="",
        type=str,
        help="The file path for bucket config.",
    )


def _get_validation_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--validation_prompt",
        type=str,
        default=None,
        help="One or more prompt(s) that is used during validation to verify that the model is learning. Multiple validation prompts should be separated by the '--validation_prompt_seperator' string.",  # noqa: E501
    )
    parser.add_argument(
        "--validation_images",
        type=str,
        default=None,
        help="One or more image path(s)/URLs that is used during validation to verify that the model is learning. Multiple validation paths should be separated by the '--validation_prompt_seperator' string. These should correspond to the order of the validation prompts.",  # noqa: E501
    )
    parser.add_argument(
        "--validation_prompt_separator",
        type=str,
        default=":::",
        help="String that separates multiple validation prompts",
    )
    parser.add_argument(
        "--num_validation_videos",
        type=int,
        default=1,
        help="Number of videos that should be generated during validation per `validation_prompt`.",
    )
    parser.add_argument(
        "--validation_epochs",
        type=int,
        default=None,
        help="Run validation every X training epochs. Validation consists of running the validation prompt `args.num_validation_videos` times.",
    )
    parser.add_argument(
        "--validation_steps",
        type=int,
        default=None,
        help="Run validation every X training steps. Validation consists of running the validation prompt `args.num_validation_videos` times.",
    )
    parser.add_argument(
        "--guidance_scale",
        type=float,
        default=6,
        help="The guidance scale to use while sampling validation videos.",
    )
    parser.add_argument(
        "--use_dynamic_cfg",
        action="store_true",
        default=False,
        help="Whether or not to use the default cosine dynamic guidance schedule when sampling validation videos.",
    )
    parser.add_argument(
        "--enable_model_cpu_offload",
        action="store_true",
        default=False,
        help="Whether or not to enable model-wise CPU offloading when performing validation/testing to save memory.",
    )


def _get_training_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--seed", type=int, default=None, help="A seed for reproducible training.")
    parser.add_argument("--lora_rank", type=int, default=64, help="The rank for LoRA matrices.")
    parser.add_argument(
        "--lora_alpha",
        type=int,
        default=64,
        help="The lora_alpha to compute scaling factor (lora_alpha / rank) for LoRA matrices.",
    )
    parser.add_argument(
        "--mixed_precision",
        type=str,
        default=None,
        choices=["no", "fp16", "bf16"],
        help="Whether to use mixed precision. Choose between fp16 and bf16 (bfloat16)",
    )
    parser.add_argument(
        "--output_dir",
        type=str,
        default="cogvideox-sft",
        help="The output directory where the model predictions and checkpoints will be written.",
    )
    parser.add_argument(
        "--height",
        type=int,
        default=480,
        help="All input videos are resized to this height.",
    )
    parser.add_argument(
        "--width",
        type=int,
        default=720,
        help="All input videos are resized to this width.",
    )
    parser.add_argument(
        "--video_reshape_mode",
        type=str,
        default=None,
        help="All input videos are reshaped to this mode. Choose between ['center', 'random', 'none']",
    )
    parser.add_argument("--fps", type=int, default=8, help="All input videos will be used at this FPS.")
    parser.add_argument(
        "--max_num_frames",
        type=int,
        default=49,
        help="All input videos will be truncated to these many frames.",
    )
    parser.add_argument(
        "--skip_frames_start",
        type=int,
        default=0,
        help="Number of frames to skip from the beginning of each input video. Useful if training data contains intro sequences.",
    )
    parser.add_argument(
        "--skip_frames_end",
        type=int,
        default=0,
        help="Number of frames to skip from the end of each input video. Useful if training data contains outro sequences.",
    )
    parser.add_argument(
        "--train_batch_size",
        type=int,
        default=4,
        help="Batch size (per device) for the training dataloader.",
    )
    parser.add_argument("--num_train_epochs", type=int, default=1)
    parser.add_argument(
        "--max_train_steps",
        type=int,
        default=None,
        help="Total number of training steps to perform. If provided, overrides `--num_train_epochs`.",
    )
    parser.add_argument(
        "--checkpointing_steps",
        type=int,
        default=500,
        help=(
            "Save a checkpoint of the training state every X updates. These checkpoints can be used both as final"
            " checkpoints in case they are better than the last checkpoint, and are also suitable for resuming"
            " training using `--resume_from_checkpoint`."
        ),
    )
    parser.add_argument(
        "--checkpoints_total_limit",
        type=int,
        default=None,
        help=("Max number of checkpoints to store."),
    )
    parser.add_argument(
        "--resume_from_checkpoint",
        type=str,
        default=None,
        help=(
            "Whether training should be resumed from a previous checkpoint. Use a path saved by"
            ' `--checkpointing_steps`, or `"latest"` to automatically select the last available checkpoint.'
        ),
    )
    parser.add_argument(
        "--gradient_accumulation_steps",
        type=int,
        default=1,
        help="Number of updates steps to accumulate before performing a backward/update pass.",
    )
    parser.add_argument(
        "--gradient_checkpointing",
        action="store_true",
        help="Whether or not to use gradient checkpointing to save memory at the expense of slower backward pass.",
    )
    parser.add_argument(
        "--fa_gradient_checkpointing",
        type=str2bool,
        default=False,
        help="Whether or not to use Flash Attention gradient checkpointing to save memory at the expense of slower backward pass.",
    )
    parser.add_argument(
        "--learning_rate",
        type=float,
        default=1e-4,
        help="Initial learning rate (after the potential warmup period) to use.",
    )
    parser.add_argument(
        "--scale_lr",
        action="store_true",
        default=False,
        help="Scale the learning rate by the number of GPUs, gradient accumulation steps, and batch size.",
    )
    parser.add_argument(
        "--lr_scheduler",
        type=str,
        default="constant",
        help=(
            'The scheduler type to use. Choose between ["linear", "cosine", "cosine_with_restarts", "polynomial",'
            ' "constant", "constant_with_warmup"]'
        ),
    )
    parser.add_argument(
        "--lr_warmup_steps",
        type=int,
        default=500,
        help="Number of steps for the warmup in the lr scheduler.",
    )
    parser.add_argument(
        "--lr_num_cycles",
        type=int,
        default=1,
        help="Number of hard resets of the lr in cosine_with_restarts scheduler.",
    )
    parser.add_argument(
        "--lr_power",
        type=float,
        default=1.0,
        help="Power factor of the polynomial scheduler.",
    )
    parser.add_argument(
        "--enable_slicing",
        action="store_true",
        default=False,
        help="Whether or not to use VAE slicing for saving memory.",
    )
    parser.add_argument(
        "--enable_tiling",
        action="store_true",
        default=False,
        help="Whether or not to use VAE tiling for saving memory.",
    )
    parser.add_argument(
        "--noised_image_dropout",
        type=float,
        default=0.05,
        help="Image condition dropout probability when finetuning image-to-video.",
    )
    parser.add_argument(
        "--ignore_learned_positional_embeddings",
        action="store_true",
        default=False,
        help=(
            "Whether to ignore the learned positional embeddings when training CogVideoX Image-to-Video. This setting "
            "should be used when performing multi-resolution training, because CogVideoX-I2V does not support it "
            "otherwise. Please read the comments in https://github.com/a-r-r-o-w/cogvideox-factory/issues/26 to understand why."
        ),
    )
    parser.add_argument(
        "--enable_sequence_parallelism",
        type=str2bool,
        default=False,
        help="whether to enable sequence parallelism. Default is False",
    )
    parser.add_argument(
        "--sequence_parallel_shards",
        default=1,
        type=int,
        help="The number of shards in sequence parallel. Default is 1.",
    )
    parser.add_argument(
        "--max_sequence_length", type=int, default=226, help="Max sequence length of prompt embeddings."
    )


def _get_optimizer_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--optimizer",
        type=lambda s: s.lower(),
        default="adam",
        choices=["adam", "adamw", "adamw_bf16"],
        help=("The optimizer type to use."),
    )
    parser.add_argument(
        "--use_8bit",
        action="store_true",
        help="Whether or not to use 8-bit optimizers from `bitsandbytes` or `bitsandbytes`.",
    )
    parser.add_argument(
        "--use_4bit",
        action="store_true",
        help="Whether or not to use 4-bit optimizers from `torchao`.",
    )
    parser.add_argument(
        "--use_torchao", action="store_true", help="Whether or not to use the `torchao` backend for optimizers."
    )
    parser.add_argument(
        "--beta1",
        type=float,
        default=0.9,
        help="The beta1 parameter for the Adam and Prodigy optimizers.",
    )
    parser.add_argument(
        "--beta2",
        type=float,
        default=0.95,
        help="The beta2 parameter for the Adam and Prodigy optimizers.",
    )
    parser.add_argument(
        "--beta3",
        type=float,
        default=None,
        help="Coefficients for computing the Prodigy optimizer's stepsize using running averages. If set to None, uses the value of square root of beta2.",
    )
    parser.add_argument(
        "--prodigy_decouple",
        action="store_true",
        help="Use AdamW style decoupled weight decay.",
    )
    parser.add_argument(
        "--weight_decay",
        type=float,
        default=1e-04,
        help="Weight decay to use for optimizer.",
    )
    parser.add_argument(
        "--epsilon",
        type=float,
        default=1e-8,
        help="Epsilon value for the Adam optimizer and Prodigy optimizers.",
    )
    parser.add_argument("--max_grad_norm", default=1.0, type=float, help="Max gradient norm.")
    parser.add_argument(
        "--prodigy_use_bias_correction",
        action="store_true",
        help="Turn on Adam's bias correction.",
    )
    parser.add_argument(
        "--prodigy_safeguard_warmup",
        action="store_true",
        help="Remove lr from the denominator of D estimate to avoid issues during warm-up stage.",
    )
    parser.add_argument(
        "--use_cpu_offload_optimizer",
        action="store_true",
        help="Whether or not to use the CPUOffloadOptimizer from TorchAO to perform optimization step and maintain parameters on the CPU.",
    )
    parser.add_argument(
        "--offload_gradients",
        action="store_true",
        help="Whether or not to offload the gradients to CPU when using the CPUOffloadOptimizer from TorchAO.",
    )


def _get_configuration_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--tracker_name", type=str, default=None, help="Project tracker name")
    parser.add_argument(
        "--push_to_hub",
        action="store_true",
        help="Whether or not to push the model to the Hub.",
    )
    parser.add_argument(
        "--hub_token",
        type=str,
        default=None,
        help="The token to use to push to the Model Hub.",
    )
    parser.add_argument(
        "--hub_model_id",
        type=str,
        default=None,
        help="The name of the repository to keep in sync with the local `output_dir`.",
    )
    parser.add_argument(
        "--logging_dir",
        type=str,
        default="logs",
        help="Directory where logs are stored.",
    )
    parser.add_argument(
        "--nccl_timeout",
        type=int,
        default=600,
        help="Maximum timeout duration before which allgather, or related, operations fail in multi-GPU/multi-node training settings.",
    )
    parser.add_argument(
        "--report_to",
        type=str,
        default="tensorboard",
        help=(
            'The integration to report the results and logs to. Supported platforms are `"tensorboard"`'
            ' (default), `"wandb"` and `"comet_ml"`. Use `"all"` to report to all integrations.'
        ),
    )


def _get_mindspore_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--distributed", action="store_true", help="Enable distributed training.")
    parser.add_argument(
        "--mindspore_mode",
        type=int,
        default=1,
        choices=[0, 1],
        help="Forms of MindSpore programming execution, 0 means static graph mode and 1 means dynamic graph mode.",
    )
    parser.add_argument(
        "--jit_level",
        type=str,
        default="O0",
        choices=["O0", "O1", "O2"],
        help=(
            "Used to control the compilation optimization level, supports [O0, O1, O2]. The framework automatically "
            "selects the execution method. O0: All optimizations except those necessary for functionality are "
            "disabled, using an operator-by-operator execution method. O1: Enables common optimizations and automatic "
            "operator fusion optimizations, using an operator-by-operator execution method. This is an experimental "
            "optimization level, which is continuously being improved. O2: Enables extreme performance optimization, "
            "using a sinking execution method. Only effective when args.mindspore_mode is 0"
        ),
    )
    parser.add_argument(
        "--amp_level",
        type=str,
        default="O2",
        choices=["O0", "O1", "O2", "O3"],
        help=(
            "Level of auto mixed precision(amp). Supports [O0, O1, O2, O3]. O0: Do not change. O1: Convert cells"
            "and operators in whitelist to lower precision operations, and keep full precision operations for "
            "the rest. O2: Keep full precision operations for cells and operators in blacklist, and convert "
            "the rest to lower precision operations. O3: Cast network to lower precision."
        ),
    )
    parser.add_argument(
        "--zero_stage",
        type=int,
        default=0,
        choices=[0, 1, 2, 3],
        help="ZeRO-Stage in data parallel.",
    )


def check_args(args):
    if len(args.height_buckets) > 1 or len(args.width_buckets) > 1 or len(args.frame_buckets) > 1:
        raise ValueError(
            "All of training argument (height_buckets, width_buckets, frame_buckets) should be a one-element list."
        )
    if args.dynamic_shape and args.vae_cache:
        raise ValueError("If use dynamic_shape, vae_cache could not be set True.")

    if args.pin_memory:
        raise ValueError("MindSpore does not support pin_memory.")

    if args.enable_model_cpu_offload:
        raise ValueError("MindONE.diffusers does not support `enable_model_cpu_offload` currently.")

    if args.optimizer in ("prodigy", "came"):
        raise ValueError(f"Unsupported optimizer: {args.optimizer}.")

    if args.use_8bit or args.use_4bit or args.use_torchao:
        raise ValueError("Low-bit optimizer is not supported in MindSpore currently.")

    if args.push_to_hub:
        raise ValueError("Pushing results to hub is not supported in MindSpore currently.")


def get_args():
    parser = argparse.ArgumentParser(description="Simple example of a training script for CogVideoX.")

    _get_model_args(parser)
    _get_dataset_args(parser)
    _get_training_args(parser)
    _get_validation_args(parser)
    _get_optimizer_args(parser)
    _get_configuration_args(parser)
    _get_mindspore_args(parser)

    args = parser.parse_args()
    check_args(args)

    return args
