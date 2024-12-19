#H.264 入门篇 - 00 (简介)
**目录**







































参考资料：

>  
  


SPEC:

>  
  (最新版本) 
  (2005 版本，带中文) 


H.264 的多媒体视频 Codec 规范由 ITU-T 和 ISO/IEC联合开发；

ITU-T 给这个标准命名为 H.264（以前叫做H.26L），而ISO/IEC 称它为 MPEG-4 高级视频编码（Advanced Video Coding，AVC）,并且它将成为MPEG-4标准的第10部分。



## 1、Profiles

H.264 有 4 种 Profile：
<li>Baseline Profile(BP) ：基本画质。 
  <ul>- 支持I/P帧，只支持无交错（Progressive）和 CAVLC- 提供I/P/B帧，支持无交错（Progressive）和交错（Interlaced），也支持CAVLC和CABAC的支持- 支持I/P/B/SP/SI帧，只支持无交错（Progressive）和CAVLC；- 在Main Profile基础上增加了8×8内部预测、自定义量化、无损视频编码和更多的YUV格式
## 2、应用领域

Baseline Profile 主要是用于可视电话，会议电视，无线通讯等实时通信。要实时，就要减少视频decode和display的时延，所以没有 B frame；为了提高针对网络丢包的容错能力，特意添加了FMO，ASO和冗余 slice；

Main Profile 多应用于流媒体领域，数字视频存储，有了CABAC，MBAFF，Interlace，B frame等。

Extended Profile 用于改进误码性能和码流切换（SP和SI slice），侧重于码流切换（SI，SP slice）和error resilience（数据分割）

High Profile 主要用于高压缩效率和质量， 引入8x8 DCT，选择量化矩阵等。

<img alt="" height="968" src="https://i-blog.csdnimg.cn/blog_migrate/a90ee257a2cc0705e208cdde99204fff.png" width="690">

一段码流的 profile 信息，会被编码到码流的 SPS (Sequence Paramater Set) 中的 profile_idc 字段 (详见 T-REC-H.264 的官方文档的 Annex A – Profiles and levels )：

>  
 Baseline -- profile_idc = 66 or constraint_set0_flag = 1 
 Constrain baseline -- profile_idc = 66 &amp;&amp; constraint_set1_flag = 1 
 Main profile -- profile_idc = 77 or constraint_set1_flag = 1 
 Extend profile -- profile_idc = 88 or constraint_set2_flag = 1 
 High profile -- profile_idc = 100 
 High 10 -- profile_idc = 110 
 High 422 -- profile_idc = 122 
 High 444 -- profile_idc = 244 


## 3、Level

H.264 的 Level 指示编码的分辨率、比特率、宏块数和帧率等。具体如下图：

<img alt="" height="970" src="https://i-blog.csdnimg.cn/blog_migrate/e67cb871019e82a620c736493f72e907.png" width="664">

一段码流的 level 信息，会被编码到码流的 SPS (Sequence Paramater Set) 中的 level_idc 字段 (详见 T-REC-H.264 的官方文档的 Annex A – Profiles and levels )：

码流所遵从的level由 level_idc 指定。

## 4、层次结构

H.264 编码过程分为了 Video Coding Layer (VCL) 和 Network Abstraction Layer (NAL)；VCL 负责将输入的流进行编码，NAL 负责将编码完毕的内容打包成符合 H.264 格式数据流；

解码过程是编码的逆过程，按照 H.264 的协议来解析 NAL，得到相关的编码信息，按照编码信息进行对应的解码策略；

编码过程

### 4.0、整个过程

下图展示了编码的整个过程：

<img alt="" height="649" src="https://i-blog.csdnimg.cn/blog_migrate/2e7309addfa4673f9b4b8ef71b44139e.png" width="1063">

这个编码过程，包含了帧内预测 (Intra-frame) 和帧间预测 (Motion)，这里有一个开关 (Intra/Inter MB select)，用于确定当前是帧内还是帧间处理；

也包含了变换和量化的过程，最后将数据给到熵编码；

