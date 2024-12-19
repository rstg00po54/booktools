#H.264 入门篇 - 08 (帧间预测 - 已解码参考帧的标记)
**目录**





















前置文章：







  

前面我们知道了，编码过程中，会将已编码的图像进行解码，然后放入到 DPB 缓存，用于后续的使用；放入到 DPB 

<img alt="" height="727" src="https://i-blog.csdnimg.cn/blog_migrate/579c86375a8265864b5a57d499b5a02e.png" width="1055">

## 0、已解码参考帧标记

当NALU中的nal_ref_idc值非0，即当前NALU所代表的图像会被作为参考帧的时候，会执行参考帧的标记过程；

参考帧标记的意义：由于当前帧会作为参考帧数据放入 DPB 中，当前 DPB 中已有的参考帧的性质可能会发生变化；短期参考帧可能会变为长期参考帧，或者某个参考帧可能会被标记为不再用做参考，因此需要对 DPB 中的参考帧数据进行重新标记

一个被标记为“用于短期参考”或“用于长期参考”的视频帧在解码过程中可以作为后续帧的参考数据，直到该参考帧被标记为“不再用作参考”为止；

将一个参考帧标记为“不再用作参考”的方法通常有两种：
- 滑动窗口法：通过一种“先进先出”机制进行的方法- 自适应内存控制法 (MMCO)；
在标准文档8.2.5.1节中，解码参考帧的标记执行过程：

1. 首先，确保当前帧的所有slice解码完成；

2. 随后，判断当前帧的帧类型。如果当前帧为一个IDR帧，则进行以下操作：

>  
 - 将所有的参考帧标记为“不作为参考”；- 如果long_term_reference_flag为0，则该IDR帧被标记为“作为短期参考”，且MaxLongTermFrameIdx设为“无长期参考帧索引”；- 如果long_term_reference_flag为1，则该IDR帧被标记为“作为长期参考”，其LongTermFrameIdx设为0，并且MaxLongTermFrameIdx设为0； 


3. 随后，判断当前帧的帧类型。如果当前帧为一个IDR帧，则进行以下操作：

>  
 - 如果adaptive_ref_pic_marking_mode_flag为1，则进行自适应内存控制法标记参考帧；- 如果adaptive_ref_pic_marking_mode_flag为0，则进行滑动窗口法标记参考帧； 


4. 的如果当前帧为非IDR帧，且没有因为 memory_management_control_operation 的值等于6而被标记为“用于长期参考”，则该帧被标记为“用于短期参考”。

## 1、滑动窗口法

滑动窗口法的执行过程：
1. 如果当前图像是一个 complementary reference field pair 中按照解码顺序的第二个场，且第一场被标记为“用作短期参考”，那么当前图像和该complementary reference field pair都被标记为“作为短期参考”。1. 否则的话，根据如下步骤执行：
>  
 - 设numShortTerm为作为短期参考的编码帧、编码场或互补场对的总数，numLongTerm为长期参考帧/场/场对的总数- 当numShortTerm与numLongTerm之和达到Max(max_num_ref_frames, 1)时，在满足numShortTerm大于0的前提下，FrameNumWrap值最小的那个作为短期参考的编码帧、编码场或互补场对将被标记为“不作为参考” 


>  
 在JM代码中有实现 


## 2、自适应内存控制法

从上一小节中可以看出，滑动窗口法的效果主要在于将过期的短期参考帧从DPB中移除出去，并不涉及到对长期参考帧的操作（除非遇到IDR时将DPB全部清空）。而自适应内存控制法的操作流程比滑动窗口法要复杂得多。

执行自适应内存控制法标记参考帧的条件是 adaptive_ref_pic_marking_mode_flag 为1，此时slice_header中会包含一些附加的语法元素信息 (dec_ref_pic_marking)：

<img alt="" height="660" src="https://i-blog.csdnimg.cn/blog_migrate/a23bbecc8245292f4bf4143d80690ad3.png" width="845">

从上图的dec_ref_pic_marking结构中可以看出，如果adaptive_ref_pic_marking_mode_flag的值为1，那么其中将会多出若干个值：
- memory_management_control_operation；- difference_of_pic_nums_minus1；- long_term_pic_num；- long_term_frame_idx；- max_long_term_frame_idx_plus1
其中，memory_management_control_operation 可以取的范围为1~6，分别代表了不同的操作。

### 2.1、mmco = 1

将短期参考帧标记为“不作为参考”

当 memory_management_control_operation = 1 时;

自适应内存控制过程会将某一个短期参考帧标记为“不作为参考”

体的执行过程为：

1. 首先计算picNumX。计算方法为：

>  
 picNumX = CurrPicNum − ( difference_of_pic_nums_minus1 + 1 ) 


其中，CurrPicNum为当前帧的frame_number，difference_of_pic_nums_minus1从dec_ref_pic_marking中解析得到。

2. 对于帧编码的图像，PicNum等于picNumX的短期参考帧会被标记为“不作为参考”；

### 2.2、mmco = 2

将长期参考帧标记为“不作为参考”

当memory_management_control_operation = 2时;

自适应内存控制过程会将某一个长期参考帧标记为“不作为参考”。具体的执行过程很简单，索引为LongTermPicNum等同于long_term_pic_num（是码流中解析出的）的长期参考帧将被标记为不作为参考。 标准文档：8.2.5.4.2

### 2.3、mmco = 3

将短期参考帧标记为“长期参考帧”

当memory_management_control_operation = 3时；

自适应内存控制过程会将某一个短期参考帧标记为“作为长期参考帧”。在这种情况下，码流中会同时包含difference_of_pic_nums_minus1以及long_term_frame_idx这两个值。执行过程如下：
1. 按照4.2.2.1中的方法计算picNumX;1. 如果long_term_frame_idx对应的长期参考帧存在，则该长期参考帧标记为“不作为参考”；1. 对于帧编码图像，由picNumX所代表的短期参考帧，将被标记为长期参考帧，并将对应的LongTermFrameIdx设为long_term_frame_idx。
### 2.4、mmco = 4

计算 MaxLongTermFrameIdx

当memory_management_control_operation = 4时；

执行计算MaxLongTermFrameIdx的操作。计算过程如下：
1. 如果码流中解析出的max_long_term_frame_idx_plus1的值为0，则MaxLongTermFrameIdx被设置为“无长期参考帧索引”；1. 否则，MaxLongTermFrameIdx的值设置为max_long_term_frame_idx_plus1-1。所有被标记为“用作长期参考”的LongTermFrameIdx大于了MaxLongTermFrameIdx的图像都会被标记为“不作为参考”。
### 2.5、mmco = 5

清空参考帧列表

当memory_management_control_operation = 5时；

执行清空参考帧列表操作。该过程会将所有参考帧标记为“不作为参考”并将MaxLongTermFrameIdx设置为“无长期参考帧索引”。

### 2.6、mmco = 6

将当前帧标记为长期参考帧

当memory_management_control_operation = 6时；

将当前帧标记为长期参考帧。在这种情况下，需从码流中解析出 long_term_frame_idx。执行过程如下：
- 如果long_term_frame_idx对应的长期参考帧存在，则该长期参考帧标记为“不作为参考”；- 将当前帧标记为“作为长期参考”，并将其LongTermFrameIdx设置为long_term_frame_idx；
在当前帧标记完成后，所有被标记为“作为参考帧”的帧、场和互补场对的数量综合不能超过Max( max_num_ref_frames, 1 )规定的值。
