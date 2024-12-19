#H.264 入门篇 - 05 (帧内预测)
**目录**



















































前置文档：











## 0、前言

宏块类型为 I 或者 SI 的时候，使用这个过程；

本过程的输入是去块效应滤波过程之前的重建样点值，以及对于 Intra_N×N 预测模式（其中 N×N 等于 4×4 或 8×8）下相邻宏块的 IntraNxNPredMode 值。

<img alt="" height="677" src="images/H.264 入门篇 - 05 (帧内预测)/453db13f1fd40a2ad4b0ffbecebbe838.png" width="1200">

## 1、帧内预测类型

帧内预测包含4种类型：
- 亮度4x4块Intra_4x4预测模式- 亮度8x8块Intra_8x8预测模式- 亮度16x16宏块Intra_16x16预测模式- 色度8x8块预测方式。
他们都需要在**相邻块**做**去块滤波 (De-blocking) 之前**进行帧内预测；

帧内预测的输入为：预测模式和相邻块像素值；

输出为当前块的预测值。

## 2、亮度 Intra_4x4 预测

当宏块预测模式为 Intra_4x4 使用该过程；

该模式下，16x16宏块中的亮度块，可分为16个4x4块，每个4x4块都使用Intra_4x4预测方式。其中16个4x4块的扫描顺序如下图：

<img alt="" height="239" src="images/H.264 入门篇 - 05 (帧内预测)/afa0d240a67d87e752768e43a74c73e0.png" width="474">

对于索引号 luma4x4BlkIdx 为 0-15 的 4x4 块，获得当前块的预测像素的过程如下：

1） 根据相邻块 Intra4x4PredMode 推导当前块 Intra4x4PredMode；

2） 根据 Intra4x4PredMode 和相邻块像素值，得到当前块预测像素值。

>  
 **luma4x4BlkIdx 的值，就是方块里面的标号；** 


### 2.1、当前块 Intra4x4PredMode 的推导过程

本过程的输入是 4x4 亮度块的索引 luma4x4BlkIdx 和先前（按照解码顺序）已经得到的相邻宏块的预测方式 Intra4x4PredMode (如果可用) 和 Intra8x8PredMode(如果可用)。 本过程的输出是变量 每个4x4块的Intra4x4PredMode[ luma4x4BlkIdx ]。

下表定义了 Intra4x4PredMode[ luma4x4BlkIdx ]的值和相应的名称。

<img alt="" height="470" src="images/H.264 入门篇 - 05 (帧内预测)/67c639b395763cf7eaaa38c67ded0d97.png" width="1184">

Intra4x4PredMode[ luma4x4BlkIdx ]的值为 0、1、2、3、4、5、6、7 和 8，这些值分别代表不同预测方向，如下图：

<img alt="" height="384" src="images/H.264 入门篇 - 05 (帧内预测)/8fa2764c1a4c069c5448452998bb6301.png" width="403">

Intra4x4PredMode[ luma4x4BlkIdx ] 由以下方式得到：

1） 以下任一条件满足则使用 DC 预测（Intra_4x4_DC），即 dcPredModePredictedFlag 设为 1
- 宏块mbAddrA（当前宏块左相邻宏块）不可用；- 宏块mbAddrB（当前宏块上相邻宏块）不可用；- 宏块mbAddrA可用，并且以帧间预测方式进行编码、constrained_intra_ pred_flag为1；- 宏块mbAddrB可用，并且以帧间预测方式进行编码、constrained_intra_ pred_flag为1；- 举个例子，I slice的第一个宏块必定使用DC预测，因为它的相邻块mbAddrA、mbAddrB都不可用。
否则 dcPredModePredictedFlag = 0 走如下流程；

2） 不满足上述条件，则通过相邻块预测模式预测当前块Intra4x4PredMode。已知以下信息：mbAddrA的预测模式、mbAddrB的预测模式、码流中读取的语法元素prev_intra4x4_pred_mode_flag。
- 从mbAddrA和mbAddrB的预测模式中选取较小的一个作为预先定义模式。- 判断码流中读取的标志位prev_intra4x4_pred_mode_flag，如果该标志位为1，则预先定义模式就是当前块的预测模式；- 如果标志位prev_intra4x4_pred_mode_flag为0，则根据码流中解析出的语法元素 rem_intra4x4_pred_mode判断。如果rem_intra4x4_pred_mode的值小于预定义模式的值则选用rem_intra4x4_pred_mode；如果大于等于预定义模式，则当前块的预测模式设为rem_intra4x4_pred_mode + 1。
伪代码如下：

```
predIntra4x4PredMode = Min( intraMxMPredModeA, intraMxMPredModeB )

if( prev_intra4x4_pred_mode_flag[ luma4x4BlkIdx ] )
    Intra4x4PredMode[ luma4x4BlkIdx ] = predIntra4x4PredMode
else
    if( rem_intra4x4_pred_mode[ luma4x4BlkIdx ] &lt; predIntra4x4PredMode )
        Intra4x4PredMode[ luma4x4BlkIdx ] = rem_intra4x4_pred_mode[ luma4x4BlkIdx ]
else
    Intra4x4PredMode[ luma4x4BlkIdx ] = rem_intra4x4_pred_mode[ luma4x4BlkIdx ] + 1

```

