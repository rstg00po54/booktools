#H.264 入门篇 - 01 (Bitstream)
**目录**















































前置文档：





前面说了编码器将连续的帧经过分割，预测，变换(DCT)，量化，去块滤波，熵编码后，就可以出正常的码流了，但这仅仅是裸的数据，我们还需要将编码器的编码过程信息经过最后一步，打包到最终的比特文件，才形成最终符合 H.264 标准的码流文件；

在之前的部分，提到过 H.264 的比特流文件的组成：

## 1、H.264 比特流格式

字节流中的比特顺序起始于第一个字节的 MSB，处理至第一个字节的 LSB，接着是第二个字节的 MSB

### 1.1、起始字段 (Start Code)

H.264 的 Bitstream 的封装如下所示：

由同步字段 (Start Code) 和 NAL Unit (Network Abstraction Layer，有的地方叫 NALU) 组成；

最初的同步字段的开始是 0x00, 0x00, 0x00, 0x01;

后面的同步字段是 0x00, 0x00, 0x01;

<img alt="" height="231" src="https://i-blog.csdnimg.cn/blog_migrate/bf22db7f62957caefd11225e715b7b07.png" width="1044">

NAL 是 H.264 最基本的数据存储单元，它可以存储很多类型的数据，前面说过，H.264 呢，不仅仅只包含了码流部分，也保留了很多的信息来描述编码的码流信息，如：帧、颜色、使用的参数等；所以这里 NAL 的真实 Payload 就有很多种类型；

### 1.2、NAL Unit 组成

NAL Unit 分为了 [ Header (1 Byte) + Payload ] 部分；

#### 1.2.1、NAL Unit Header

header 部分包含了如下内容
- forbidden_bit (1 bit)：传输中发生错误时，会被置为1，告诉接收方丢掉该单元；否则为 0；- nal_ref_idc (2 bit)：指示当前 NALU 的优先级，或者说重要性，数值越大表明越重要；- nal_unit_type (5 bit)：表示 NALU 的类型；
<img alt="" height="873" src="https://i-blog.csdnimg.cn/blog_migrate/1da826472f3031d32774002a043b4703.png" width="682">

nal_type_id 如下所示：红色部分是对应到 H.264 SEPC 的第 7 章-语法语义（T-REC-H.264）

我们可以根据对应的字符串在SPEC中进行搜索；
| nal_unit_type | Content of NAL unit and RBSP syntax structure | Categories | Annex A NAL unit type class | Annex G and Annex H NAL unit type class 

Content of NAL unit and RBSP syntax structure

Annex A

type class

and

NAL unit
| 0 | 未定义 | non-VCL | non-VCL | non-VCL 

未定义

non-VCL
| 1 | Coded slice of a non-IDR picture slice_layer_without_partitioning_rbsp( ) | 2, 3, 4 | VCL | VCL 

Coded slice of a non-IDR picture

2, 3, 4

VCL
| 2 | Coded slice data partition A slice_data_partition_a_layer_rbsp( ) | 2 | VCL | not applicable 

Coded slice data partition A

2

not
| 3 | Coded slice data partition B slice_data_partition_b_layer_rbsp( ) | 3 | VCL | not applicable 

Coded slice data partition B

3

not
| 4 | Coded slice data partition C slice_data_partition_c_layer_rbsp( ) | 4 | VCL | not applicable 

Coded slice data partition C

4

not
| 5 | Coded slice of an IDR picture slice_layer_without_partitioning_rbsp( ) | 2, 3 | VCL | VCL 

Coded slice of an IDR picture

2, 3

VCL
| 6 | Supplemental enhancement information (SEI) sei_rbsp( ) | 5 | non-VCL | non-VCL 

Supplemental enhancement information (SEI)

5

non-VCL
| 7 | Sequence parameter set seq_parameter_set_rbsp( ) | 0 | non-VCL | non-VCL 

Sequence parameter set

0

non-VCL
| 8 | Picture parameter set pic_parameter_set_rbsp( ) | 1 | non-VCL | non-VCL 

Picture parameter set

1

non-VCL
| 9 | Access unit delimiter access_unit_delimiter_rbsp( ) | 6 | non-VCL | non-VCL 

Access unit delimiter

6

non-VCL
| 10 | End of sequence end_of_seq_rbsp( ) | 7 | non-VCL | non-VCL 

End of sequence

7

non-VCL
| 11 | End of stream end_of_stream_rbsp( ) | 8 | non-VCL | non-VCL 

End of stream

8

non-VCL
| 12 | Filler data filler_data_rbsp( ) | 9 | non-VCL | non-VCL 

Filler data

9

non-VCL
| 13 | Sequence parameter set extension seq_parameter_set_extension_rbsp( ) | 10 | non-VCL | non-VCL 

Sequence parameter set extension

10

non-VCL
| 14 | Prefix NAL unit prefix_nal_unit_rbsp( ) | 2 | non-VCL | suffix dependent 

Prefix NAL unit

2

suffix
| 15 | Subset sequence parameter set subset_seq_parameter_set_rbsp( ) | 0 | non-VCL | non-VCL 

Subset sequence parameter set

0

non-VCL
| 16..18 | Reserved | non-VCL | non-VCL | non-VCL 

Reserved

non-VCL
| 19 | Coded slice of an auxiliary coded picture without partitioning slice_layer_without_partitioning_rbsp( ) | 2, 3, 4 | non-VCL | non-VCL 

Coded slice of an auxiliary coded picture without partitioning

2, 3, 4

non-VCL
| 20 | Coded slice extension slice_layer_extension_rbsp( ) | 2, 3, 4 | non-VCL | VCL 

Coded slice extension

2, 3, 4

VCL
| 21..23 | Reserved | non-VCL | non-VCL | non-VCL 

Reserved

non-VCL
| 24..31 | Unspecified | non-VCL | non-VCL | non-VCL 

Unspecified

non-VCL

>  
 VCL 是 Video Coding Layer 的简写，代表编码的图像数据； 
 包含图像数据的 unit 属于VCL NAL units. 
 SPS、PPS、和SEI 属于Non-VCL NAL Units; 


#### 1.2.2、NAL Unit Payload

NAL Unit 的 Payload 如下所示：

NAL Unit Payload 由 EBSP 构成；

EBSP 抽出 0x03 后，变成了 RBSP；

RBSP 抽出尾部的 Padding 后，构成了真实的有效负载部分；

