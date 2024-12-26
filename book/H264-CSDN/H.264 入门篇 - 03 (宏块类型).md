#H.264 入门篇 - 03 (宏块类型)
**目录**





















前置文档：











H.264 标准中，编解码如下所示

<img alt="" height="733" src="images/H.264 入门篇 - 03 (宏块类型)/cfee7a2a14850b62c9bdd763702ee18b.png" width="1200">

在 Slice -&gt; RBSP -&gt; MacroBlock Layer 中，包含了一个 mb_type 这个字段：
<td colspan="2" rowspan="1"> slice_type 允许的宏块类型集合 </td>
| slice_type | 允许的宏块类型集合 

允许的宏块类型集合
| I (Slice) | I (参见表 7-11) (宏块类型) 

I (参见表 7-11) (宏块类型)
| P (Slice) | P (参见表 7-13) 和 I (参见表 7-11) (宏块类型) 

P (参见表 7-13) 和 I (参见表 7-11) (宏块类型)
| B (Slice) | B (参见表 7-14) 和 I (参见表 7-11) (宏块类型) 

B (参见表 7-14) 和 I (参见表 7-11) (宏块类型)
| SI (Slice) | SI (参见表 7-12) 和 I (参见表 7-11) (宏块类型) 

SI (参见表 7-12) 和 I (参见表 7-11) (宏块类型)
| SP (Slice) | P (参见表 7-13) 和 I (参见表 7-11) (宏块类型) 

P (参见表 7-13) 和 I (参见表 7-11) (宏块类型)

为节省编码码流，mb_type 包含了多个信息，比如该宏块的划分方式，子块预测方式，cbp 等；

## 1、宏块划分方式
- I 宏块支持 16x16、4个8x8块、16个4x4块划分方式；- P 宏块支持 16x16、2个16x8块、2个8x16块、4个8x8块（8x8块还需要再次划分）- B 宏块支持 16x16、2个16x8块、2个8x16块、4个8x8块（8x8块还需要再次划分）
## 2、宏块数据语法

<img alt="" height="910" src="images/H.264 入门篇 - 03 (宏块类型)/83cad5d4f66217b8da9fb472fba57832.png" width="705">

<img alt="" height="105" src="images/H.264 入门篇 - 03 (宏块类型)/5fbcabbc299a5e561a648a6d6176ff5d.png" width="703">

## 3、宏块类型 mb_type

mb_type 的查找法如下所示：

<img alt="" height="813" src="images/H.264 入门篇 - 03 (宏块类型)/4b92c2715534fb25576c780d512521dd.png" width="1200">

不同的 Slice type 下，同样的 mb_type 值，代表了不同的含义；

### 3.1、I Slice 的 mb_type

I Slice 的 mb_type 如下：
<td colspan="7" rowspan="1"> 表7-11－I Slice 的宏块类型 </td>
| mb_type | mb_type 的名称 | transform_size_8x8_flag | MbPartPredMode ( mb_type, 0 ) | Intra16x16PredMode | CodedBlockPatternChroma | CodedBlockPatternLuma 

mb_type 的名称

MbPartPredMode

Intra16x16PredMode

CodedBlockPatternLuma
| 0 | I_NxN | 0 | Intra_4x4 | na | 公式 7-33 | 公式 7-33 

I_NxN

Intra_4x4

公式 7-33
| 0 | I_NxN | 1 | Intra_8x8 | na | 公式 7-33 | 公式 7-33 

I_NxN

Intra_8x8

公式 7-33
| 1 | I_16x16_0_0_0 | na | Intra_16x16 | 0 | 0 | 0 

I_16x16_0_0_0

Intra_16x16

0
| 2 | I_16x16_1_0_0 | na | Intra_16x16 | 1 | 0 | 0 

I_16x16_1_0_0

Intra_16x16

0
| 3 | I_16x16_2_0_0 | na | Intra_16x16 | 2 | 0 | 0 

I_16x16_2_0_0

Intra_16x16