总结为：
- 如果不能获取相邻宏块的预测方式，则当前块的预测模式为DC预测；- 否则选择相邻块预测方式较小的一个作为当前的模式预测值；- 码流中指定了要不要使用这个预测值。如果用，那么这个预测值就是当前块的帧内预测模式；否则就从后续读取的预测模式中计算。
#### 2.1.1、预测模式获取情况

当 DC = 0，即不满足 DC 预测的时候，选取相邻块 mbAddrA（当前宏块左相邻宏块） 和 mbAddrB（当前宏块上相邻宏块）的时候，可能出现下面 3 种情况：

1、左与上的相邻块都在当前宏块，即此时当前宏块还未决定是采用 I_8x8 还是 I_4x4 或者其他的预测方式。那么当前块的相邻块A,B的预测模式就采用与这轮的宏块模式相同的方式的预测模式。如，当前正以I_8x8进行帧内预测，那 PredModeA = PredMode8x8A，PredModeB = PredMode8x8_B.

<img alt="" height="542" src="images/H.264 入门篇 - 05 (帧内预测)/9d50e630432be60a7e19b4962b96d51c.png" width="866">

2、左与上的宏块都位于相邻宏块，即当前块位于宏块的左上角。此时左与上块所在的宏块都已选定了所采用的帧内宏块预测方式，因此无论当前块是在哪轮的帧内预测上（I_4x4或I_8x8），都应采用相邻宏块的预测方式来作为当前块的相邻块的帧内预测模式，PredModeA = PredModeMacroBlockA，PredModeB = PredModeMacroBlockB.

<img alt="" height="719" src="images/H.264 入门篇 - 05 (帧内预测)/cfb9f308269b4fa12723f43166ca0edf.png" width="886">

3、左或上的其中一个块为相邻宏块，仅有一个（左或上）块位于当前宏块。这种情况下，位于其他宏块的相邻块采用其所在宏块的帧内预测模式，位于当前宏块的相邻块采用这一轮预测模式。PredModeA = PredMode4x4A，PredModeB = PredModeMacroblockB.

<img alt="" height="712" src="images/H.264 入门篇 - 05 (帧内预测)/4b548879a95fde24392822ccb06ea7e6.png" width="940">

最终：

**PredPredMode = Min(PredModeA, PredModeB)**

### 2.2、获取预测数据

Intra_4x4 预测需要用到的13个相邻像素值如下图所示：

<img alt="" height="160" src="images/H.264 入门篇 - 05 (帧内预测)/866750ef553e94107dfe8c8960f32621.png" width="298">

相邻像素如何获取可参考.

首先需要判断这13个像素值是否有效。当下列4个条件满足任意一个，那么该像素便被判定为无效，不能用于预测：
- 宏块mbAddrN不可获得；- 宏块mbAddrN为帧间预测模式，且标识位constrained_intra_pred_flag为1；- 宏块mbAddrN为SI类型，，且标识位constrained_intra_pred_flag为1，且当前宏块不是SI类型；- 块索引luma4x4BlkIdx为3或11时，EFGH4个像素值不可用；（如下图所示，当解码到第3个块时，4还未解码，所以块4中的预测像素值不能使用，也就是EFGH这4个像素值）。
<img alt="" height="253" src="images/H.264 入门篇 - 05 (帧内预测)/ebb88ba787d5c5b47fb5922b37340abf.png" width="251">

### 2.3、Intra4x4 预测

Intra4x4 预测根据相邻的13个像素值得到当前4x4块预测像素值。预测方式共有9种；

#### 2.3.1、Intra4x4_Vertical 预测模式

<img alt="" height="220" src="images/H.264 入门篇 - 05 (帧内预测)/c7d11007a868f7b9bed33454c640abdd.png" width="389">

#### 2.3.2、Intra4x4_Horizontal 预测模式

<img alt="" height="312" src="images/H.264 入门篇 - 05 (帧内预测)/522c58d5cdcf167462fc670b648fef0b.png" width="553">

#### 2.3.3、Intra4x4_DC 预测模式

<img alt="" height="267" src="images/H.264 入门篇 - 05 (帧内预测)/b9b076b79043e6efb22b27429a5174fe.png" width="467">

Dc数值为相邻像素值的均值：
1. A、B、C、D、I、J、K、L都存在时，dc为这8个像素值的均值；1. A、B、C、D不可用时，dc为I、J、K、L这4个像素的均值；1. I、J、K、L不可用时，dc为A、B、C、D这4个像素的均值；1. 当这8个像素都不可用时，dc为(1&lt;&lt;(bit_depth-1))
#### 2.3.4、Intra4x4_Diagonal_Down_left 预测模式