<img alt="" height="733" src="https://i-blog.csdnimg.cn/blog_migrate/8a1541880ed3f3d342c15aa08b141c22.png" width="764">

**1.2.2.1、EBSP**

首先解释一下 EBSP 的来历，EBSP 主要起到 NAL Unit 的防止竞争的作用；

EBSP 全称 Encapsulated Byte Sequence Payload，称为扩展字节序列载荷。和 RBSP 关系如下：

EBSP ：RBSP 插入防竞争字节（0x03）

这里说明下防止竞争字节（0x03）：H264 会插入一个 StartCode 的字节串来分割NALU，于是问题来了，如果RBSP种也包括了StartCode（0x000001或0x00000001）怎么办呢？所以，就有了防止竞争字节（0x03）：

编码时，扫描 RBSP，如果遇到连续两个0x00字节，就在后面添加防止竞争字节（0x03）；解码时，同样扫描 EBSP，进行逆向操作即可。

**1.2.2.2、RBSP**

RBSP 全称 Raw Byte Sequence Payload，又称原始字节序列载荷。和SODB关系如下：

RBSP = SODB + RBSP Trailing Bits（RBSP尾部补齐字节）

引入 RBSP Trailing Bits做8位字节补齐。

**1.2.2.3、SODB**

SODB 英文全称 String Of Data Bits，称原始数据比特流，就是最原始的编码/压缩得到的数据；

### 1.3、NAL Unit - Slice 组成

如果我们将nal_type_id 来区分不同的 NAL，如下所示：

<img alt="" height="739" src="https://i-blog.csdnimg.cn/blog_migrate/281ff6a8108ea68910a54a0c329dd220.png" width="1200">

## 2、语法和语义

H.264 的 Annex B规定了 NAL Unit 组成 NAL 单元流的方式，对于面向比特的传送，字节流中的比特顺序起始于第一个字节的 MSB，处理至第一个字节的 LSB，接着是第二个字节的 MSB；

它的描述非常类似于代码：

<img alt="" height="893" src="https://i-blog.csdnimg.cn/blog_migrate/0485830c1b9905de6c3930b52cd04994.png" width="717">

第一列代表了语法；

第二列是 Categories，也就是类别的意思；slice data 可以最多分为 3 种 partitioning of slice data；
- Slice data partition A ：包含了类别 2 的所有语法元素；- Slice data partition B ：包含了类别 3 的所有语法元素；- Slice data partition C ：包含了类别 4 的所有语法元素；
如果语法元素或者语法结构的类别标为”All”，它可以出现在所有的语法结构中；

第三列是描述符，规定了每个语法元素的解析处理，对于某些语法元素，需要使用通过竖线分开的两个描述符。在这些情况下，左边的描述符在 entropy_coding_mode_flag 等于 0 的时候使用 ，右边的 描述符在 entropy_coding_mode_flag 等于 1 的时候使用。
- ae(v)：上下文自适应算术熵编码语法元素。- b(8)：任意形式的8比特字节。该描述符的解析过程通过函数read_bits( 8 )的返回值来规定。- ce(v)：左位在先的上下文自适应可变长度熵编码语法元素。- f(n)：n位固定模式比特串（由左至右），左位在先， 该描述符的解析过程通过函数read_bits( n )的返回值来规定。- i(n)：使用n比特的有符号整数。在语法表中，如果n是‘v’，其比特数由其它语法元素值确定。解析过程由函数read_bits(n)的返回值规定，该返回值用最高有效位在前的2的补码表示- me(v)：映射的指数哥伦布码编码的语法元素，左位在先。- se(v)：有符号整数指数哥伦布码编码的语法元素位在先。- te(v)：舍位指数哥伦布码编码语法元素，左位在先。- u(n)：n位无符号整数。在语法表中，如果n是‘v’，其比特数由其它语法元素值确定。解析过程由函数read_bits(n)的返回值规定，该返回值用最高有效位在前的二进制表示。- ue(v)：无符号整数指数哥伦布码编码的语法元素，左位在先。
比如，一个 NAL Unit 的表示为：

<img alt="" height="497" src="https://i-blog.csdnimg.cn/blog_migrate/584ec73f65bbf8b701d91153807c6c9b.png" width="957">

黑色加粗的部分，我打了红色标记，代表了一个 NAL Unit 的组成，这里我们可以看到，为了防止竞争，而插入的 0x03 字节；

<img alt="" height="866" src="https://i-blog.csdnimg.cn/blog_migrate/ae9f0c7f84824712135d603380cbf798.png" width="1200">

所以，这里我们知道了，H.264 使用图表 + 伪代码的方式向我们展现了它的比特流的定义；

NAL Unit 解析的时候，根据不同的 nal_unit_type 走到不同的解析解码流程表格，这些表格都在 H.264 的官方文档种有明确定义；

<img alt="" height="757" src="https://i-blog.csdnimg.cn/blog_migrate/5b2397bec6eb944d395f9ee2979a5c11.png" width="1200">

## 3、SPS 数据语法 (Sequence parameter set data syntax)

### 3.1、SPS 简述

Sequence parameter set data 简称 SPS（序列参数集），SPS 中保存了一组编码视频序列(Coded video sequence)的全局参数。所谓的编码视频序列即原始视频的一帧一帧的像素数据经过编码之后的结构组成的序列。而每一帧的编码后数据所依赖的参数保存于图像参数集中。

一个 SPS 和 PPS 的 NAL Unit 通常位于整个码流的起始位置。但在某些特殊情况下，在码流中间也可能出现这两种结构，主要原因可能为：
1. 解码器需要在码流中间开始解码；1. 编码器在编码的过程中改变了码流的参数（如图像分辨率等）；
### 3.2、SPS 结构

SPS 的结构位于 H.264 准协议文档的 7.3.2.1 部分:

<img alt="" height="918" src="https://i-blog.csdnimg.cn/blog_migrate/5cc3bfebeaebdab81d47b84f48a4e859.png" width="874">

<img alt="" height="469" src="https://i-blog.csdnimg.cn/blog_migrate/68c2e44661005db17b071589120dcfbc.png" width="875">

<img alt="" height="533" src="https://i-blog.csdnimg.cn/blog_migrate/b0aff4eb0addf5a5fe81af08c0c4f53a.png" width="879">

下面将关键的参数罗列一下；

3.2.1、profile_idc

标识当前H.264码流的profile。我们知道，H.264中定义了三种常用的档次profile：

基准档次：baseline profile;

主要档次：main profile;

扩展档次：extended profile;