下面会拆解整个流程，分段进行描述；

<img alt="" height="803" src="https://i-blog.csdnimg.cn/blog_migrate/1e5136c6543c51809762fa1469f44e5a.png" width="1200">

### 4.1、数据切分

每帧数据可以分为 1 个或者多个 Slice；

每个 Slice 分为多个 Macroblock；

每个 Macroblock 还可以分为子 Block；

<img alt="" height="748" src="https://i-blog.csdnimg.cn/blog_migrate/d073e0a947e7152e825952ef9bee6fbc.png" width="1091">

#### 4.1.1、Macroblock (宏块)

H.264 使用基础的 16x16 Macroblock；除了 16x16，还可以细分为如下类型宏块；

<img alt="" height="462" src="https://i-blog.csdnimg.cn/blog_migrate/b589e2535a59dbae41c61d5624f2a389.png" width="1093">

每个分割的或者子宏块，都有独立的运动向量 (MV)，并且需要被编码和传输；

使用 Elecard StreamEye Tools 工具抓取 H.264 的 P 帧，进行 Macroblock 分析如下所示：

<img alt="" height="817" src="https://i-blog.csdnimg.cn/blog_migrate/3011885fdba5d4e9177146c4303c3397.png" width="1001">

### 4.2、帧内预测 (Intra-Frame Prediction)

一个 GOP 的第一帧一定是 I 帧，虽然 I 帧是 “完整” 的帧，其实我们也不能完全真的让他完整，要对其进行帧内预测编码，对关键帧进行压缩；

H.264的帧内压缩与JPEG很相似。一幅图像被划分好 Macroblock 后，对每个 Macroblock 可以进行多达 9 种模式的预测。找出与原图最接近的一种预测模式。

帧内预测编码就是用周围邻近的像素值来预测当前的像素值，然后对预测误差进行编码。帧内预测是基于图像块；

对于亮度分量（Luma），块的大小，可以在16×16和4×4之间选择，16×16块有4种预测模式（垂直Vertical，水平Horizontal，直流分量DC，平面Plane），4×4块有9种预测模式（直流分量DC，8个方向）。

对于色度分量（Chroma），预测是对整个8×8块进行的，有4种预测模式（垂直Vertical，水平Horizontal，直流分量DC，平面Plane）。除了DC预测外，其他每种预测模式对应不同方向上的预测
- 16×16大小的亮度块：4种预测模式- 4×4大小的亮度块：9种预测模式- 8×8 色度块：4种预测模式，同16×16的亮度块
16×16亮度块和色度块的4种预测模式如下图：

<img alt="" height="312" src="https://i-blog.csdnimg.cn/blog_migrate/5212be21a33a5a00e90e98716234b41f.png" width="578">

4×4亮度块的9种预测模式如下图表示：

<img alt="" height="697" src="https://i-blog.csdnimg.cn/blog_migrate/07f20b7c0d0d3e6c99b1231d146e5846.png" width="1004">

>  
 DC 模式用上方和左方相邻像素的均值表示整个预测块 


帧内预测后，与真实图像比较如下：

<img alt="" height="428" src="https://i-blog.csdnimg.cn/blog_migrate/d5f563ad8e35480049336a98ad6b9593.png" width="753">

此刻，我们得到了基于 Macroblock 的预测方式 (预测向量)，我们再用预测的图像与真实的图像做残差：

<img alt="" height="243" src="https://i-blog.csdnimg.cn/blog_migrate/95b269dcc0ece2e4595f92048c09ce1e.png" width="473">

再将我们之前得到的预测模式信息一起保存起来，这样我们就可以在解码时恢复原图了；

<img alt="" height="339" src="https://i-blog.csdnimg.cn/blog_migrate/845609761a01414c48c395a10e04c72a.png" width="604">

过程如下：

<img alt="" height="584" src="https://i-blog.csdnimg.cn/blog_migrate/2adc97412f691592d2abaff9a92c7595.png" width="417">