0
| 4 | I_16x16_3_0_0 | na | Intra_16x16 | 3 | 0 | 0 

I_16x16_3_0_0

Intra_16x16

0
| 5 | I_16x16_0_1_0 | na | Intra_16x16 | 0 | 1 | 0 

I_16x16_0_1_0

Intra_16x16

1
| 6 | I_16x16_1_1_0 | na | Intra_16x16 | 1 | 1 | 0 

I_16x16_1_1_0

Intra_16x16

1
| 7 | I_16x16_2_1_0 | na | Intra_16x16 | 2 | 1 | 0 

I_16x16_2_1_0

Intra_16x16

1
| 8 | I_16x16_3_1_0 | na | Intra_16x16 | 3 | 1 | 0 

I_16x16_3_1_0

Intra_16x16

1
| 9 | I_16x16_0_2_0 | na | Intra_16x16 | 0 | 2 | 0 

I_16x16_0_2_0

Intra_16x16

2
| 10 | I_16x16_1_2_0 | na | Intra_16x16 | 1 | 2 | 0 

I_16x16_1_2_0

Intra_16x16

2
| 11 | I_16x16_2_2_0 | na | Intra_16x16 | 2 | 2 | 0 

I_16x16_2_2_0

Intra_16x16

2
| 12 | I_16x16_3_2_0 | na | Intra_16x16 | 3 | 2 | 0 

I_16x16_3_2_0

Intra_16x16

2
| 13 | I_16x16_0_0_1 | na | Intra_16x16 | 0 | 0 | 15 

I_16x16_0_0_1

Intra_16x16

0
| 14 | I_16x16_1_0_1 | na | Intra_16x16 | 1 | 0 | 15 

I_16x16_1_0_1

Intra_16x16

0
| 15 | I_16x16_2_0_1 | na | Intra_16x16 | 2 | 0 | 15 

I_16x16_2_0_1

Intra_16x16

0
| 16 | I_16x16_3_0_1 | na | Intra_16x16 | 3 | 0 | 15 

I_16x16_3_0_1

Intra_16x16

0
| 17 | I_16x16_0_1_1 | na | Intra_16x16 | 0 | 1 | 15 

I_16x16_0_1_1

Intra_16x16

1
| 18 | I_16x16_1_1_1 | na | Intra_16x16 | 1 | 1 | 15 

I_16x16_1_1_1

Intra_16x16

1
| 19 | I_16x16_2_1_1 | na | Intra_16x16 | 2 | 1 | 15 

I_16x16_2_1_1

Intra_16x16

1
| 20 | I_16x16_3_1_1 | na | Intra_16x16 | 3 | 1 | 15 

I_16x16_3_1_1

Intra_16x16

1
| 21 | I_16x16_0_2_1 | na | Intra_16x16 | 0 | 2 | 15 

I_16x16_0_2_1

Intra_16x16

2
| 22 | I_16x16_1_2_1 | na | Intra_16x16 | 1 | 2 | 15 

I_16x16_1_2_1

Intra_16x16

2
| 23 | I_16x16_2_2_1 | na | Intra_16x16 | 2 | 2 | 15 

I_16x16_2_2_1

Intra_16x16

2
| 24 | I_16x16_3_2_1 | na | Intra_16x16 | 3 | 2 | 15 

I_16x16_3_2_1

Intra_16x16

2
| 25 | I_PCM | na | na | na | na | na 

I_PCM

na

na

其中：

**mb_type **宏块类型的数值，I slice共有 26个数值：

**name **宏块类型的名称，其中
- 名称开头的I表示 I 宏块类型- I_NxN 表示的是 I_8x8 或者 I_4x4；- I_16x16_a_b_c 中的 I_16x16 代表以 intra_16x16 为预测方式；- I_16x16_a_b_c 中的 a 代表 intra_16x16 当中的 4 种模式；- I_16x16_a_b_c 中的 b 代表使用 intra_16x16 预测方式时的 Chroma CBP；- I_16x16_a_b_c 中的 c 代表使用 intra_16x16 预测方式时的 Luma CBP；- I_PCM：把一个宏块共256个像素点的值不做任何处理，直接进行熵编码的模式，Chroma 也有PCM这个模式；
**transform_size_8x8_flag ：**表示该宏块是否使用8x8大小的DCT变换
- 1 表示，宏块划分为4个8x8块，采用 8x8 的块进行熵编码；- 0 表示，宏块划分为16个4x4块，采用 4x4 块进行熵编码，na 的情况同 0；
**MbPartPredMode(mb_type, 0) ：**

