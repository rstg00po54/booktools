#H.264 入门篇 - 07 (帧间预测 - 解码图像缓存 DPB)
**目录**















前置文章：















## 1、DPB 的概念

DPB 全称 decoded picture buffer，即解码图片缓存区。

在做视频解码时，需要将最近的若干幅参考帧缓存起来，这个缓冲区就叫做 DPB。解码已经完成的图像被缓存在 DPB 中，供后续帧用作参考图像，因此，解码器需要按照一定的规则对DPB中的图像进行管理。

<img alt="" height="690" src="https://i-blog.csdnimg.cn/blog_migrate/e4bde598031d95e44ab6476e5e750bcc.png" width="903">

DPB中的每一个图像必须处于三种状态中的一种
- Unused for reference：不作为参考帧；- Used for short-term reference：短期参考帧；- Used for long-term reference：长期参考帧；
这3种状态之间的转化，是通过**解码图像标记过程**进行控制的：H.264/AVC 中采用了滑动窗和MMCO两种方式。

滑动窗：是以 DPB 可以存放的帧数为窗口，随着当前解码的图像，以先入先出的方式，将新的解码图像移入，将超出窗口的解码图像移出。因此，DPB 中保存的是最近解码的多个图像。

MMCO：是编码器在码流中传输控制命令，通知解码器对 DPB 中的图像进行状态标记。它支持将一个“Used for reference”标记为“Unused for reference”，也可以将当前帧或者“Used for short-term referene”的帧标记为“Used for long-term reference”等。

DPB 一般以宏块数为单位，计算公式为：

>  
 DpbInMbs = ref * PicWidthInMbs * FrameHeightInMbs 

- ref（参考帧数）- PicWidthInMbs（水平宏块数）- FrameHeightInMbs（垂直宏块数）
## 2、DPB 最大深度

H.264协议规定，在不同的级别（Level）下，最大的解码图片缓存区宏块数（MaxDpbMbs）是不同的：

<img alt="" height="793" src="https://i-blog.csdnimg.cn/blog_migrate/c68bc29dc78af9edb4ac9e10b6f514e3.png" width="1018">



我们可根据 MaxDpbMbs约束 倒推出最大的参考帧数

>  
 max_ref = min(floor(MaxDpbMbs / (PicWidthInMbs * FrameHeightInMbs)), 16) 


>  
 注1：floor(x)是向底舍入函数，返回的是小于等于x的最大整数。 
 注2：因参考帧数（ref）最大只能为16。 


所以最大存储帧数也是最大参考帧数（ref）。

在 SPS 中，max_num_ref_frames 说明了DPB的大小。

## 3、DPB 的行为

### 3.1、清空机制

当解码器收到一个IDR帧时会立即将DPB清空，因为H.264协议规定一个IDR帧之后的任何帧都不会引用该IDR之前的任何帧，所以DPB中的数据已失效，可以清空。这也是IDR帧名称的来源，即 Instantaneous Decoding Refresh – 解码立即重置。

### 3.2、内存分配过大

H.264 bitstream 语法结构(SPS)中定义了一个参数用于通知解码器最大参考帧数。有些不合理的编码器会随便报告一个安全余量很大的参数，实际上可能根本用不到。比如为了图方便在结构体中报告最大参考帧数=16，但实际上最多只用到2帧，如果解码器按照16分配内存则会造成大量的浪费。

对于资源紧张的场合，解码器的设计通常会要求最大参考帧数不能超过某个值，编码器输出的码流必须满足同样的限制才能顺利解码。显然，如果这个限制定为6帧，应该可以解大多数编码器的码流。但是如果定为2帧，则遇到不兼容码流的概率就会显著增加。

### 3.3、内存分配不足

有些不合理的编码器可能会报告一个不恰当的 level。有网友做高清 camera 时，遇到过所有产品型号中统一报告 level=4.1。1000万像素型号也是 level=4.1，但是其实：

1) 一帧4K分辨率的图像

宏块数 = (3840/16)*(2160)/16 = 32,400

按照 level 4.1 准备 DPB 只能存一个参考帧

2) 一帧1000万像素分辨率的图像

宏块数 = (3872/16)*(2592)/16 = 39204 ,

按照 level 5.0 准备 DPB 能存2个参考帧，

按照 level 5.1 则可以存4个参考帧。

按照 level 4.1 则一帧也放不下

所以，这里 1000W 像素的时候，level 写成 4.1 就不合适了