### 4.3、帧间预测 (Inter-Frame Prediction)

H.264 帧间预测是利用**先前编码帧的重建图像**作为参考，对当前图像进行预测编码的一种方式。它把参考图像的抽样点通过运动矢量的补偿，作为当前图像抽样值的参考值；

H.264/AVC帧间预测的区别在于块尺寸更丰富，采用了1/4精度运动矢量、多参考帧等方法。

<img alt="" height="302" src="https://i-blog.csdnimg.cn/blog_migrate/3269f8b2bc89614ba2117e82194e085c.png" width="608">

通过宏块扫描与宏块搜索可以发现这两个帧的关联度是非常高的。进而发现这一组帧的关联度都是非常高的。因此，上面这几帧就可以划分为一组。其算法是：在相邻几幅图像画面中，一般有差别的像素只有10%以内的点,亮度差值变化不超过2%，而色度差值的变化只有1%以内，我们认为这样的图可以分到一组。

在这样一组帧中，经过编码后，我们只保留第一帖的完整数据，其它帧都通过参考上一帧计算出来。我们称第一帧为 I帧，其它帧我们称为P／B帧，这样编码后的数据帧组我们称为GOP。

**运动估计 (Motion Estimation) 与运动补偿 (Motion Compensation)**

在帧间编码中，活动的图像邻近帧之间存在一定的相关性，可以将活动的图像分为若干宏块，设法搜索出每个宏块在邻近帧之间的位置，并得出两者之间空间位置的相对偏移量，得到的偏移量叫做运动矢量 (Motion Vector)，得到运动矢量的过程叫运动估计；

帧间预测使用的宏块类型如下：

<img alt="" height="462" src="https://i-blog.csdnimg.cn/blog_migrate/279fbee40d4d8e61442f415df7df3dc5.png" width="1093">

**每个分割或子宏块都有一个独立的运动补偿。每个运动矢量都须被编码、传输，分割的选择也要将编码压缩到比特流中。**

对于较大的分割尺寸，运动矢量的选择和分割的选择只需少量的比特，但运动补偿残差较多。

小尺寸的分割可以减少运动补偿后的残差，但是需要传输较多的运动矢量和分割的选择。

因而，大尺寸分割适合于较平坦的区域，小尺寸分割适合较多细节区域。宏块的色度成分（Cr, Cb）为相应亮度的一半，采用和亮度相同的分割模式，只是尺寸减半

在H264编码器中将帧分组后，就要计算帧组内物体的运动矢量了。还以上面运动的台球视频帧为例，我们来看一下它是如何计算运动矢量的。

H264将两帧视频数据进行宏块扫描。当发现其中一幅图片中有物体时，就在另一幅图的邻近位置（搜索窗口中）进行搜索。如果此时在另一幅图中找到该物体，那么就可以计算出物体的运动矢量了。下面这幅图就是搜索后的台球移动的位置。

<img alt="" height="305" src="https://i-blog.csdnimg.cn/blog_migrate/5348b53df3a90283e8c69426ff0a9ffe.png" width="403">

通过上图中台球位置相差，就可以计算出台图运行的方向和距离。H264依次把每一帧中球移动的距离和方向都记录下来就成了下面的样子

<img alt="" height="337" src="https://i-blog.csdnimg.cn/blog_migrate/cd7f80b572197637fb0815afff6ddf98.png" width="636">

运动矢量计算出来后，将相同部分（也就是绿色部分）减去，就得到了**补偿数据**。我们最终只需要将补偿数据进行压缩保存，以后在解码时 (加上运动矢量) 就可以恢复原图了。压缩补偿后的数据只需要记录很少的一点数据。如下所示：

<img alt="" height="367" src="https://i-blog.csdnimg.cn/blog_migrate/e36657d7243610b8c8f6b2590c056417.png" width="612">

注意：帧间预测是利用先前编码帧的重建图像作为参考，对当前图像进行预测编码

### 4.4、变换 (Transform -&gt; DCT)

帧内预测我们得到了：残差数据 + 预测方向；