表明当前宏块类型所采用的 Intra 预测方式，关于 Intra 预测方式参考 

**Intra16x16PredMode **(代表了 16x16 mb 的 4 中预测模式)：

如果当前宏块类型采用的预测方式为 Intra_16x16，那么该字段有效，它用0~3表示了 Intra_16x16中的 4 种模式，请参考中的 Intra16x16 部分：
| Intra16x16PredMode | Name of Intra16x16PredMode 

Name of Intra16x16PredMode
| 0 | Intra_16x16_Vertical 

Intra_16x16_Vertical
| 1 | Intra_16x16_Horizontal 

Intra_16x16_Horizontal
| 2 | Intra_16x16_DC 

Intra_16x16_DC
| 3 | Intra_16x16_Plane 

Intra_16x16_Plane

**CodedBlockPatternChroma（CBP）**：

如果当前宏块类型采用的预测方式为 Intra_16x16，那么该字段有效，它用0~2表示了 Chroma 宏块中的 CBP，请参考中的 coded_block_pattern

<img alt="" height="197" src="images/H.264 入门篇 - 03 (宏块类型)/f66f062ce72e469eaab9e576076ffd1a.png" width="787">

**CBP** 用来反映该宏块编码中残差情况的语法元素；

**CodedBlockPatternLuma （CBP）** ：

如果当前宏块类型采用的预测方式为 Intra_16x16，那么该字段有效，它表示了Luma宏块中的CBP。从的 residual 部分，我们知道当预测模式为Intra_16x16时，宏块需要分开AC level与DC level进行熵编码。0：表示宏块内的16个4x4块中的AC level全部都为0，15：宏块内的16个4x4块中至少有一个块的 AC level不全为 0

公式 7-33：

CodedBlockPatternLuma = coded_block_pattern % 16

CodedBlockPatternChroma = coded_block_pattern / 16

当宏块为子宏块，即多个 4x4 或者 8x8 的时候，使用 9 种预测模式：
| IntraPredMode | Name of Intra4x4PredMode | Name of Intra8x8PredMode 

Name of Intra4x4PredMode
| 0 | Intra_4x4_Vertical | Intra_8x8_Vertical 

Intra_4x4_Vertical
| 1 | Intra_4x4_Horizontal | Intra_8x8_Horizontal 

Intra_4x4_Horizontal
| 2 | Intra_4x4_DC | Intra_8x8_DC 

Intra_4x4_DC
| 3 | Intra_4x4_Diagonal_Down_left | Intra_8x8_Diagonal_Down_left 

Intra_4x4_Diagonal_Down_left
| 4 | Intra_4x4_Diagonal_Down_right | Intra_8x8_Diagonal_Down_right 

Intra_4x4_Diagonal_Down_right
| 5 | Intra_4x4_Vertical_Right | Intra_8x8_Vertical_Right 

Intra_4x4_Vertical_Right
| 6 | Intra_4x4_Horizontal_Down | Intra_8x8_Horizontal_Down 

Intra_4x4_Horizontal_Down
| 7 | Intra_4x4_Vertical_Left | Intra_8x8_Vertical_Left 

Intra_4x4_Vertical_Left
| 8 | Intra_4x4_Horizontal_Up | Intra_8x8_Horizontal_Up 

Intra_4x4_Horizontal_Up

<img alt="" height="905" src="images/H.264 入门篇 - 03 (宏块类型)/5e1e289a70fa288eae6c5178ac5c43f8.png" width="1200">