当A、B、C、D、E、F、G、H 8个像素存在时才能使用这种预测模式；
- 当(x,y)=(3,3)，即计算一个4×4像素块最右下方的像素p时：- pred4x4L[ x, y ] = ( p[ 6, −1 ] + 3 * p[ 7, −1 ] + 2 ) &gt;&gt; 2- 其他情况计算方式如下：- pred4x4L[ x, y ] = ( p[ x + y, −1 ] + 2 * p[ x + y + 1, −1 ] + p[ x + y + 2, −1 ] + 2 ) &gt;&gt; 2；
以像素点a为例，做一条左下方向成45°直线，会穿过预测像素点B，预测计算过程依赖A、B、C三个像素值，pred_a = (A+2B+C+2)/4

<img alt="" height="260" src="images/H.264 入门篇 - 05 (帧内预测)/a8888d3aec8d28657cbedf6b8066c947.png" width="465">

#### 2.3.5、Intra4x4_Diagonal_Down_right 预测模式

<img alt="" height="268" src="images/H.264 入门篇 - 05 (帧内预测)/62d58e4d1d9937e572d62fba64a3d923.png" width="468">

#### 2.3.6、Intra_4x4_Vertical_Right 预测模式

后面的几种预测方向不是45°整数倍，要分成两种情况分别计算。

以Intra_4x4_Vertical_Right为例，像素a、j的预测值为（A+Q+1）/2;

像素f、o的预测值为（Q+2A+B+2）/4

<img alt="" height="294" src="images/H.264 入门篇 - 05 (帧内预测)/c4178868747559d69f1d99d5b5b63e3b.png" width="527">

#### 2.3.7、Intra_4x4_Horizontal_Down 预测模式

<img alt="" height="259" src="images/H.264 入门篇 - 05 (帧内预测)/e1ee1d3f738bad70d970f9fab2d50d35.png" width="462">

#### 2.3.8、Intra_4x4_Vertical_Left 预测模式

<img alt="" height="273" src="images/H.264 入门篇 - 05 (帧内预测)/11d86ddf41229c9cddb88ab468bcf84e.png" width="474">

#### 2.3.9、Intra_4x4_Horizontal_Up 预测模式

<img alt="" height="262" src="images/H.264 入门篇 - 05 (帧内预测)/28d66a35914742e8e0ed88cdddad2cab.png" width="463">

## 3、亮度 Intra_8x8 预测

一个宏块种的16x16亮度分量可分为4个8x8亮度块，每个8x8块都是用Intra_8x8预测方式。其中4个8x8块的扫描顺序如下：

<img alt="" height="189" src="images/H.264 入门篇 - 05 (帧内预测)/ad2626412cfbb5c6799f4e7d3944c2af.png" width="193">

对于索引号luma8x8BlkIdx为0-3的8x8块，预测方式推导过程、预测像素计算过程与Intra4x4类似，在此不再赘述。获取8x8块预测像素值流程如下：

1） 根据相邻块Intra8x8PredMode推导当前块Intra8x8PredMode；

2） 确定预测过程使用的相邻块预测像素是否可用

3） 根据Intra8x8PredMode和相邻块预测像素值，得到当前块预测像素值。

## 4、亮度 Intra_16x16 预测

相比于Intra_4x4和Intra_8x8，Intra_16x16的区别主要有以下几点：

预测模式可以直接从mb_type得到，不需要通过相邻块预测；

预测模式只有4种

Intra_16x16需要33个参考像素点，分别为当前宏块左侧16个像素点，上方16个像素点以及左上方一个像素点。这些参考像素点是否可用的判断方式于Intra_4x4类似。

4种预测模式如下：

<img alt="" height="280" src="images/H.264 入门篇 - 05 (帧内预测)/72f9e026b5637d941f6452e8407b6295.png" width="798">

### 4.1、Intra_16x16_Vertical 预测模式

只有上方16个参考像素有效时才可以使用，计算方法为

predL[ x, y ] = p[ x, −1 ], x, y = 0…15

### 4.2、Intra_16x16_Horizontal 预测模式

只有左侧16个参考像素有效时才可以使用，计算方法为

predL[ x, y ] = p[ −1, y ], x, y = 0…15

### 4.3、Intra_16x16_DC 预测模式

16×16模式的DC预测模式同4×4模式的DC预测方法类似，判断左侧16个像素和上方16个像素的有效性，将其中有效部分的均值作为整个预测块的像素值。如果32个像素都无效，则预测块像素值为( 1

一般码流中第一个I slice的第一个宏块会使用Intra_16x16_DC预测模式，对于8bit像素，其宏块预测值为128.

### 4.4、Intra_16x16_Plane 预测模式

Intra_16x16_Plane模式要求33个像素值都存在时才能使用。计算方式如下：

predL[ x, y ] = Clip1Y( ( a + b * ( x − 7 ) + c * ( y − 7 ) + 16 ) &gt;&gt; 5 )，x，y = 0…15

其中，

a = 16 * ( p[−1, 15 ] + p[ 15, −1 ] )

b = ( 5 * H + 32 ) &gt;&gt; 6

c = ( 5 * V + 32 ) &gt;&gt; 6

## 5、色度8x8块预测

一个宏块包含两个8x8色度块，分别为cb分量和cr分量。这两个分量使用相同的预测方式，由mb header中的语法元素intra_chroma_pred_mode决定。

这4种预测模式与 Intra_16x16 类似，不再赘述。



参考