帧间预测我们得到了：残差数据 (运动补偿数据) + 运动矢量；

接下来对残差数据做变换；

H.264/AVC中的宏块大小为16×16，对其中每个4×4大小的块进行4×4的整数DCT变换后，得到16个4×4的变换矩阵。为了进一步提高压缩效率，该协议还允许把每个4×4的变换矩阵中的直流分量DC，单独取出组成一个新的4×4矩阵，对此矩阵进行Hadamard变换。整数DCT避免了以往标准中的编解码不匹配问题，使得反变换不会出现失衡的问题。并且其运算只包含加减和移位，且将量化融合在其中，有效的降低了运算量。H.264/AVC编码中整数变换及量化过程如图6-9所示。宏块的数据传送顺序如图6-10所示，图中上方的-1、16、17为直流分量形成的4×4、2×2块。

<img alt="" height="689" src="https://i-blog.csdnimg.cn/blog_migrate/783808a5ad569bfdda8f5c7c80d8a75c.png" width="1160">

### 4.5、量化 (Quantization)

量化过程在不降低视觉效果的前提下减少图像的编码长度，减少图像信息中视觉恢复中不必要的信息。

量化结果，实际上是由量化步长决定的 （QStep），量化步长越小，图像的细节信息保留的越多，码率越高，图像质量越高。反之，量化步长值越大，图像质量越差。

量化是有损压缩，这一步的图像质量有一定的损失。但是前提是不影响正常的视觉和图像质量。

q(x, y) = round(F(x, y) / Q + 0.5);

<img alt="" height="255" src="https://i-blog.csdnimg.cn/blog_migrate/6c48b9b88102d9c125dfa19ab496e8df.png" width="572">

再经过锯齿扫描 zig-zag（之字扫描）

<img alt="" height="416" src="https://i-blog.csdnimg.cn/blog_migrate/e204fd53ceb9b9395a19478979099da2.png" width="429">

将二维数组转换成一维数组，例如上面量化后数据，可以以9、0、-1、0、-1、0、0、0、0、0、0、0、0、0、0、0形式保存在一维数组里面。下面就可以 将这些数据进行熵编码，继续压缩了。

FFmpeg 的标志，就来源于这个 zig-zag 扫描；

<img alt="" height="170" src="https://i-blog.csdnimg.cn/blog_migrate/fb6890dd7e183856ca7c7c824ea08e0e.png" width="283">

### 4.6、熵编码 (entropy coding)

H.264/AVC协议对于图像数据或残差提供了两种熵编码的方式，分别为基于上下文自适应变长码CAVLC（Context-based Adaptive Variable Length Coding）和基于上下文自适应二进制算术编码CABAC（Context-based Adaptive Binary Arithmetic Coding）；如果不是预测残差，而是运动向量等其他数据，H.264/AVC则采用Exp-Golomb码或CABAC编码，视编码器的设置而定。

#### 4.6.1、CAVLC

变长编码VLC的基本思想就是对出现频率大的符号使用较短的码字，而出现频率小的符号采用较长的码字，这样可以使得平均码长最小。CAVLC中，H.264/AVC采用若干VLC码表，不同的码表对应不同的概率模型。编码器能够根据上下文，在这些码表中自动地选择如周围块的非零系数或系数的绝对值大小。最大可能地与当前数据的概率模型匹配，从而实现了上下文自适应的功能。

#### 4.6.2、CABAC

算术编码是一种高效的熵编码方案，其每个符号所对应的码长被认为是分数。由于对每一个符号的编码都与以前编码的结果有关，所以它考虑的是信源符号序列整体的概率特性，而不是单个符号的概率特性，因而它能够更大程度地逼近信源的极限香浓熵，降低码率。为了绕开算术编码中无限精度小数的表示问题，对信源符号概率进行估计，现代的算术编码多以有限状态机的方式实现，H.264/AVC的CABAC便是一个例子，其他的例子还有JPEG2000。在CABAC中，每编码一个二进制符号，编码器就会自动调整对信源概率模型（用一个“状态”来表示）的估计，随后的二进制符号就在这个更新了的概率模型基础上进行编码。这样的编码器不需要信源统计特性的先验知识，而是在编码过程中自适应地进行估计。显然，与CAVLC编码中预先设定好若干概率模型的方法比较起来，CABAC有更大的灵活性，可以获得更好的编码性能——大约降低10%的码率。

