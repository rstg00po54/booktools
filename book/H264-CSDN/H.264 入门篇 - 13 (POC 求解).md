#H.264 入门篇 - 13 (POC 求解)
**目录**































POC（picture order counts）用来表示解码帧显示顺序，当码流中存在B帧时，解码顺序和显示顺序不一样，视频帧显示时需要根据 POC 重排顺序，否则会出现跳帧、画面不连贯。

比如，对于IPBB这项顺序的视频序列，解码顺序为 I-P-B-B，但它的显示顺序为 I-B-B-P。

## 1、基本概念

对于H.264的码流，需要计算POC包括三种：coded frame（编码帧）, coded field（编码场）和complementary field pair（互补参考场对），每种类型的POC都由 TopFieldOrderCnt 和BottomFieldOrderCnt 这两个值的一个或两个组成：
1. 每一个编码帧的poc包含两个值TopFieldOrderCnt和BottomFieldOrderCnt；1. 每一个编码场的poc只包含一个值，如果该field为顶场则为TopFieldOrderCnt，如果是底场为BottomFieldOrderCnt；1. 对于每一个互补参考场对，POC包含两个值，顶场为TopFieldOrderCnt，底场为BottomFieldOrderCnt；
换句话来说，求解 POC 就是求解：**TopFieldOrderCnt** 和 **BottomFieldOrderCnt**

## 2、求解过程

POC计算过程依据标准文档中的 8.2.1；

求解 POC 参考 pic_order_cnt_type 的值，pic_order_cnt_type 被定义再 SPS 中；该值有三种可能：0、1、2，分别对应了 3 种不同的求解 POC 的方式；

### 2.1、pic_order_cnt_type=0

由于POC会随着帧数增多而逐渐增大，如果直接编码 POC，消耗的bit数回越来越大，因此，把POC分为低有效位（POCLsb）和高有效位（POCMsb）两部分。编码时只传输 POCLsb，而 POCMsb 由前面帧计算得到。

该过程

输入为：按解码顺序前一个参考图像的高有效位 prevPOCMsb；

输出为：当前picture的TopFiledPOC、BottomFieldPOC两者中的一个或两个。

#### 2.1.1、计算前一个按解码顺序参考帧的 POC 信息

prevPicOrderCntMsb和prevPicOrderCntLsb是当前帧按解码顺序前一帧的POC数据，其计算方式为：
- 如果当前图像为 IDR 帧，prevPicOrderCntMsb=prevPicOrderCntLsb=0；- 如果当前帧为非IDR帧，分三种情况：1. 前一个参考图像 mmco（memory_management_control_operation）=5，并且前一个参考图像不为底场，则prevPicOrderCntMsb=0；prevPicOrderCntLsb等于前一参考图像的TopfieldPOC；1. 前一个参考图像 mmco（memory_management_control_operation）=5，并且前一个参考图像是底场，则prevPicOrderCntMsb=prevPicOrderCntLsb=0；1. 前一个参考图像 mmco（memory_management_control_operation）不等于5，prevPicOrderCntMsb等于前一个参考图像的PicOrderCntMsb，prevPicOrderCntLsb等于前一个参考图像的pic_order_cnt_lsb。（pic_order_cnt_lsb从slice header解析得到）
#### 2.1.2、计算当前图像的 PicOrderCntMsb

PicOrderCntMsb是当前帧的POC的高有效位。在该过程中需要用到两个从码流中解析出的语法元素值：
- pic_order_cnt_lsb：从slice_header中解析；- MaxPicOrderCntLsb：由sps中的log2_max_pic_order_cnt_lsb_minus4计算得到；
获取到了上述数据之后，可依据标准文档中的公式8-3计算PicOrderCntMsb：

```
if( (pic_order_cnt_lsb &lt; prevPicOrderCntLsb) &amp;&amp; ( ( prevPicOrderCntLsb − pic_order_cnt_lsb ) &gt;= ( MaxPicOrderCntLsb / 2 ) ) )
        PicOrderCntMsb = prevPicOrderCntMsb + MaxPicOrderCntLsb (8-3)
else if( ( pic_order_cnt_lsb &gt; prevPicOrderCntLsb ) &amp;&amp;
 ( ( pic_order_cnt_lsb − prevPicOrderCntLsb ) &gt; ( MaxPicOrderCntLsb / 2 ) ) )
        PicOrderCntMsb = prevPicOrderCntMsb − MaxPicOrderCntLsb
else
        PicOrderCntMsb = prevPicOrderCntMsb 

```