在H.264的SPS中，第一个字节表示 profile_idc，根据profile_idc的值可以确定码流符合哪一种档次。constraint_set0_flag ~ constraint_set5_flag 是在编码的档次方面对码流增加的其他一些额外限制性条件。

>  
 Baseline profile -- profile_idc = 66 or constraint_set0_flag = 1 
 Constrain baseline -- profile_idc = 66 &amp;&amp; constraint_set1_flag = 1 
 Main profile -- profile_idc = 77 or constraint_set1_flag = 1 
 Extend profile -- profile_idc = 88 or constraint_set2_flag = 1 
 High profile -- profile_idc = 100 
 High 10 -- profile_idc = 110 
 High 422 -- profile_idc = 122 
 High 444 -- profile_idc = 244 


3.2.2、level_idc

标识当前码流的 Level。编码的Level定义了某种条件下的最大视频分辨率、最大视频帧率等参数，码流所遵从的 level 由 level_idc 指定。

<img alt="" height="970" src="https://i-blog.csdnimg.cn/blog_migrate/074ee2b26d9ab0a58357ee7cd939de06.png" width="664">

3.2.3、constraint_set0_flag

当 constraint_set0_flag=1 的时候，代表强制使用 Baseline profile 进行编码；

3.2.4、constraint_set1_flag

当 constraint_set1_flag=1 的时候，代表强制使用 Main profile 进行编码；

3.2.5、constraint_set2_flag

当 constraint_set2_flag=1 的时候，代表强制使用 Extended profile 进行编码；

3.2.6、constraint_set3_flag

— 如果 profile_idc 等于66、77或88（Baseline、Main、Extended）并且 level_idc 等于 11，constraint_set3_flag 等于 1 是指该比特流遵从附件A中对级别1b的所有规定，constraint_set3_flag等于0是指该比特流可以遵从也可以不遵从附件A中有关1b级别的所有规定。

<img alt="" height="565" src="https://i-blog.csdnimg.cn/blog_migrate/16e1afd2f68f0d52b32aaa52b13fa092.png" width="861">

— 否则（profile_idc 等于100、110、122或144或level_ idc不等于 11），constraint_set3_flag 等于1留作未来 ITU-T | ISO/IEC 使用。当profile_idc等于100、110、122或144或level_ idc不等于 11时，比特流中constraint_set3_flag 应等于0。当profile_idc等于100、110、122或144或level_ idc不等于 11时，国际标准的解码器将忽略 constraint_set3_flag 的值。

3.2.7、reserved_zero_4bits

应等于 0，解码器忽略这个值；

3.2.8、seq_parameter_set_id

表示当前的序列参数集 (SPS) 的 id。用于识别图像参数集 (PPS) 所指的序列参数集 (SPS)；

取值范围从 0~31；

当其他的序列参数集语法不一致的时候，编码器将使用不同的 seq_parameter_set_id 来表征；

3.2.9、chroma_format_idc

当 (profile_id==100 || profile_id==110 || profile_id==122 || profile_id==144) 的有这个域，也就是 High Profile 的时候色度采样，值在 0~3 之间；

<img alt="" height="136" src="https://i-blog.csdnimg.cn/blog_migrate/befb1ee14e5fdd69d9929c66048caee6.png" width="532">

当 chroma_format_idc 不存在的时候，默认为 1，即 (4:2:0);

下面是一个 High Profile 带 chroma_format_idc 的例子（使用 Elecard StreamEye Analyzer 分析）

<img alt="" height="703" src="https://i-blog.csdnimg.cn/blog_migrate/e85254bc2247cfad210394ed63956d8b.png" width="799">

3.2.10、residual_colour_transform_flag

当采样为 4:4:4 的时候，会存在 residual_colour_transform_flag 这个值；

<img alt="" height="62" src="https://i-blog.csdnimg.cn/blog_migrate/78bc870dced3104c079dc94b07688daa.png" width="837">

residual_colour_transform_flag 值等于1时 ，使用 SPEC 8.5 节规定的残差颜色变换 。

residual_colour_transform_flag 等于 0 时则不使用残差颜色变换。

当 residual_colour_transform_flag 不存在时，默认其值为 0。

3.2.11、bit_depth_luma_minus8

bit_depth_luma_minus8 是指亮度队列样值的比特深度以及亮度量化参数范围的取值偏移 QpBdOffsetY ，如下所示：

BitDepthY = 8 + bit_depth_luma_minus8

QpBdOffsetY = 6 * bit_depth_luma_minus8

当 bit_depth_luma_minus8 不存在时，应推定其值为 0。

bit_depth_luma_minus8 取值范围应该在 0 到 4 之间；

3.2.12、bit_depth_chroma_minus8

bit_depth_chroma_minus8 是指色度队列样值的比特深度以及色度量化参数范围的取值偏移 QpBdOffsetC ，如下所示：

BitDepthC = 8 + bit_depth_chroma_minus8

QpBdOffsetC = 6 * ( bit_depth_chroma_minus8 + residual_colour_transform_flag )

当 bit_depth_chroma_minus8 不存在时，应推定其值为 0。

bit_depth_chroma_minus8 取值范围应该在 0 到 4 之间（包括 0 和 4）。

3.2.13、log2_max_frame_num_minus4

用于计算 MaxFrameNum 的值。计算公式为

<img alt="" height="40" src="https://i-blog.csdnimg.cn/blog_migrate/e2f9e0d40e28124bff32f8d1665537b8.png" width="334">

MaxFrameNum = 2^(log2_max_frame_num_minus4 + 4)

MaxFrameNum 是 frame_num 的上限值，frame_num 是图像序号的一种表示方法，在帧间编码中常用作一种参考帧标记的手段。

log2_max_frame_num_minus4 的值应在 0-12 范围内（包括 0 和 12）；

3.2.14、pic_order_cnt_type

表示解码 picture order count (POC)的方法。POC是另一种计量图像序号的方式，与frame_num有着不同的计算方法。该语法元素的取值为 0、1 或 2。

参考 SPEC 的 8.2 解码过程；

3.2.15、log2_max_pic_order_cnt_lsb_minus4

用于计算图像顺序数解码过程中的变量 MaxPicOrderCntLsb 的值，该值表示 POC 的上限。计算方法为：

MaxPicOrderCntLsb = 2^(log2_max_pic_order_cnt_lsb_minus4 + 4)。

取值范围 0~12

3.2.16、max_num_ref_frames

用于表示参考帧的最大数目；