### 3.2、P Slice 的 mb_type

P slice中包含了I宏块类型（I开头）与P宏块类型（P开头）。I宏块类型mb_type数值为5~30，见上面I宏块类型的表格，其序号为mb_type-5。P宏块类型为0~4，见下表
<td colspan="7" rowspan="1"> 表7-13－P和SP条带的值为0到4的宏块类型 </td>
| mb_type | mb_type 的名称 | NumMbPart ( mb_type ) | MbPartPredMode ( mb_type, 0 ) | MbPartPredMode ( mb_type, 1 ) | MbPartWidth ( mb_type ) | MbPartHeight ( mb_type ) 

mb_type 的名称

( mb_type )

( mb_type, 0 )

( mb_type, 1 )

( mb_type )

( mb_type )
| 0 | P_L0_16x16 | 1 | Pred_L0 | na | 16 | 16 

P_L0_16x16

Pred_L0

16
| 1 | P_L0_L0_16x8 | 2 | Pred_L0 | Pred_L0 | 16 | 8 

P_L0_L0_16x8

Pred_L0

16
| 2 | P_L0_L0_8x16 | 2 | Pred_L0 | Pred_L0 | 8 | 16 

P_L0_L0_8x16

Pred_L0

8
| 3 | P_8x8 | 4 | na | na | 8 | 8 

P_8x8

na

8
| 4 | P_8x8ref0 | 4 | na | na | 8 | 8 

P_8x8ref0

na

8
| 推测值 | P_Skip | 1 | Pred_L0 | na | 16 | 16 

P_Skip

Pred_L0

16

**mb_type **宏块类型的数值，P slice共有31个数值

**name **宏块类型的名称，其中
- 开头的P表示P宏块类型- 末尾的 M x N 代表宏块的分割方式- P_L0_16x16 表示宏块的分割方式为16x16，也就是不进行分割，那么它只有一个前向参考图像 L0；- P_L0_L0_16x8 表示宏块的的分割方式为 16x8，也就是宏块被分成俩个 16x8 的块，每个 16x8 的块都有一个前向参考图像 L0，即两个L0，按顺序写成 P_L0_L0_16x8- P_L0_L0_16x8 表示宏块的的分割方式为 8x16，也就是宏块被分成俩个 8x16 的块，每个 8x16 的块都有一个前向参考图像 L0，即两个 L0，按顺序写成 P_L0_L0_8x16- P_8x8 表示宏块分成 4 个 8x8 的子宏块，对每个子宏块会采用 sub_mb_type 来表明该子宏块的类型，下面一节会进行分析- P_8x8ref0 表示同上，不过该宏块的4个子宏块采用的参考图像都是ref0，在sub_mb_pred（请参考中的sub_mb_pred部分）语法结构中不会包含他们的refIdx- P_Skip 表示该宏块在码流中没有更多的数据了。请注意他的 mb_type 为 inferred，不过它并不在mb_type 中表示，而是在slice_data处就已经用skip_run或者skip_flag来表示，请参考中的slice_data部分
**NumMbPart(mb_type)** 宏块被分割成多少部分

**MbPartPredMode(mb_type,0)** 宏块分割后的第一部分的预测模式为前向预测，还是后向预测，还是双向预测，由于是 P slice，这里只能是前向预测 **Pred_L0**

**MbPartPredMode(mb_type,1)** 宏块分割后的第二部分的预测模式为前向预测，还是后向预测，还是双向预测，由于是 P slice，这里只能是前向预测 **Pred_L0**

**MbPartWidth(mb_type) **分割后的块的宽度

**MbPartHeight(mb_type) **分割后的块的高度

### 3.3、B Slice 的 mb_type

B slice中包含了I宏块类型（I开头）与B宏块类型（B开头）。I宏块类型mb_type数值为23~48，见上面I宏块类型的表格，其序号为mb_type-23。P宏块类型为0~22，见下表
<td colspan="7" rowspan="1"> 表7-14－B条带中值为0到22的宏块类型 </td>
| mb_type | mb_type 的名称 | NumMbPart ( mb_type ) | MbPartPredMode ( mb_type, 0 ) | MbPartPredMode ( mb_type, 1 ) | MbPartWidth ( mb_type ) | MbPartHeight ( mb_type ) 

