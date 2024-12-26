#H.264 入门篇 - 09 (帧间预测 - 参考帧列表)
**目录**





















前置文章：













## 0、前言

H.264 支持多参考帧，对于 P 帧最少参考 1 帧，B 帧最少参考 2 帧；

在 H.264 编解码的过程中，一帧图像编码完毕后，经过解码后，会经过 DPB 缓存起来，但是是否作为帧间参考的参考帧，还不一定，这里就会维护一个 DPB 中的一个参考帧列表；

<img alt="" height="710" src="https://i-blog.csdnimg.cn/blog_migrate/3ea6b20a16d3ca9e0a2714a564e9c546.png" width="982">
- 某一帧图像在解码完成后，可能会被保存于参考帧列表中；- 参考帧列表中的图像作为帧间编码的参考数据；<li>对 P 帧和 B 帧，参考帧列表有所不同； 
  <ul>- P 帧对应一个参考帧列表；- B 帧对应两个参考帧列表；- 参考帧列表中的数据在某条件下可进行修改；
## 1、frame_num 和 POC

由于 H.264 中存在 B 帧编码，所以视频的编码顺序和显示顺序可能会不一样；
- frame_num：表示解码顺序- POC：表示显示顺序（picture_order_count）
### 1.1、frame_num
- 代表视频的解码顺序：也就是编码器将每帧的图像压缩编码后写入到输出文件的顺序，同时也是解码时送入解码器的顺序- 对于一个给定的，已经生成好的视频文件而言，解码顺序一般是固定的，不会轻易改变的，否则可能造成解码和播放的错误或画面的无法显示等问题- frame_num 保存于每一个 slice_header 结构中- 在一个GOP中，第一个slice即作为随机接入点的 IDR slice，其frame_num值为0，表示当前slice是一个GOP的起点- 对于非IDR帧，GOP中的其他slice按照相应距离IDR的顺序按1递增- 当另一个语法元素gaps_in_frame_num_value_allowed存在时，slice可以以大于1的值递增，此时缺失的frame_num值需要解码器用空slice数据进行填充
### 1.2、显示顺序标志值 picture_order_count (POC)
- 是用于表示视频帧显示顺序的值- 视频中IDR的第一个field作为POC的开始，其值为0- 对于H.264的码流，有三种结构会被赋予POC的值：coded frame（编码帧）, coded field（编码场）和 complementary field pair（互补参考场对）- POC 都由 TopFieldOrderCnt 和 BottomFieldOrderCnt 这两个值的一个或两个组成1. 对于每一个编码帧，POC 包含两个值 TopFieldOrderCnt 和 BottomFieldOrderCnt；1. 对于每一个编码场，POC 包含一个值，如果该field为顶场则为 TopFieldOrderCnt，如果是底场为 BottomFieldOrderCnt；1. 对于每一个互补参考场对，POC 包含两个值，对顶场为 TopFieldOrderCnt，对底场为 BottomFieldOrderCnt；
在H.264中，TopFieldOrderCnt和BottomFieldOrderCnt共定义了3种解析方法，由 sps 中的值pic_order_cnt_type 决定；具体的计算方法参考 POC (分为 pic_order_cnt_type 的值等于0、1、2的情况 )

## 2、图像管理

当H.264作为参考帧的某一帧解码完成后，该帧的数据将会保存在解码图像缓存区中(DPB)

每一个参考帧将按照相应的规则标记为短期或长期参考帧

<img alt="" height="322" src="https://i-blog.csdnimg.cn/blog_migrate/875c180aa6a62bde29f98c2c39efdd0a.png" width="1125">

短期和长期的关系和区别：在一个解码器中的 DPB（参考帧缓存）大小总是有限的，所以引入一个问题，什么样的参考帧会被保存到 DPB 中，什么样的参考帧会被移除出去，因此将分为长期和短期参考帧，所谓短期参考帧是这帧不会长期驻留在DPB中，如果参考帧缓存已满或者有其他特定的条件，那么短期参考帧就会被从DPB中移除；与之相对的长期参考帧，只要没有遇到某个指定的条件，遇到某个IDR帧， 遇到了清空整个DPB的指令等等，那么长期参考帧会长期在DPB中，不会因为有新的参考帧而被冲刷掉；