规定了可能在视频序列中任何图像帧间预测的解码过程中用到的短期参考帧和长期参考帧、互补参考场对以及不成对的参考场的最大数量。num_ref_frames 字段也决定了 8.2.5.3 节规定的滑动窗口操作的大小。num_ref_frames 的取值范围应该在 0 到 MaxDpbSize （参见 A.3.1 或 A.3.2 节的定义）范围内，包括 0 和 MaxDpbSize；

3.2.17、gaps_in_frame_num_value_allowed_flag

标识位，说明 frame_num 中是否允许不连续的值；

3.2.18、pic_width_in_mbs_minus1

本句法元素加 1 后代表图像宽度，以宏块为单位：

PicWidthInMbs = pic_width_in_mbs_minus1 + 1

通过这个句法元素解码器可以计算得到亮度分量以像素为单位的图像宽度：

PicWidthInSamplesL = PicWidthInMbs * 16

从而也可以得到色度分量以像素为单位的图像宽度：

PicWidthInSamplesC = PicWidthInMbs * 8

以上变量 PicWidthInSamplesL、PicWidthInSamplesC 分别表示图像的亮度(Luma)、色度分量(Chorma)以像素为单位的宽。

比如：

<img alt="" height="888" src="https://i-blog.csdnimg.cn/blog_migrate/014abd1bc8e4d203698ad6dffdd2e51b.png" width="799">

PicWidthInMbs = 79 + 1 = 80

PicWidthInSamplesL = 80 * 16 = 1280

所以这个视频的宽度为 1280；

H.264 将图像的大小在序列参数集中定义，意味着可以在通信过程中随着序列参数集动态地改变图像的大小，甚至可以将传送的图像剪裁后输出。

3.2.19、pic_height_in_map_units_minus1

本句法元素加 1 后，代表以 Slice 组映射为单位的一个解码帧或场的高度

PicHeightInMapUnits = pic_height_in_map_units_minus1 + 1

PicSizeInMapUnits = PicWidthInMbs * PicHeightInMapUnits

FrameHeightInMbs 的计算如下：

FrameHeightInMbs = ( 2 – frame_mbs_only_flag ) * PicHeightInMapUnits

以宏块为单位的图像高度的变量由下列公式得出：

PicHeightInMbs = FrameHeightInMbs / ( 1 + field_pic_flag )

这个 field_pic_flag 被包含在 Slice header 中；

用于亮度分量的图像高度变量由下列公式得出：

PicHeightInSamplesL = PicHeightInMbs * 16

用于色度分量的图像高度变量由下列公式得出：

PicHeightInSamplesC = PicHeightInMbs * MbHeightC

当前图像的 PicSizeInMbs 变量由下列公式得出：

PicSizeInMbs = PicWidthInMbs * PicHeightInMbs

与上面同一个视频的例子：

<img alt="" height="888" src="https://i-blog.csdnimg.cn/blog_migrate/7f6124d0461f8dfca3ffe5be0cd76f49.png" width="799">

PicHeightInMapUnits = 44 + 1 = 45；

FrameHeightInMbs = ( 2 – 1 ) * 45 = 45；

PicHeightInMbs = 45 / ( 1 + field_pic_flag )

field_pic_flag 如果没有的话，就是 0；所以：

<img alt="" height="295" src="https://i-blog.csdnimg.cn/blog_migrate/654e8b8344daf394ca530f0073ddb6fe.png" width="787">

PicHeightInMbs = 45；

PicHeightInSamplesL = 45 * 16 = 720；

3.2.20、frame_mbs_only_flag

标识位，说明宏块的编码方式。

该标识位为0时，宏块可能为帧编码或场编码；

该标识位为1时，所有宏块都采用帧编码。

根据该标识位取值不同，PicHeightInMapUnits 的含义也不同，为0时表示一场数据按宏块计算的高度，为1时表示一帧数据按宏块计算的高度。

如果 frame_mbs_only_flag 等于0，pic_height_in_map_units_minus1加1就表示以宏块为单位的一场的高度。

否则（frame_mbs_only_flag等于1），pic_height_in_map_units_minus1加1就表示以宏块为单位的一帧的高度。

变量 FrameHeightInMbs 由下列公式得出：

FrameHeightInMbs = ( 2 – frame_mbs_only_flag ) * PicHeightInMapUnits

3.2.21、mb_adaptive_frame_field_flag

等于0表示在一个图像的帧和场宏块之间没有交换 。

mb_adaptive_frame_field_flag 等于 1 表示在帧和帧内的场宏块之间可能会有交换。

mb_adaptive_frame_field_flag 没有特别规定时，默认其值为 0。

3.2.22、direct_8x8_inference_flag

标识位，用于 B_Skip、B_Direct 模式运动矢量的推导计算；

3.2.23、frame_cropping_flag

标识位，说明是否需要对输出的图像帧进行裁剪。

3.2.24、vui_parameters_present_flag

标识位，说明SPS中是否存在VUI信息，即，是否存在 vui_parameters() 结构。

3.2.25、小结

这里是按照了 SPEC 来对照看 SPS，也可以从开源软件 X264 源码初始化 SPS 部分和解析SPS相关函数来看如何去解析的；

void x264_sps_init( x264_sps_t *sps, int i_id, x264_param_t *param ) bool x264_analysis_t::h264_decode_sps(uint8_t * buf, uint32_t nLen, GY::x264_SPS_t * sps_data)

## 4、PPS 数据语法 (Picture Parameter Set)

### 4.1、PPS 简述

除了序列参数集SPS之外，H.264中另一重要的参数集合为图像参数集Picture Paramater Set(PPS)。通常情况下，PPS类似于SPS，在H.264的裸码流中单独保存在一个NAL Unit中，只是PPS NAL Unit的nal_unit_type值为8；而在封装格式中，PPS通常与SPS一起，保存在视频文件的文件头中。

### 4.2、PPS 结构

PPS 的语法如下：

<img alt="" height="892" src="https://i-blog.csdnimg.cn/blog_migrate/d6eadee33f4f8e1681357daee314816e.png" width="702">

<img alt="" height="302" src="https://i-blog.csdnimg.cn/blog_migrate/33819b06d456378afbae53c5a183dc9a.png" width="703">

<img alt="" height="179" src="https://i-blog.csdnimg.cn/blog_migrate/06ad963aaa030f2c6a09b683e35cb038.png" width="704">

4.2.1、pic_parameter_set_id