mb_type 的名称

( mb_type )

( mb_type, 0 )

( mb_type, 1 )

( mb_type )

( mb_type )
| 0 | B_Direct_16x16 | na | Direct | Na | 8 | 8 

B_Direct_16x16

Direct

8
| 1 | B_L0_16x16 | 1 | Pred_L0 | Na | 16 | 16 

B_L0_16x16

Pred_L0

16
| 2 | B_L1_16x16 | 1 | Pred_L1 | Na | 16 | 16 

B_L1_16x16

Pred_L1

16
| 3 | B_Bi_16x16 | 1 | BiPred | Na | 16 | 16 

B_Bi_16x16

BiPred

16
| 4 | B_L0_L0_16x8 | 2 | Pred_L0 | Pred_L0 | 16 | 8 

B_L0_L0_16x8

Pred_L0

16
| 5 | B_L0_L0_8x16 | 2 | Pred_L0 | Pred_L0 | 8 | 16 

B_L0_L0_8x16

Pred_L0

8
| 6 | B_L1_L1_16x8 | 2 | Pred_L1 | Pred_L1 | 16 | 8 

B_L1_L1_16x8

Pred_L1

16
| 7 | B_L1_L1_8x16 | 2 | Pred_L1 | Pred_L1 | 8 | 16 

B_L1_L1_8x16

Pred_L1

8
| 8 | B_L0_L1_16x8 | 2 | Pred_L0 | Pred_L1 | 16 | 8 

B_L0_L1_16x8

Pred_L0

16
| 9 | B_L0_L1_8x16 | 2 | Pred_L0 | Pred_L1 | 8 | 16 

B_L0_L1_8x16

Pred_L0

8
| 10 | B_L1_L0_16x8 | 2 | Pred_L1 | Pred_L0 | 16 | 8 

B_L1_L0_16x8

Pred_L1

16
| 11 | B_L1_L0_8x16 | 2 | Pred_L1 | Pred_L0 | 8 | 16 

B_L1_L0_8x16

Pred_L1

8
| 12 | B_L0_Bi_16x8 | 2 | Pred_L0 | BiPred | 16 | 8 

B_L0_Bi_16x8

Pred_L0

16
| 13 | B_L0_Bi_8x16 | 2 | Pred_L0 | BiPred | 8 | 16 

B_L0_Bi_8x16

Pred_L0

8
| 14 | B_L1_Bi_16x8 | 2 | Pred_L1 | BiPred | 16 | 8 

B_L1_Bi_16x8

Pred_L1

16
| 15 | B_L1_Bi_8x16 | 2 | Pred_L1 | BiPred | 8 | 16 

B_L1_Bi_8x16

Pred_L1

8
| 16 | B_Bi_L0_16x8 | 2 | BiPred | Pred_L0 | 16 | 8 

B_Bi_L0_16x8

BiPred

16
| 17 | B_Bi_L0_8x16 | 2 | BiPred | Pred_L0 | 8 | 16 

B_Bi_L0_8x16

BiPred

8
| 18 | B_Bi_L1_16x8 | 2 | BiPred | Pred_L1 | 16 | 8 

B_Bi_L1_16x8

BiPred

16
| 19 | B_Bi_L1_8x16 | 2 | BiPred | Pred_L1 | 8 | 16 

B_Bi_L1_8x16

BiPred

8
| 20 | B_Bi_Bi_16x8 | 2 | BiPred | BiPred | 16 | 8 

B_Bi_Bi_16x8

BiPred

16
| 21 | B_Bi_Bi_8x16 | 2 | BiPred | BiPred | 8 | 16 

B_Bi_Bi_8x16

BiPred

8
| 22 | B_8x8 | 4 | na | na | 8 | 8 

B_8x8

na

