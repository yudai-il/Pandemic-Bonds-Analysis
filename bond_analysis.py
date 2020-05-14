import pandas as pd
import numpy as np
import jieba
import jieba.posseg as pseg

jieba.enable_paddle()
import jieba.analyse

import seaborn as sns

import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

def raw_data_process(data,rate_columns_names = "票面利率(发行时)\r\n[单位] %"):
    bonds_data = data.copy()
    bonds_data.set_index("证券代码", inplace=True)
    bonds_data.dropna(how="all", inplace=True)

    bonds_data['票面利率(%)'] = bonds_data[rate_columns_names].replace("--", np.nan).astype(np.float)
    return bonds_data


def coupon_rate_summary(bonds_data,group_name = "债券类型"):
    g = bonds_data.groupby(group_name)['票面利率(%)']
    effective_counts = g.apply(lambda x: sum(~(x.isna()))).rename("公开数量")
    total_counts = g.apply(lambda x: len(x)).rename("总数")
    _ = g.apply(lambda x: pd.Series([x.min(), x.max(), x.mean()])).unstack().rename(
        columns={0: "最小值", 1: "最大值", 2: "平均值"})
    stats = pd.concat([total_counts, effective_counts, _], axis=1)
    _ = pd.Series({"最小值": stats['最小值'].min(), "最大值": stats['最大值'].max(), "平均值": bonds_data['票面利率(%)'].mean()})
    _ = pd.concat([_, stats[['总数', '公开数量']].sum()]).rename("总计")
    stats.loc['总计'] = _
    stats['占比'] = (((stats['总数']/_['总数'])*100).round(2)).astype(str)+"%"
    return stats[['总数','占比','公开数量','最小值','最大值','平均值']]


def category_analysis(bonds_data, category_name,counts = True):
    if counts:
        quantity = bonds_data.groupby(category_name).apply(len).rename('数量')
    else:
        quantity = bonds_data.groupby(category_name).apply(lambda x:x["发行总额\r\n[单位] 亿元"].sum()).rename("金额(亿)")
    percentage = (quantity / quantity.sum()).rename("占比")
    return pd.concat([quantity, percentage], axis=1)




def province_data_format(province_analysis):
    province_analysis.index = province_analysis.index.str.replace("省", "").str.replace("市", "").str.replace("特别行政区", "").str.replace(
        "广西壮族自治区", "广西").str.replace("西藏自治区", '西藏').str.replace("宁夏回族自治区", "宁夏").str.replace("新疆维吾尔自治区", '新疆').str.replace("内蒙古自治区",
                                                                                                           '内蒙古')
    province = ['北京', '天津', '河北', '山西', '内蒙古', '辽宁', '吉林', '黑龙江', '上海', '江苏', '浙江',
                '安徽', '福建', '江西', '山东', '河南', '湖北', '湖南', '广东', '广西', '海南', '重庆', '四川',
                '贵州', '云南', '西藏', '陕西', '甘肃', '青海', '宁夏', '新疆', '台湾', '香港', '澳门','南海诸岛']
    # province_analysis = province_analysis.reindex(province_analysis.index.union(province)).fillna(0)
    return province_analysis


def usage_analysis(bonds_data):

    jieba.load_userdict("Bonds/pendemic_bonds/dict")
    jieba.analyse.set_stop_words("Bonds/pendemic_bonds/stop_lists")

    usage = bonds_data['募集资金用途'].dropna()

    sentence = "。".join([_ for _ in usage])

    return jieba.analyse.textrank(sentence, 200, withWeight=True)

    # jieba.analyse.extract_tags(sentence, topK=200, withWeight=True, allowPOS=('n','v','nv'))
    #
    # jieba.analyse.textrank(sentence, topK=20, withFlag=True, withWeight=True, allowPOS=("vn"))


def rank(bonds_data,rank_names = "最终评级",pay_off_order = ["普通","A1","次级"]):
    _bonds_data = bonds_data[bonds_data['偿付顺序'].isin(pay_off_order)]

    ranks = _bonds_data[rank_names].dropna()
    _ = ranks.groupby(ranks).apply(len)
    _["未公布评级"] = len(_bonds_data) - _.sum()
    _['已公布评级'] = len(_bonds_data) - _["未公布评级"]
    _["合计"] = len(_bonds_data)

    return _.rename("数量")



# mappings = {"IB":"银行间市场发行",
#             "SH":"",
#             "SZ":"",
#             "":""
#             }
# bonds_data.index.str.split(".").str[1]

# def coupon_rate_plot(bonds_data, bins=None, kde=False):
#     fig, ax = plt.subplots()
#     rate = bonds_data['票面利率(%)'].dropna()
#     if not kde:
#         rate.hist(bins=bins)
#     else:
#         sns.distplot(rate, bins=bins)