表示当前PPS的id。某个PPS在码流中会被相应的 Slice 引用，slice 引用PPS的方式就是在Slice header 中保存PPS的id值。该值的取值范围为[0,255]

4.2.2、seq_parameter_set_id

表示当前PPS所引用的激活的SPS的id。通过这种方式，PPS中也可以取到对应SPS中的参数。该值的取值范围为[0,31]。

4.2.3、entropy_coding_mode_flag

熵编码模式标识，该标识位表示码流中熵编码/解码选择的算法。对于部分语法元素，在不同的编码配置下，选择的熵编码方式不同。例如在一个宏块语法元素中，宏块类型mb_type的语法元素描述符为“ue(v) | ae(v)”，在baseline profile等设置下采用指数哥伦布编码，在main profile等设置下采用CABAC编码。

标识位entropy_coding_mode_flag的作用就是控制这种算法选择。

当该值为0时，选择左边的算法，通常为指数哥伦布编码或者 CAVLC；

当该值为1时，选择右边的算法，通常为 CABAC。

4.2.4、num_slice_groups_minus1

表示某一帧中 slice group 的个数。当该值为0时，一帧中所有的slice都属于一个slice group。slice group是一帧中宏块的组合方式，定义在协议文档的3.141部分。

4.2.5、num_ref_idx_l0_default_active_minus1、num_ref_idx_l0_default_active_minus1

表示当Slice Header中的num_ref_idx_active_override_flag标识位为0时，P/SP/B slice的语法元素num_ref_idx_l0_active_minus1和num_ref_idx_l1_active_minus1的默认值。

4.2.6、weighted_pred_flag

标识位，表示在P/SP slice中是否开启加权预测。

4.2.7、weighted_bipred_idc

表示在B Slice中加权预测的方法，取值范围为[0,2]。0表示默认加权预测，1表示显式加权预测，2表示隐式加权预测。

4.2.8、pic_init_qp_minus26 和 pic_init_qs_minus26

表示初始的量化参数。实际的量化参数由该参数、slice header中的slice_qp_delta/slice_qs_delta计算得到。

4.2.9、chroma_qp_index_offset

用于计算色度分量的量化参数，取值范围为[-12,12]。

4.2.10、deblocking_filter_control_present_flag

标识位，用于表示Slice header中是否存在用于去块滤波器控制的信息。当该标志位为1时，slice header中包含去块滤波相应的信息；当该标识位为0时，slice header中没有相应的信息。

4.2.11、constrained_intra_pred_flag

若该标识为1，表示I宏块在进行帧内预测时只能使用来自I和SI类型宏块的信息；若该标识位0，表示I宏块可以使用来自Inter类型宏块的信息。

4.2.12、redundant_pic_cnt_present_flag

标识位，用于表示Slice header中是否存在redundant_pic_cnt语法元素。当该标志位为1时，slice header中包含redundant_pic_cnt；当该标识位为0时，slice header中没有相应的信息。

工具也可以解析 PPS：

<img alt="" height="525" src="https://i-blog.csdnimg.cn/blog_migrate/c8c3d66d8baea1efe814d936b5b89208.png" width="834">

## 5、Slice RBSP 数据语法(slice_layer_without_partitioning_rbsp)

如果当前 slice 不采用 slice data partition（A/B/C） 的 RBSP 结构的话，就会是这个RBSP结构，编码时一般都会采用的这个RBSP结构；

我们知道编码是以slice为单位的，这个结构内包含的就是视频中编码的主要内容，视频图像进行编码后就会包含在这个结构内，也就是说编码后的码流中，大多数都是以这个结构的RBSP打包成的NAL unit

<img alt="" height="133" src="https://i-blog.csdnimg.cn/blog_migrate/886e02d52da4d56bbab8b17fb81c6c9f.png" width="702">

可以看到，slice_layer_without_partitioning_rbsp 流程分为了 3 部分；

slice_header(); -- 解析 slice header 流程；

slice_data(); -- 解析 slice_data 流程；

rbsp_slice_trailing_bits(); -- RBSP 尾部按字节补齐的部分；

### 5.1、Slice Header 数据语法

Slice 首先是 header 部分，slice_header 包含的是本 slice 相关的参数，如下；

<img alt="" height="848" src="https://i-blog.csdnimg.cn/blog_migrate/8a6d19bdc50746223d5f58f53f624a91.png" width="706">

<img alt="" height="297" src="https://i-blog.csdnimg.cn/blog_migrate/1d0a1d350b34c43eb7d319333212c165.png" width="706">

<img alt="" height="329" src="https://i-blog.csdnimg.cn/blog_migrate/28fa1917c6477fe254c6d0de9b6a7afb.png" width="707">

5.1.1、first_mb_in_slice

当该 slice 的第一个宏块(Macroblock)在图像中的位置

5.1.2、slice_type

表示当前 slice 的编码类型；

如下表。当slice_type为5~9的时候，就表明要求当前图像的其他slice为slice_type%5，也就是要求当前图像slice_type一致

slice_type 的值在 5 到 9 范围内表示，除了当前 Slice 的编码类型，所有当前编码图像的其他

Slice 的 slice_type 值应与当前条带的 slice_type 值 一样，或者等于当前条带的 slice_type 值减 5
| slice_type | Nane of slice_type 

Nane of slice_type
| 0 | P(P slice) 

P(P slice)
| 1 | B(B slice) 

B(B slice)
| 2 | I(I slice) 

I(I slice)
| 3 | SP(SP slice) 

SP(SP slice)
| 4 | SI(SI slice) 

SI(SI slice)
| 5 | P(P slice) 

P(P slice)
| 6 | B(B slice) 

B(B slice)
| 7 | I(I slice) 

I(I slice)
| 8 | SP(SP slice) 

SP(SP slice)
| 9 | SI(SI slice) 

SI(SI slice)

当 nal_unit_type 等于 5（IDR 图像）时， slice_type 应等于 2、 4、 7 或 9。

当 num_ref_frames 等于 0 时， slice_type 应等于 2、 4、 7 或 9；

使用 Elecard Stream analyzer 查看：

<img alt="" height="640" src="https://i-blog.csdnimg.cn/blog_migrate/d0e44a5c48fcb993996f094a70694ce7.png" width="1200">

5.1.4、pic_parameter_set_id

当前slice所属的PPS的ID，pic_parameter_set_id 的值应该在 0 到 255 范围内；

Elecard Stream analyzer 查看，看到他们都属于 PPS ID = 0；

<img alt="" height="639" src="https://i-blog.csdnimg.cn/blog_migrate/952e62d0e13d99eee56e6f12172b7891.png" width="1200">