短期参考帧由上文中提到的 frame_num 标记，长期参考帧由另一个值 LongTermPicNum 标记

## 3、图像排序

### 3.1、计算图像序号

参考图像分为：
- **短期参考图像**（short-term reference）；- **长期参考图像**（long-term reference）；
在某一个时间点上，参考图像只能是这两种的其中一种（非短即长）。参考图像列表分为两个部分：短期参考部分，长期参考部分。短期参考部分排在列表前头，长期排在后面。

参考帧列表的初始化、更新，参考帧的标记，以及处理非连续的frame_num时，需要计算参考帧的图像序号

主要数据：
- 短期：FrameNum, FrameNumWrap, PicNum- 长期：LongTermFrameIdx 和 LongTermPicNum
对于一个短期参考帧，计算FrameNum和FrameNumWrap。当前帧的FrameNum和FrameNumWrap计算方法为：
- 首先设FrameNum的值为对应的短期参考帧的frame_num的值；- 如果FrameNum的值大于当前帧slice_header中解析出的frame_num值，则FrameNumWrap的计算方式为：
>  
 FrameNumWrap = FrameNum - MaxFrameNum 

- 否则，FrameNumWrap 的计算方式为：
>  
 FrameNumWrap = FrameNum 


对于一个长期参考帧，计算其LongTermFrameIdx的值。

最后，对于每一个短期参考帧图像，计算 PicNum；

对于一个长期参考帧图像，计算 LongTermPicNum。

如果当前帧为帧编码，即field_pic_flag为0，则二者的值分别与FrameNumWrap和LongTermPicNum相等：

>  
 PicNum = FrameNumWrap 
 LongTermPicNum = LongTermFrameIdx 

- 短期参考帧按照PicNum进行索引- 长期参考帧按照LongTermFrameIdx索引
通过这两个索引值可以在参考帧列表中获取对应的参考帧图像。

### 3.1、P 帧排序

一般来说，距离当前图像最近的参考图像会被当前图像用作最多的参考，距离越远则参考得越少，短期参考图像列表就是依据这种规律来进行排序的。
- 在P帧的参考帧列表 RefPicList0 中，短期参考帧排列在长期参考帧的前面，即短期参考帧的索引值均小于长期参考帧的索引。- 排列短期参考帧：按照PicNum的顺序降序排列，即从PicNum最高的帧开始，一直到PicNum最低的帧为止。- 排列长期参考帧：短期参考帧相反，是按照LongTermPicNum升序排列，即从LongTermPicNum最低的帧开始，一直到LongTermPicNum最高的帧为止。
举例如下，假设DPB最大容量为8，其中包含了5个短期参考帧和3个长期参考帧，那么P帧解码时的参考帧列表可用下图表示：

<img alt="" height="526" src="https://i-blog.csdnimg.cn/blog_migrate/9a9f6bce733787798f9ad5a27babcd85.png" width="1200">

### 3.2、B 帧排序

初始化B帧参考帧列表的过程与P/SP稍有不同，主要体现在参考帧的排列顺序上

在两个参考帧列表RefPicList0和RefPicList1中，短期参考帧的顺序按照显示顺序，即POC进行排列。（P帧是按照编码顺序）

在排列短期参考帧时，会将当前帧的POC与DPB中参考帧的POC进行比较，然后根据结果进行以下操作：
<li>对参考帧列表 refPicList0： 
  <ul>- 如果DPB中短期参考帧的POC小于当前帧的POC，则短期参考帧按照POC的降序排列在参考帧列表refPicList0的前部，其余短期参考帧按照POC的升序紧随其后排列；- DPB中的长期参考帧按照LongTermPicNum递增的顺序在短期参考帧之后排列；- 如果DPB中短期参考帧的POC大于当前帧的POC，则短期参考帧按照POC的升序排列在参考帧列表refPicList1的前部，其余短期参考帧按照POC的降序紧随其后排列；- DPB中的长期参考帧按照LongTermPicNum递增的顺序在短期参考帧之后排列；- 若refPicList1包含多于1个参考帧，且refPicList1与refPicList0等同时，refPicList1中前两个参考帧refPicList1[0]和refPicList1[1]将进行交换。
<img alt="" height="790" src="https://i-blog.csdnimg.cn/blog_migrate/f914f1ba9c177d9a43a75e72cf490966.png" width="1200">


