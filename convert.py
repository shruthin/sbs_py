# initial ffmpeg download, only runs the first time the code is run
import imageio
imageio.plugins.ffmpeg.download()

from moviepy.editor import *
from moviepy.video.tools.drawing import color_split

# load clips
target_clip = VideoFileClip("/home/sn/sbs_py/videos/target.mp4")
source_clip = VideoFileClip("/home/sn/sbs_py/videos/source.mp4")

duration = min(target_clip.duration, source_clip.duration)
fps = min(target_clip.fps, source_clip.fps)

# temp
#duration = 5

tw, th = target_clip.size
sw, sh = source_clip.size

if (tw != sw) or (th != sh):
    # do resizing. not important now bc vids are same size
    pass

width, height = (tw, th)

# make left clip - target
left_mask = color_split((3*width/4, height),
                         p1=(3*width/4, height), p2=(3*width/4, 0),
                         col1=1, col2=0,
                         grad_width=2)
mask_clip_l = ImageClip(left_mask, ismask=True)

clip_left = (target_clip.copy()
                        .subclip(0, duration)
                        .set_mask(mask_clip_l))

# make right clip - source
right_mask = color_split((3*width/4, height),
                         p1=(3*width/4, height), p2=(3*width/4, 0),
                         col1=1, col2=0,
                         grad_width=2)
mask_clip_r = ImageClip(right_mask, ismask=True)

source_clip = source_clip.without_audio() # since not aligned
clip_right = (source_clip.copy()
                         .subclip(0, duration)
                         .set_mask(mask_clip_r))

# join, write to file
cc = CompositeVideoClip([clip_right.set_pos((width/4, 0)),
                         clip_left.set_pos((-width/4, 0))],
                         size=(width, height))
cc.write_videofile("/home/sn/sbs_py/videos/composite.mp4", fps=fps, codec='mpeg4')

print('done')