5.1.5、frame_num

用于POC计算，请参考  中的frame_num

Elecard Stream analyzer 查看，看到 H.264 的视频前 3 帧 (I、P、P) 的 frame_num 分别为 0、1、2

<img alt="" height="775" src="https://i-blog.csdnimg.cn/blog_migrate/56441f6f880f81543c785af1ab6ef2a0.png" width="1200">

frame_num 不是一直递增的，详见 SPEC 描述；

5.1.6、field_pic_flag

当前slice是否进行的是场编码；

等于 1 表示该 Slice 是一个编码场的 Slice。field_pic_flag 等于 0 表示该 Slice 是一个编码帧的 Slice。当 field_pic_flag 不存在时，应推定其值为 0

变量 MbaffFrameFlag 由下列公式得到：

MbaffFrameFlag = ( mb_adaptive_frame_field_flag &amp;&amp; !field_pic_flag ) (7-22)

以宏块为单位的图像高度的变量由下列公式得出：

PicHeightInMbs = FrameHeightInMbs / ( 1 + field_pic_flag ) (7-23)

用于亮度分量的图像高度变量由下列公式得出：

PicHeightInSamplesL = PicHeightInMbs * 16 (7-24)

用于色度分量的图像高度变量由下列公式得出：

PicHeightInSamplesC = PicHeightInMbs * MbHeightC (7-25)

当前图像的 PicSizeInMbs 变量由下列公式得出：

PicSizeInMbs = PicWidthInMbs * PicHeightInMbs (7-26)

变量 MaxPicNum 由下列公式得出：

— 如果 field_pic_flag 等于 0，MaxPicNum 设为等于 MaxFrameNum。

— 否则（field_pic_flag 等于 1），MaxPicNum 设为等于 2*MaxFrameNum。

变量 CurrPicNum 由下列公式得出：

— 如果 field_pic_flag 等于 0，CurrPicNum 设为等于 frame_num。

— 否则（field_pic_flag 等于 1），CurrPicNum 设为等于 2 * frame_num + 1

5.1.7、bottom_field_flag

等于 1 表示该条带是一个编码底场的一部分。bottom_field_flag 等于 0 表示该图像是一个编

码的顶场。当该条带不存在此语法元素时，应推定其值为 0

5.1.8、idr_pic_id

只有 slice_type == 5 的时候 (IDR picture) 的时候，才会存在这个 field；

标识一个 IDR 图像的 ID。

一个 IDR 图像的所有 Slice 中的 idr_pic_id 值应保持不变。当按解码顺序的两个连续访问单元都是 IDR 访问单元时，第一个 IDR 访问单元的 Slice 的 idr_pic_id 值应与第二个 IDR 访问单元的 idr_pic_id 值不同。idr_pic_id 的值应在 0 到 65535 的范围内（包括 0 和 65535）；

使用 Elecard StreamAnalyzer ，选中 H.264 的第一帧 (I 帧) 查看如下：

<img alt="" height="642" src="https://i-blog.csdnimg.cn/blog_migrate/eacda7d0758fb036dc8f15b38c2d126b.png" width="1200">

选中 H.264 的第2个关键帧 (I 帧) 查看：

<img alt="" height="250" src="https://i-blog.csdnimg.cn/blog_migrate/334b615ac9d5ac55d9903df0a331a0e9.png" width="1200">

5.1.9、pic_order_cnt_lsb、delta_pic_order_cnt_bottom、delta_pic_order_cnt

三个都是用于计算POC，请参考 

5.1.10、redundant_pic_cnt

冗余图像编码相关

5.1.11、direct_spatial_mv_pred_flag

1：B帧direct编码采用空域预测方式

0：B帧direct编码采用时域预测方式，请参考

5.1.12、Others
- num_ref_idx_active_override_flag 当前slice的参考图像列表是否采用以下两个长度而不用PPS规定的长度- num_ref_idx_l0_active_minus1 前向参考图像列表长度- num_ref_idx_l1_active_minus1 后续参考图像列表长度- ref_pic_list_modification 参考图像列表重排序的参数结构语法，请结合标准并参考-&gt;参考图像列表-&gt;参考图像列表重排序- pred_weight_table 加权预测的参数结构语法，请结合标准并参考- dec_ref_pic_marking 解码图像标记的参数结构语法，请结合标准并参考-&gt;解码图像缓存-&gt;解码图像标记过程- cabac_init_idc cabac中m、n表的索引- slice_qp_delta pic_init_qp_minus26 + 26 + slice_qp_delta将成为当前slice的初始QP- disable_deblocking_filter_idc- slice_alpha_c0_offset_div2- slice_beta_offset_div2 以上三个是的相关参数<li>
### 5.2、Slice Data 数据语法

slice_data是slice的主体部分，当前slice内的宏块编码后的信息都在其中；

<img alt="" height="922" src="https://i-blog.csdnimg.cn/blog_migrate/ff97ca9f66812770884aba50e87f9f47.png" width="705">

<img alt="" height="81" src="https://i-blog.csdnimg.cn/blog_migrate/c1e3dec9df6aae6ac62381307ede5d87.png" width="703">
- cabac_alignment_one_bit 如果是cabac，需要slice_data的头部8bit对齐，因此可能需要插入1- mb_skip_run 如果当前采用的是CAVLC编码方式，则会采用这个语法元素来表达 skip 宏块（P_Skip，B_Skip），mb_skip_run 代表的是当前这个宏块以及它的后面共有多少个跳过宏块，并且后面的 skip 宏块都不会被编码。- mb_skip_flag 如果当前采用的是CABAC编码方式，则会采用这个语法元素来表达skip宏块（P_Skip，B_Skip），跟mb_skip_run不同的是，每个skip宏块都有一个mb_skip_flag- macroblock_layer 如果不是为skip宏块的话，则表明本宏块有编码的数据，因此会进去macroblock_layer- end_of_slice_flag 如果采用的是CABAC编码方式，还会用这个标记来表达当前宏块是否为这个slice的最后一个宏块
### 5.3、宏块数据语法 (macroblock_layer)

<img alt="" height="910" src="https://i-blog.csdnimg.cn/blog_migrate/df1bde4283b28a7b1464bfd001ab2a6b.png" width="705">