### 4.7、去块滤波 (Deblocking filter)

去块滤波，也叫环路滤波，它的作用是，消除经反量化和反变换后，**重建图像**中由于预测误差产生的块效应，即块边缘处的像素值跳变，从而一来改善图像的主观质量，二来减少预测误差。

<img alt="" height="669" src="https://i-blog.csdnimg.cn/blog_migrate/e3f026eeb6c472a5462b4fe6eb9d6e74.png" width="1144">

H.264/AVC中的 Deblocking Filter还能够根据图像内容做出判断，只对由于块效应产生的像素值跳变进行平滑，而对图像中物体边缘处的像素值不连续给予保留，以免造成边缘模糊。与以往的Deblocking Filter不同的是，经过滤波后的图像将根据需要放在缓存中用于帧间预测，而不是仅仅在输出重建图像时用来改善主观质量，也就是说该滤波器位于解码环中，而非解码环的输出外，因而它又称作环路滤波 Loop Filter。需要注意的是，对于帧内预测，使用的是未经过滤波的重建图像。

<img alt="" height="658" src="https://i-blog.csdnimg.cn/blog_migrate/23788e84de287a48fec094dc62412605.png" width="1162">

<img alt="" height="600" src="https://i-blog.csdnimg.cn/blog_migrate/29ae87eec3111da10ed53405f2bd270b.png" width="1079">

### 4.8、其他

#### 4.8.1、多参考帧的帧间预测

以往的P帧编码是以前面重建的帧作为参考，进行运动估计预测得到最佳匹配块。B帧编码同样是以前后重建帧为参考预测得到残差。H.264/AVC提供了多个参考帧的帧间预测模式，使估计到的宏块更贴近实际运动物体模型，运动向量表示更精确。但在选用多帧参考的同时，计算量巨增；

<img alt="" height="563" src="https://i-blog.csdnimg.cn/blog_migrate/c516f95d9df360784580ad13964776cc.png" width="855">

## 5、开源软件

H.264是一种视频压缩标准，其只规定了符合标准的码流的格式，以及码流中各个语法元素的解析方法。H.264标准并未规定编码器的实现或流程，这给了不同的厂商或组织在编码实现方面极大的自由度，并产生了一些比较著名的开源H.264编解码器工程。其中H.264编码器中最著名的两个当属JM和X264，这二者都属于H.264编码标准的一种实现形式。

>  
 JM:JM通常被认为是H.264标准制定团队所认可的官方参考软件，基本实现了H.264标准的全部特征。JM在运行时的运算过程较为复杂，而且没有采用汇编优化等加速方法，因此运行速度较慢，很难达到实时编解码。通常主要用于编解码技术的科学研究领域，目前（2016.7）最新版本为JM 19。 
 X264:X264是另一个著名的H.264开源视频编码器，由开源组织VideoLan开发制定。X264是目前企业界应用最为广泛的开源编码器，主要因为X264相对于JM进行了大量的优化与简化，使其运行效率大幅提高，主要有对编码代价计算方法的简化以及添加了MMX、SSE汇编优化等部分。虽然编码的质量在某些情况下相对于JM略有下降，但是已无法掩盖其在可应用性，尤其是实时编码方面无可比拟的优势。 
 JM的源代码的下载地址为：。 


除了上面描述的内容，FFmpeg 也是最流行的音视频开源软件，众多的播放器都曾使用 FFmpeg 作为他们的实现使用；

总览：

<img alt="" height="1200" src="https://i-blog.csdnimg.cn/blog_migrate/36a787e6882101df9c901bc092730e0d.png" width="1200">

 