8
| 推测值 | B_Skip | na | 直接值 | na | 8 | 8 

B_Skip

直接值

8

**mb_type** 宏块类型的数值；

**name **宏块类型的名称，其中
- 开头的B代表B宏块类型- 末尾的 mxn 代表宏块的分割方式- B_Direct_16x16 整个宏块都采用 Direct 的方式进行预测（请参考），不需要编码mvd 以及 refIdx ，在解码时重建宏块所用的 mv 与 refIdx 靠直接预测进行推导，只需要编码residual（请参考）- B_X0_mxn 当宏块的分割方式为16x16时，意味着宏块不需要进行分割，因此只需要用一个字段（L0:前向预测；L1:后向预测；Bi：双向预测）来表示当前宏块的预测类型- B_X0_X1_mxn 当前宏块的分割方式为16x8或者8x16时，意味着宏块会被分割成两部分，因此需要用两个字段来分别表示这两个部分的预测类型（如L0_Bi表示第一部分为前向预测，第二部分为双向预测）- B_8x8表示宏块分成4个8x8的子宏块，对每个子宏块会采用sub_mb_type来表明该子宏块的类型，下面一节会进行分析- B_Skip 表示该宏块在码流中没有更多的数据了。请注意他的 mb_type 为inferred，不过它并不在mb_type中表示，而是在slice_data处就已经用skip_run或者skip_flag来表示，请参考中的slice_data部分
**NumMbPart(mb_type)** 宏块被分割成多少部分

**MbPartPredMode(mb_type,0) **宏块分割后的第一部分的预测模式为前向预测，还是后向预测，还是双向预测

**MbPartPredMode(mb_type,1) **宏块分割后的第二部分的预测模式为前向预测，还是后向预测，还是双向预测

**MbPartWidth(mb_type)** 分割后的块的宽度

**MbPartHeight(mb_type)** 分割后的块的高度

## 4、子宏块类型 sub_mb_type

子宏块即 8x8 块，一个16x16的宏块分为4个子宏块，每个子宏块类型表示都是一个8x8块的分割、预测方式，因此，采用子宏块预测的宏块其语法结构中会有4个子宏块类型。在H.264码流结构中，子宏块类型在 sub_mb_pred 中用 sub_mb_type表示（请参考中的sub_mb_pred）。

sub_mb_type 也是与slice类型相关的，在 I slice中是没有子宏块类型的，因为I slice中只包含intra预测，而子宏块类型是inter预测中的部分。另外，数值相同的sub_mb_type在P slice与B slice中表示的是不同的类型。

### 4.1、P slice 的 sub_mb_type

P slice的子宏块类型只包含了以下P子宏块类型（P开头），数值为0~3，见下表
| sub_mb_type [mbPartIdx ] | name | NumSubMbPart ( sub_mb_type [mbPartIdx ] ) | SubMbPredMode ( sub_mb_type [mbPartIdx ] ) | SubMbPartWidth ( sub_mb_type [mbPartIdx ] ) | SubMbPartHeight ( sub_mb_type [mbPartIdx ] ) 

name

( sub_mb_type [mbPartIdx ] )

( sub_mb_type [mbPartIdx ] )

( sub_mb_type [mbPartIdx ] )

( sub_mb_type [mbPartIdx ] )
| inferred | na | na | na | na | na 

na

na

na
| 0 | P_L0_8x8 | 1 | Pred_L0 | 8 | 8 

P_L0_8x8

Pred_L0

8
| 1 | P_L0_8x4 | 2 | Pred_L0 | 8 | 4 

P_L0_8x4

Pred_L0

4
| 2 | P_L0_4x8 | 2 | Pred_L0 | 4 | 8 

P_L0_4x8

Pred_L0

8
| 3 | P_L0_4x4 | 4 | Pred_L0 | 4 | 4 

P_L0_4x4

Pred_L0

4

**sub_mb_type** 子宏块类型的值

**mbPartIdx** 由于一个宏块可以分割成4个子宏块，因此用这个符号来表示这四个子宏块