<img alt="" height="105" src="https://i-blog.csdnimg.cn/blog_migrate/e3d622e3e26c9447f61b4992c7a834ce.png" width="703">
- mb_type 当前宏块的类型，对于不同的slice（I,P,B），同一个值会表示不同的类型。而且这个类型不仅仅表达宏块的预测模式，分割方式，还有其他的一些信息，请参考- pcm_alignment_zero_bit 在PCM情况下会要求进行字节对齐- pcm_sample_luma 亮度的PCM，一共有16x16个- pcm_sample_chroma 色度的PCM，根据yuv的格式不同会有不同的个数，一般的4:2:0格式有8x8x2个- sub_mb_pred 子宏块预测的语法结构，子宏块为8x8大小的宏块，也就是说一个宏块有4个子宏块，在这个语法结构的内部会进行4次子宏块预测<li>transform_size_8x8_flag 宏块所采用的变换方法0：4x4DCT；1：8x8DCT。变换方法请参考。按照上述语法描述，只有满足了以下条件码流中才会出现这个语法元素，如果该语法元素没出现在码流中则默认为0。 
  <ul>- Intra：总开关transform_8x8_mode_flag为1，并且宏块类型为I_NxN（参考，如果是I_8x8则为1，如果是I_4x4则为0）。- Inter：总开关transform_8x8_mode_flag为1，并且宏块的预测模式块不小于8x8。另外如果宏块采用了直接预测方式，并且预测模式为B_Direct_16x16，则需要direct_8x8_inference_flag为1。（此时码流中transform_size_8x8_flag的值为0或者1，是在编码端由算法自行决定的）。- Intra_16x16以及I_PCM的情况下码流中不存在该语法元素。- mb_pred 宏块预测的语法结构，宏块预测与子宏块预测的语法结构是相斥的，一个宏块的组成结构要么采用的是宏块预测的结构，要么4个子宏块都是子宏块的预测结构- coded_block_pattern 简称CBP，用来反映该宏块编码中残差情况的语法元素。CBP共有6位，其中前面2位代表UV分量，描述如下表所示；后面4位是Y分量，分别代表宏块内的4个8x8子宏块，如果任意一位为0，表明对应的8x8块中所有变换系数level（transform coefficient levels 也就是对像素残差进行变换、量化后的矩阵内的值，以后统称level）全部都是0，否则表明对应的8x8块中的变换系数level不全为0。另外需要注意的是，如果当前宏块的预测模式是Intra_16x16，则不会存在这个元素，此时CBP会由mb_type来表示，请参考。CBP的主要作用是加快解码速度，当一个块的残差都为0时，就不用对这个块进行残差解码了。| CodedBlockPatternChroma | Description 

Description
| 0 | All chroma transform coefficient levels are equal to 0. 

All chroma transform coefficient levels are equal to 0.
| 1 | One or more chroma DC transform coefficient levels shall be non-zero valued. All chroma AC transform coefficient levels are equal to 0. 

One or more chroma DC transform coefficient levels shall be non-zero valued.
| 2 | Zero or more chroma DC transform coefficient levels are non-zero valued. One or more chroma AC transform coefficient levels shall be non-zero valued. 

Zero or more chroma DC transform coefficient levels are non-zero valued.
- mb_qp_delta 用来计算当前宏块的QP，QP=pic_init_qp_minus26 + 26 + slice_qp_delta + mb_qp_delta- residual 像素残差编码的语法结构。
按照macroblock_layer的语法结构上看，宏块能粗略分成三种结构：PCM、sub_mb_pred（子宏块预测）、mb_pred（宏块预测）。另外，虽然skip宏块并不在macroblock内描述，它也是宏块的一种结构。

### 5.4、mb_perd 语法

<img alt="" height="917" src="https://i-blog.csdnimg.cn/blog_migrate/666fe78cf1ce73d7497d22b66ccf37d4.png" width="702">
- prev_intra4x4_pred_mode_flag 如果当前宏块采用的是intra4x4的预测方式，则会存在这个语法元素，它的含义请参考- rem_intra4x4_pred_mode 如果当前宏块采用的是intra4x4的预测方式，则可能会存在这个语法元素，它的含义请参考- prev_intra8x8_pred_mode_flag 如果当前宏块采用的是intra8x8的预测方式，则会存在这个语法元素，它的含义请参考- rem_intra8x8_pred_mode 如果当前宏块采用的是intra8x8的预测方式，则可能会存在这个语法元素，它的含义请参考- intra_chroma_pred_mode intra chroma的预测模式，只有当前宏块的Luma部分采用intra预测时才会存在这个语法元素，它的含义请参考- ref_idx_l0 前向参考图像索引。如果当前宏块为inter预测，并且他的预测方式并非后向预测（即可能为前向预测或双向预测），则会存在这个语法元素- ref_idx_l1 后向参考图像索引。如果当前宏块为inter预测，并且他的预测方式并非前向预测（即可能为后向预测或双向预测），则会存在这个语法元素- mvd_l0 前向向量残差。如果当前宏块为inter预测，并且他的预测方式并非后向预测（即可能为前向预测或双向预测），则会存在这个语法元素- mvd_l1 后向向量残差。如果当前宏块为inter预测，并且他的预测方式并非前向预测（即可能为后向预测或双向预测），则会存在这个语法元素
下图分别是几个mb_pred结构的例子
- 在intra16x16的宏块模式下，intra16x16的宏块信息是被包含在mb_type里面的，因此mb_pred结构内只有chroma相关的信息- 在intra8x8的宏块模式下，共有四个子宏块，因此分成4个部分- 在intra4x4的宏块模式下，共有16个4x4块，因此分成16部分- 如果是Pslice的inter宏块，并且宏块采用16x8的分割方式，那么宏块会被分割成两部分，因此会有两个refIdx以及两个mvd- 如果是Bslice的inter宏块，并且宏块采用16x16的分割方式，那么宏块不会被分割，如果这个没被宏块采用的是双向预测方式，那么会有前、后向的refIdx以及mvd- 如果是Bslice的inter宏块，并且宏块采用8x16的分割方式，那么宏块会被分割成两部分，如果第一部分采用的是前向预测方式，第二部分采用的是双向预测方式，那么mb_pred内会有两个前向、一个后向refIdx以及mvd
<img alt="" height="701" src="https://i-blog.csdnimg.cn/blog_migrate/c26c3c01cd36cafb24602d8a2ded80b9.png" width="857">

### 5.5、sub_mb_pred 语法

