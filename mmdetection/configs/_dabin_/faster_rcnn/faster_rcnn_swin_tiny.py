_base_ = [
    '../_base_/models/faster_rcnn_r50_fpn.py',
    '../_base_/datasets/coco_detection.py',
    '../_base_/schedules/schedule_1x.py', '../_base_/default_runtime.py'
]
pretrained = 'https://github.com/SwinTransformer/storage/releases/download/v1.0.0/swin_tiny_patch4_window7_224.pth'  # noqa
model = dict(
    # type='MaskRCNN', # mask 사용 안 함
    backbone=dict(
        _delete_=True, # (기존 config를 지움) parameter 안 맞는 부분을 미리 지우고 transformer를 한다는 뜻
        type='SwinTransformer',
        embed_dims=96,
        depths=[2, 2, 6, 2],
        num_heads=[3, 6, 12, 24],
        window_size=7,
        mlp_ratio=4,
        qkv_bias=True,
        qk_scale=None,
        drop_rate=0.,
        attn_drop_rate=0.,
        drop_path_rate=0.2,
        patch_norm=True,
        out_indices=(0, 1, 2, 3),
        with_cp=False,
        convert_weights=True,
        init_cfg=dict(type='Pretrained', checkpoint=pretrained)), # checkpoint는 pretrained weight 불러옴. backbone에서 다른 weight 넣어주기
    neck=dict(in_channels=[96, 192, 384, 768])) # 중요! feature의 채널 수

optimizer = dict(
    _delete_=True, # SGD optimizer 였는데, 지우고 adam에 맞춰서 바꿔줌
    type='AdamW',
    lr=0.0001,
    betas=(0.9, 0.999),
    weight_decay=0.05,
    paramwise_cfg=dict(
        custom_keys={
            'absolute_pos_embed': dict(decay_mult=0.),
            'relative_position_bias_table': dict(decay_mult=0.),
            'norm': dict(decay_mult=0.)
        }))
lr_config = dict(min_lr_ratio=0.001)
# lr_config = dict(step=[8, 11])
runner = dict(max_epochs=12)

log_config = dict(
            interval=50,
            hooks=[
                dict(type='MlflowLoggerHook', exp_name='fasterrcnn_swintiny'),
                dict(type='TextLoggerHook'),
                dict(type='WandbLoggerHook',
                     init_kwargs={
                         'entity': 'sodabeans',
                         'project': 'fasterrcnn_swintiny',
                         'name': 'cosann_epoch'
                     })
            ])