**name** 子宏块类型的名称，其中
- P表示为P子宏块类型- P_L0_mxn中的L0表示子宏块的预测方式- P_L0_mxn中的mxn表示子宏块的分割方式
**NumSubMbPart** 子宏块会被分割成多少部分

**SubMbPredMode **子宏块预测模式，由于是P slice，因此只能是前向预测Pred_L0

**SubMbPartWidth **分割后的块的宽度

**SubMbPartHeight** 分割后的块的高度

### 4.2、B slice 的 sub_mb_type

B slice的子宏块类型只包含了以下B子宏块类型（B开头），数值为0~12，见下表
| sub_mb_type [mbPartIdx ] | name | NumSubMbPart ( sub_mb_type [mbPartIdx ] ) | SubMbPredMode ( sub_mb_type [mbPartIdx ] ) | SubMbPartWidth ( sub_mb_type [mbPartIdx ] ) | SubMbPartHeight ( sub_mb_type [mbPartIdx ] ) 

name

( sub_mb_type [mbPartIdx ] )

( sub_mb_type [mbPartIdx ] )

( sub_mb_type [mbPartIdx ] )

( sub_mb_type [mbPartIdx ] )
| inferred | na | na | na | na | na 

na

na

na
| 0 | B_Direct_8x8 | 4 | Direct | 4 | 4 

B_Direct_8x8

Direct

4
| 1 | B_L0_8x8 | 1 | Pred_L0 | 8 | 8 

B_L0_8x8

Pred_L0

8
| 2 | B_L1_8x8 | 1 | Pred_L1 | 8 | 8 

B_L1_8x8

Pred_L1

8
| 3 | B_Bi_8x8 | 1 | BiPred | 8 | 8 

B_Bi_8x8

BiPred

8
| 4 | B_L0_8x4 | 2 | Pred_L0 | 8 | 4 

B_L0_8x4

Pred_L0

4
| 5 | B_L0_4x8 | 2 | Pred_L0 | 4 | 8 

B_L0_4x8

Pred_L0

8
| 6 | B_L1_8x4 | 2 | Pred_L1 | 8 | 4 

B_L1_8x4

Pred_L1

4
| 7 | B_L1_4x8 | 2 | Pred_L1 | 4 | 8 

B_L1_4x8

Pred_L1

8
| 8 | B_Bi_8x4 | 2 | BiPred | 8 | 4 

B_Bi_8x4

BiPred

4
| 9 | B_Bi_4x8 | 2 | BiPred | 4 | 8 

B_Bi_4x8

BiPred

8
| 10 | B_L0_4x4 | 4 | Pred_L0 | 4 | 4 

B_L0_4x4

Pred_L0

4
| 11 | B_L1_4x4 | 4 | Pred_L1 | 4 | 4 

B_L1_4x4

Pred_L1

4
| 12 | B_Bi_4x4 | 4 | BiPred | 4 | 4 

B_Bi_4x4

BiPred

4

**sub_mb_type **子宏块类型的值；

**mbPartIdx** 由于一个宏块可以分割成4个子宏块，因此用这个符号来表示这四个子宏块；

**name **子宏块类型的名称，其中
- B表示为B子宏块类型；- B_X0_mxn中的X0表示子宏块的预测模式，由于参考图像索引refIdx是以8x8块为单位的，因此一个子宏块中的所有子块共用参考图像索引（请参考中的sub_mb_pred部分），也就是说整个子宏块的预测模式只能是是前向预测Pred_L0、后向预测Pred_L1、双向预测BiPred中的某一种；- B_X0_mxn中的mxn表示子宏块的分割方式；
**NumSubMbPart **子宏块会被分割成多少部分；

**SubMbPredMode **子宏块预测模式，由于是B slice，因此预测模式相比P slice的前向预测Pred_L0增加了后向预测Pred_L1以及双向预测BiPred中；

**SubMbPartWidth **分割后的块的宽度；

**SubMbPartHeight **分割后的块的高度；



 参考文档：