<img alt="" height="727" src="https://i-blog.csdnimg.cn/blog_migrate/1e679c81bb391bb2e4e258d4ff4ad280.png" width="717">
- sub_mb_type 子宏块模式，子宏块大小为8x8，因此一个宏块内有4个子宏块，也就会有4种子宏块模式，具体请参考- ref_idx_l0- ref_idx_l1 描述同mb_pred，不过需要注意的一点是，由于在8x8的子宏块中，分块（2个8x4块，4个4x4块等）是共用参考图像的，也就是说整个宏块最多也就只包含四个ref_idx- mvd_l0- mvd_l1 描述同mb_pred
下面是一个sub_mb_pred语法结构的例子。假设处于Bslice，左边的表格分别代表四个子宏块的模式。在该sub_mb_pred结构中
- 头部保存的是4个子宏块各自的子宏块类型- 接下来是前向refIdx，第一个子宏块的预测方式为Bi，因此有前向refIdx；第二个子宏块的预测方式为L0，也有前向refIdx；第三个子宏块为直接预测，没有refIdx；第四个子宏块为L0,有前向refIdx- 然后是后向refIdx，只有第一个子宏块的Bi会包含后向refIdx- 然后是前向mvd，第一个子宏块分割方式为4x8，分割成两个部分，因此有两个前向mvd；第二个子宏块分割方式为8x8，即不分割，因此只有一个前向mvd；第三个子宏块为直接预测，没有mvd；第四个子宏块分割方式为8x4，分割成两个部分，因此有两个前向mvd- 最后是后向mvd，例子中只有第一个子宏块，也就是采用Bi预测的会有后向mvd，由于第一个子宏块被分割成两部分，因此有两个后向mvd
图例中，结构上面的数字代表了该语法元素所属的子宏块。

<img alt="" height="380" src="https://i-blog.csdnimg.cn/blog_migrate/3b805b120f18ebc31b6fc569485f22ad.png" width="579">

### 5.6、残差语法 - residual

<img alt="" height="884" src="https://i-blog.csdnimg.cn/blog_migrate/ae69dcdb68d3eacaffaf7f93f9bdfd2b.png" width="700">

<img alt="" height="170" src="https://i-blog.csdnimg.cn/blog_migrate/8ffc4662da489ab5a65635ca58feb09a.png" width="700">

residual内部首先会根据entropy_coding_mode_flag来选择CAVLC或者CABAC的熵编码方式，然后在下面进行level的处理。level处理部分先包含了residual_luma，也就是先进行luma level的处理，然后用residual_block对chroma level进行处理。

chroma level一般采用的yuv格式都是4:2:0，也就是ChromaArrayType=1。

### 5.7、残差语法 - residual_luma

<img alt="" height="810" src="https://i-blog.csdnimg.cn/blog_migrate/202b9e314a24bccc1c546b36842a9dee.png" width="704">
<li>residual_luma 亮度残差变换量化后的语法结构，各参数说明如下 
  <ul>- i16x16DClevel 如果是intra16x16的宏块模式，会分开AC与DC单独编码，DC level会从residual_block内取出，并存在i16x16DClevel数组内- i16x16AClevel 如果是intra16x16的宏块模式，会分开AC与DC单独编码，AC level会从residual_block内取出，并存在i16x16AClevel数组内- level4x4 不是intra16x16的情况下，如果DCT变换采用的是4x4的方式，宏块的level会从residual_block内取出，并存在level4x4数组内- level8x8 不是intra16x16的情况下，如果DCT变换采用的是8x8的方式，宏块的level会从residual_block内取出，并存在level8x8数组内- startIdx 需要进行熵编码的数组起始位置的索引- endIdx 需要进行熵编码的数组结束位置的索引- residual_block 这并不是完整的熵编码，而是熵编码参数的语法结构，以后分析熵编码再进行分析
luma level分为几种，如上面的数组i16x16DClevel, i16x16AClevel, level4x4, level8x8，在解码过程中，这些数组后续会被用于逆量化、逆变换，residual_luma的目的是从residual_block内取出level，并填充到这些数组当中。

我们来完整分析一下residual_luma的工作过程
- 如果当前宏块是Intra_16x16的预测模式，并且为亮度残差语法结构的开头，那么会从residual_block中获取16个DC level，存储到i16x16DClevel数组内<li>接下来会以子宏块为单位进行，一个宏块内有4个8x8大小的子宏块 
  <ul><li>如果当前宏块是以4x4块为单位进行DCT变换的（transform_size_8x8_flag=0），或者如果要求当前视频使用CAVLC进行熵编码（entropy_coding_mode_flag=0），这意味着熵编码是以4x4块为单位进行的。一个子宏块内包含4个4x4个子块。 
    <ul><li>在当前4x4块内level不全为0的情况下（CBP相应位为1），才需要从residual_block中获取level。 
      <ul>- 如果当前的宏块为Intra_16x16的预测方式，需要从residual_block中获取15个AC level，存储到i16x16AClevel中- 否则，则会从residual_block中获取16个level，存储到level4x4中- 否则（CBP相应位为0），如果当前的宏块为Intra_16x16的预测方式，它的AC level全为0，为i16x16AClevel中的15个元素赋值0- 否则（CBP相应位为0），意味着该4x4块内的level全为0，就为level4x4中的16个元素赋值0- 如果当前视频使用CAVLC进行熵编码（entropy_coding_mode_flag=0），但是当前宏块是以8x8块为单位进行DCT变换的（transform_size_8x8_flag=1），我们则需要把这些CAVLC解码得到的4x4块组合成8x8块，以便后续使用- 否则（要求当前视频使用CABAC进行熵编码（entropy_coding_mode_flag=1）并且当前宏块是以8x8为单位进行DCT变换（transform_size_8x8_flag=1），如果该8x8块内的level不全为0（CBP相应位为1），那么就从residual_block中获取64个level，并存储到level8x8中）- 否则（要求当前视频使用CABAC进行熵编码（entropy_coding_mode_flag=1）并且当前宏块是以8x8为单位进行DCT变换（transform_size_8x8_flag=1），如果该8x8块内的level全为0（CBP相应位为0），就为level8x8中的64个元素赋值0.
如果没有宏块CBP上的bit全都不为0的话，它的residual就会是如下的样子

<img alt="" height="458" src="https://i-blog.csdnimg.cn/blog_migrate/94c833d17dec636a3131650655e626bc.png" width="582">

## 6、Slice、SPS、PPS 引用

<img alt="" height="870" src="https://i-blog.csdnimg.cn/blog_migrate/a3d4e5a9e7cf9d66f3ccf201f4e54921.png" width="755">

参考文献














