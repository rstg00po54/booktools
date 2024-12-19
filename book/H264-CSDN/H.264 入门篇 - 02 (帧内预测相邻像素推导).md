#H.264 入门篇 - 02 (帧内预测相邻像素推导)
**目录**











前置文档：





帧内预测的时候，需要根据相邻像素宏块来预测当前块的像素值，以 Intra_4x4 为例，如下图所示，需要用到的13个相邻像素值，那么如何获取这13个像素值？

<img alt="" height="697" src="images/H.264 入门篇 - 02 (帧内预测相邻像素推导)/35df2cf538f2c0d3003702796fcf9a84.png" width="1004">

本文要主要说明如何获取帧内预测所用到的相邻像素。对应参考文档6.4.5-6.4.9小节内容。

获取相邻像素的流程如下：
- 找到当前块（可以为4x4、8x8、16x16大小）的左、上、右上、左上相邻块- 找到左、上、右上、左上相邻块所在宏块- 根据当前宏块以及相邻块所在宏块确定相邻像素
在此之前需要先知道宏块地址是否可用，如果宏块地址不可用，则在该宏块的相邻像素也都不可用。

## 0、宏块地址

宏块地址用 mbAddr 来表示，我们使用 Elecard 工具打开一段码流：

<img alt="" height="752" src="images/H.264 入门篇 - 02 (帧内预测相邻像素推导)/d68bf55580b04e9ff3c1081f0fd61497.png" width="1200">

可以看到它的宏块地址，我们选择第一个宏块，看到地址为 0，从上到下，从左到右，一次递增；

## 1、宏块地址可用性推导

每个宏块都有它的地址，如果当前处于解码阶段，并当前宏块标识为 CurrMbAddr，针对一个宏块地址 mbAddr 来说，当 mbAddr 出现如下情况，我们认为该宏块地址 mbAddr 不可用：
1. mbAddr1. mbAddr&gt;CurrMbAddr，也就是在当前解码宏块之后的宏块，后面的宏块还未解码，不可用做预测1. mbAddr和CurrMbAddr属于不同slice；
## 2、相邻宏块地址可用性推导

分为两种情况：
1. MbaffFlag=01. MBaffFlag=1
### 2.1 非 MBAFF 宏块（帧宏块或场宏块）

mbAddrA：表示当前宏块左侧宏块的地址和可用性状态。

mbAddrB：表示当前宏块上侧宏块的地址和可用性状态。

mbAddrC：表示当前宏块右上侧宏块的地址和可用性状态。

mbAddrD：表示当前宏块左上侧宏块的地址和可用性状态。

下图表示地址为 mbAddrA、mbAddrB、mbAddrC 和 mbAddrD 的宏块与地址为 CurrMbAddr 的当前宏块在空间上的相对位置。

<img alt="" height="234" src="images/H.264 入门篇 - 02 (帧内预测相邻像素推导)/5b82289631987576244993a5a519260c.png" width="299">

SPEC 6.4.5 节规定的过程的输入为 mbAddrA= CurrMbAddr – 1，输出为 mbAddrA 宏块是否可用。另外，当 CurrMbAddr % PicWidthInMbs 等于 0 时 mbAddrA 将被标识为不可用。

SPEC 6.4.5 节规定的过程的输入为 mbAddrB = CurrMbAddr – PicWidthInMbs，输出为 mbAddrB 是否可用。

SPEC 6.4.5 节规定的过程的输入为 mbAddrC = CurrMbAddr – PicWidthInMbs + 1，输出为 mbAddrC 是否可用。另外，当( CurrMbAddr + 1 ) % PicWidthInMbs 等于 0 时 mbAddrC 将被标识为不可用。

SPEC 6.4.5 节规定的过程的输入为 mbAddrD = CurrMbAddr – PicWidthInMbs – 1，输出为 mbAddrD 是否可用。另外，当 CurrMbAddr % PicWidthInMbs 等于 0 时 mbAddrD 将被标识为不可用