#### 2.1.3、计算当前图像的TopFiledPOC和BottomFieldPOC
- 如果当前图像不是底场（顶场或帧格式），TopFieldOrderCnt 计算公式如下：
```
TopFieldOrderCnt = PicOrderCntMsb + pic_order_cnt_lsb
```
- 如果当前图像不是顶场，BottomFieldOrderCnt 计算公式如下，其中delta_pic_order_cnt_bottom和pic_order_cnt_lsb 都是从slice header中解析：
```
if( !field_pic_flag ) //帧格式
        BottomFieldOrderCnt = TopFieldOrderCnt + delta_pic_order_cnt_bottom
else // 场格式
        BottomFieldOrderCnt = PicOrderCntMsb + pic_order_cnt_lsb 

```

### 2.2、pic_order_cnt_type=1 (基于 frame_num 计算)

该过程的输入为：按解码顺序前一个图像的 FrameNumOffset，输出为：当前picture的TopFiledPOC、BottomFieldPOC两者中的一个或两个。

#### 2.2.1、计算FrameNumOffset

令prevFrameNum为前一个图像的frame_num；变量prevFrameNumOffset为前一图像的FrameNumOffset，如当前图像不是 IDR，而前一图像的 memory_management_control_operation 等于 5，prevFrameNumOffset 设为 0；否则，prevFrameNumOffset 设置等于前一图像的 FrameNumOffset。

FrameNumOffset计算方法如下：
- 若当前图像为IDR，则FrameNumOffset为0；- 若当前图像不是IDR，且prevFrameNum大于frame_num，则计算方式为：
```
FrameNumOffset = prevFrameNumOffset + MaxFrameNum
```
- 若当前图像不是IDR，且prevFrameNum小于frame_num，则FrameNumOffset的值即为prevFrameNumOffset；
```
if( IdrPicFlag = = 1 )
        FrameNumOffset = 0
else if( prevFrameNum &gt; frame_num ) 
         FrameNumOffset = prevFrameNumOffset + MaxFrameNum
else
         FrameNumOffset = prevFrameNumOffset 

```

#### 2.2.2、计算 absFrameNum

absFrameNum计算公式如下：

```
if( num_ref_frames_in_pic_order_cnt_cycle != 0 )
         absFrameNum = FrameNumOffset + frame_num
else 
         absFrameNum = 0
if( nal_ref_idc = = 0 &amp;&amp; absFrameNum &gt; 0 )
         absFrameNum = absFrameNum − 1 

```

如果absFrame&gt;0

```
picOrderCntCycleCnt = ( absFrameNum − 1 ) / num_ref_frames_in_pic_order_cnt_cycle
frameNumInPicOrderCntCycle = ( absFrameNum − 1 ) % num_ref_frames_in_pic_order_cnt_cycle 

```

#### 2.2.3、计算 expectedPicOrderCnt

```
if( absFrameNum &gt; 0 ){
         expectedPicOrderCnt = picOrderCntCycleCnt * ExpectedDeltaPerPicOrderCntCycle
        for( i = 0; i &lt;= frameNumInPicOrderCntCycle; i++ )
                expectedPicOrderCnt = expectedPicOrderCnt + offset_for_ref_frame[ i ]
} else
         expectedPicOrderCnt = 0
         
if( nal_ref_idc = = 0 ) 
         expectedPicOrderCnt = expectedPicOrderCnt + offset_for_non_ref_pic 

```

#### 2.2.4、计算TopFieldOrderCnt和BottomFieldOrderCnt

```
if( !field_pic_flag ) {
        TopFieldOrderCnt = expectedPicOrderCnt + delta_pic_order_cnt[ 0 ]
        BottomFieldOrderCnt = TopFieldOrderCnt +
        offset_for_top_to_bottom_field + delta_pic_order_cnt[ 1 ] 
} else if( !bottom_field_flag )
        TopFieldOrderCnt = expectedPicOrderCnt + delta_pic_order_cnt[ 0 ]
else
        BottomFieldOrderCnt = expectedPicOrderCnt + offset_for_top_to_bottom_field + delta_pic_order_cnt[ 0 ] 

```

### 2.3、pic_order_cnt_type=2

这种方式不能出现连续的非参考帧并且解码输出顺序和显示顺序一致，也就是不能出现B帧，但可以出现不做参考的P场。

pic_order_cnt_type为2时，FrameNumOffset和prevFrameNumOffset同模式1中的计算方法类似。

#### 2.3.1、计算tempPicOrderCnt

```
if( IdrPicFlag = = 1 )
         tempPicOrderCnt = 0
else if( nal_ref_idc = = 0 ) 
        tempPicOrderCnt = 2 * ( FrameNumOffset + frame_num ) − 1
else
         tempPicOrderCnt = 2 * ( FrameNumOffset + frame_num ) 

```

#### 2.3.2、计算 TopFieldOrderCnt 和 BottomFieldOrderCnt

```
if( !field_pic_flag ) {
        TopFieldOrderCnt = tempPicOrderCnt
        BottomFieldOrderCnt = tempPicOrderCnt (8-13)
} else if( bottom_field_flag )
        BottomFieldOrderCnt = tempPicOrderCnt
else
        TopFieldOrderCnt = tempPicOrderCnt 

```


