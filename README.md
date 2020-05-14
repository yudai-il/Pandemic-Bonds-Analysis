#### Pandemic-Bonds-Analysis（防疫债分析）
Some analysis based on Chinese pandemic Bonds（An new tool to mitigating Cash Crunch）

### Requirements:

1、分类统计不同类型的债券（参考字段 ：债券类型）✅<p>
2、所有债券的票面利率（分布图，最大，最小，平均），分类统计不同的类型的债券的票面利率，以及不同类型下债券的票面利率的（最大，最小，平均）（需要备注说明：有多少债券公布了票面利率✅<p>
3、发行的省份的统计（比如上海**，占比*%，能否做一个省市的地图，用热力图显示发行的情况），发行人行业的统计（比如金融**，占比*%，柱状图显示）✅<p>
4、募集资金用途（流动资金，疫情物质采购，营运资金等，使用算法工具区分出字段，并做热点统计）✅<p>
5、债券评级（有多少公布了评级，评级的分布统计情况）✅<p>

### Notes:
IB是银行间市场发行;
CP :同业存单/<p>
SCP: 超短期融资券/ <p>
PPN: 定向工具（私募券）/<p>
MTN: 中期票据（中票）ABN: 资产支持票据/<p>
SCP :超短期融债券是指具有法人资格、信用评级较高的非金融企业在银行间债券市场发行的，期限在270天以内的短期融资券。<p>
PPN :在银行间债券市场以非公开定向发行方式发行的债务融资工具称为非公开定向债务融资工具(PPN,private placement note)。<p>
MTN :英文Medium-term Notes的缩写。中期票据是指具有法人资格的非金融企业在银行间债券市场按照计划分期发行的,约定在一定期限还本付息的债务融资工具。


<hr/>

Visual Display with Pyecharts (以下仅展示部分，具体展示结果可参考<a href="https://github.com/yudai-il/Pandemic-Bonds-Analysis/blob/master/page.html">该页面</a>)

每日发行状况

<img src="https://github.com/yudai-il/Pandemic-Bonds-Analysis/blob/master/results/pic%20(5).png"/>

债券发行省份数量：

<img src="https://github.com/yudai-il/Pandemic-Bonds-Analysis/blob/master/results/pic%20(1).png"/>

债券发行行业统计：
<img src="https://github.com/yudai-il/Pandemic-Bonds-Analysis/blob/master/results/pic%20(2).png"/>


资金用途热点
### 使用LDA分析
<img src="https://github.com/yudai-il/Pandemic-Bonds-Analysis/blob/master/results/pic%20(3).png"/>


评级分析

<img src="https://github.com/yudai-il/Pandemic-Bonds-Analysis/blob/master/results/pic%20(4).png"/>


发行利率统计分析

<img src="https://github.com/yudai-il/Pandemic-Bonds-Analysis/blob/master/results/pic.png"/>








