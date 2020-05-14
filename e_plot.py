from pyecharts.commons.utils import JsCode
from pyecharts.charts import Grid, Bar, Map, Pie,Tab
from pyecharts.components import Table
from pyecharts.options import ComponentTitleOpts

import pyecharts.options as opts
from pyecharts.charts import WordCloud

import pandas as pd
import numpy as np
import jieba
import jieba.posseg as pseg

jieba.enable_paddle()
import jieba.analyse

import seaborn as sns
from Bonds.pendemic_bonds.bonds_analysis import *

import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

fig_height = "600px"
fig_width = "1250px"
pixel_ratio = 1


def issuer_industry_plot(data):
    name = data.columns[0]
    data = data.sort_values(by=name)
    x_data = data.index
    value = np.round(data[name],2).tolist()

    bar = (
        Bar()
            .add_xaxis(
            xaxis_data=x_data.tolist(),
        )
            .add_yaxis(
            series_name="",
            yaxis_data=value,
            yaxis_index=0,
            color="#36648B",
        )

            .set_global_opts(
            yaxis_opts=opts.AxisOpts(
                type_="value",
                name=name,
                position="left",
                # offset=80,
                axisline_opts=opts.AxisLineOpts(
                    linestyle_opts=opts.LineStyleOpts()
                ),
                axislabel_opts=opts.LabelOpts(formatter="{value}"),
            ),
            xaxis_opts=opts.AxisOpts(
                axislabel_opts=opts.LabelOpts(rotate=-90),
                type_="category",
                name="行业",
            ),
            tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
            title_opts=opts.TitleOpts(subtitle="数据来源：WIND"),
            toolbox_opts=opts.ToolboxOpts(is_show=True,
                                          feature=opts.ToolBoxFeatureOpts(
                                              save_as_image=opts.ToolBoxFeatureSaveAsImageOpts(
                                                  background_color='white',
                                                  connected_background_color="white",
                                                  pixel_ratio=pixel_ratio,
                                                  name="pic",
                                              ),
                                          )
                                          )
        )
    )

    pie = (Pie(init_opts=opts.InitOpts()).add(
        series_name="",
        data_pair=[list(z) for z in zip(x_data, (data['占比']*100).round(2).tolist())],
        radius=["25%", "35%"],
        center=["30%","35%"],
        label_opts=opts.LabelOpts(is_show=False),
    ).set_global_opts(legend_opts=opts.LegendOpts(is_show=False,pos_left="legft", orient="vertical")) \
        .set_series_opts(
        tooltip_opts=opts.TooltipOpts(
            trigger="item", formatter="{b}: {c}%"
        ),
        label_opts=opts.LabelOpts(formatter="{b}: {c}%"),
        toolbox_opts=opts.ToolboxOpts(is_show=True,
                                      feature=opts.ToolBoxFeatureOpts(
                                          save_as_image=opts.ToolBoxFeatureSaveAsImageOpts(
                                              background_color='white',
                                              connected_background_color="white",
                                              pixel_ratio=pixel_ratio,
                                              name="pic",
                                          ),
                                      )
                                      )
    ))

    grid_chart = (
        Grid(init_opts=opts.InitOpts(width=fig_width, height=fig_height))
        .add(
            bar,
            grid_opts=opts.GridOpts(
                pos_left="10%", pos_top="10%"
            ),
        )
        .add(pie, grid_opts=opts.GridOpts())



    )
    return grid_chart



def province_analysis_plot(data):
    def format_data(data):
        data['占比'] = (data['占比'] * 100).round(4)
        _ = data.reset_index().values
        data = list(zip([d[0] for d in _], _.tolist()))
        data = [list(d) for d in data]
        return data

    data = format_data(data)

    min_data, max_data = (
        min([d[1][1] for d in data]),
        max([d[1][1] for d in data]),
    )
    map_chart = (
        Map(init_opts=opts.InitOpts(
            width=fig_width, height=fig_height,
            page_title="中国各省疫情防控债发行情况"))
        .add(
            series_name="",
            data_pair=data,
            # label_opts=opts.LabelOpts(is_show=False,
            #                           # formatter="{b}:{@占比}"
            #                           ),
            is_map_symbol_show=False,
        ).set_series_opts(
            label_opts=opts.LabelOpts(is_show=True,
            formatter=JsCode("""
                       function(params){                                                                                                         
                            if (typeof(params.data) == 'undefined') {
                                return params.value[2];  
                            } else {          
                                return params.data.name + params.data.value[2] + '%' ;
                            }                                                                                                                 
                       }"""
             ))
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(
                # title="中国各省疫情防控债发行情况",
                subtitle="数据来源：WIND",
                pos_left="center",
                pos_top="top",
                title_textstyle_opts=opts.TextStyleOpts(
                    font_size=25, color="rgba(255,255,255, 0.9)"
                ),
            ),

            tooltip_opts=opts.TooltipOpts(
                is_show=True,
                formatter=JsCode(
                    """function(params) {
                    if ('value' in params.data) {
                        return params.data.value[0] + '<br/>占比：' + params.data.value[2]+'%<br/>数量：'+params.data.value[1];
                    }
                }"""
                ),
            ),
            visualmap_opts=opts.VisualMapOpts(
                is_calculable=True,
                dimension=1,
                pos_left="10",
                pos_top="center",
                range_text=["High", "Low"],
                range_color=["lightskyblue", "yellow", "orangered"],
                textstyle_opts=opts.TextStyleOpts(color="#ddd"),
                min_=min_data,
                max_=max_data,
            ),
            toolbox_opts=opts.ToolboxOpts(is_show=True,
                                          feature=opts.ToolBoxFeatureOpts(
                                              save_as_image=opts.ToolBoxFeatureSaveAsImageOpts(
                                                  background_color='white',
                                                  connected_background_color="white",
                                                  pixel_ratio=pixel_ratio,
                                                  name="pic",
                                              ),
                                          )
                                          )
        )
    )

    return map_chart




def rate_histogram_plot(data,bins = 10):
    m, bins = np.histogram(data.dropna(), bins)
    m = m.astype(float)
    s = m.sum()
    x = bins.round(2).astype(str).tolist() + [""]
    bar = (
        Bar(init_opts=opts.InitOpts(width=fig_width, height=fig_height))
            .add_xaxis(xaxis_data=bins.round(2).tolist(),
                       )
            .extend_axis(xaxis_data=x,

                         xaxis=opts.AxisOpts(
                             position="bottom",
                             is_show=True,
                             # ,
                             is_scale = True,
                             boundary_gap = False,
                             # type_="value",
                             axistick_opts=opts.AxisTickOpts(is_align_with_label=True),
                             axisline_opts=opts.AxisLineOpts(
                                 on_zero_axis_index = 0,
                                 is_on_zero=False, linestyle_opts=opts.LineStyleOpts()
                             ),
                             axispointer_opts=opts.AxisPointerOpts(
                                 is_show=False, label=opts.LabelOpts()
                             ),
                         ),
                         )
            .add_yaxis(

            xaxis_index =0,
            series_name="",
            yaxis_data=m.astype(float).tolist(),
            # yaxis_index=0,
            # color=colors[1],
            category_gap=0,
            gap =5,
            itemstyle_opts=opts.ItemStyleOpts(border_color=None),
            label_opts=opts.LabelOpts(

                formatter=JsCode(
                                    """function(params) {
                                            return params.data + '(' + ((Math.round(params.data / %s *10000)/100)) + '%s)' ;
                                    }"""%(s,"%")
                                   )
            ),
            color="#36648B",
        )
            .set_global_opts(
            title_opts=opts.TitleOpts(subtitle="数据来源:WIND"),
            yaxis_opts=opts.AxisOpts(
            type_="value",
            name="频数",
            position="left",
            # offset=80,
            axisline_opts=opts.AxisLineOpts(
                is_on_zero=True,linestyle_opts=opts.LineStyleOpts()
            ),
            axislabel_opts=opts.LabelOpts(
                #                                         # if ('value' in params.data) {
                # }
                # formatter="{value}"
                formatter = JsCode(
                                    """function(params) {
                                            return (params);
                                    }"""
                                   )

            ),


        ),
            xaxis_opts=opts.AxisOpts(
                is_show=False
            ),

        tooltip_opts=opts.TooltipOpts(is_show=False),
        toolbox_opts=opts.ToolboxOpts(is_show=True,
                                      feature=opts.ToolBoxFeatureOpts(
                                          save_as_image=opts.ToolBoxFeatureSaveAsImageOpts(
                                              background_color='white',
                                              connected_background_color="white",
                                              pixel_ratio=pixel_ratio,
                                              name="pic",
                                          ),
                                      )
                                      )
    ))
    return bar



def word_clouds(weights):

    w = WordCloud(init_opts=opts.InitOpts(width=fig_width, height=fig_height)).add(series_name="热点分析",
                        data_pair=weights,
                        word_size_range=[6, 66],
                        shape="circle",
                        )\
        .set_global_opts(
        title_opts=opts.TitleOpts(
            title="", title_textstyle_opts=opts.TextStyleOpts(font_size=23),subtitle="数据来源：WIND"
        ),
        tooltip_opts=opts.TooltipOpts(is_show=True),
        toolbox_opts=opts.ToolboxOpts(is_show=True,
                                      feature=opts.ToolBoxFeatureOpts(
                                          save_as_image=opts.ToolBoxFeatureSaveAsImageOpts(
                                              background_color='white',
                                              connected_background_color="white",
                                              pixel_ratio=pixel_ratio,
                                              name="pic",
                                          ),
                                      )
                                      )
    )
    return w


def table_base(data):

    data = data.reset_index().round(4)
    headers = data.columns.tolist()
    cont = data.values.tolist()
    table = Table().add(headers, cont).set_global_opts(
        title_opts=ComponentTitleOpts(title="", subtitle="数据来源:WIND")
    ).set_global_opts()
    return table


def pie_plot(data):
    _p_data = data.copy()
    pie = (Pie(init_opts=opts.InitOpts(width=fig_width, height=fig_height)).add(
        series_name="占比",
        data_pair=[list(z) for z in zip(_p_data.index, (_p_data.values).round(2).tolist())],
        radius=["30%", "50%"],
        # center=["30%","35%"],
        label_opts=opts.LabelOpts(is_show=False),
    ).set_global_opts(legend_opts=opts.LegendOpts(is_show=True,pos_left="2%", orient="vertical",pos_top="10%"),
                      title_opts=opts.TitleOpts(title="",subtitle="数据来源：WIND"),
                      toolbox_opts=opts.ToolboxOpts(is_show=True,
                                                    feature=opts.ToolBoxFeatureOpts(
                                                        save_as_image=opts.ToolBoxFeatureSaveAsImageOpts(
                                                            background_color='white',
                                                            connected_background_color="white",
                                                            pixel_ratio=pixel_ratio,
                                                            name="pic",
                                                        ),
                                                    )
                                                    )
                      ) \
        .set_series_opts(
        tooltip_opts=opts.TooltipOpts(
            trigger="item", formatter="{a} <br/>{b}: {c} ({d}%)"
        ),
        label_opts=opts.LabelOpts(formatter= "{b}: {c}（{d}%）")
    ))

    return pie
# pie_plot(ranks_analysis).render("mm.html")


def daily_issue_analysis(bonds_data):
    g = bonds_data.groupby('发行起始日期↑')
    count = g.apply(len).rename("发行数量")
    quantity = g['发行总额\r\n[单位] 亿元'].sum().rename("发行总额")

    merged_data = pd.concat([count,quantity],axis=1).sort_index()
    merged_data.index.name = "发行日期"

    cummulative = merged_data.cumsum()

    cummulative = cummulative.rename(columns = lambda x:"累计%s"%x)

    return merged_data,cummulative


def daily_issue_plot(daily,cummulative):
    import pyecharts.options as opts
    from pyecharts.charts import Bar, Line

    # color = ["#36648B","tomato"]

    daily = daily.round(2)
    cummulative = cummulative.round(2)

    x_data = daily.index.astype(str).tolist()

    bar = (
        Bar(init_opts=opts.InitOpts(width=fig_width, height=fig_height))
            .add_xaxis(xaxis_data=x_data)
            .add_yaxis(
            series_name="每日发行数量",
            yaxis_index=2,
            yaxis_data=daily['发行数量'].tolist(),
            label_opts=opts.LabelOpts(is_show=False),
        ).add_yaxis(
            series_name="每日发行总额",
            yaxis_index=3,
            yaxis_data=daily['发行总额'].tolist(),
            label_opts=opts.LabelOpts(is_show=False),
        )
            .set_global_opts(
            tooltip_opts=opts.TooltipOpts(
                is_show=True, trigger="axis", axis_pointer_type="cross"
            ),
            xaxis_opts=opts.AxisOpts(
                type_="category",
                axispointer_opts=opts.AxisPointerOpts(is_show=True, type_="shadow"),
            ),
            yaxis_opts=opts.AxisOpts(
                name="数量",
                type_="value",
                # min_=0,
                # max_=250,
                # interval=50,
                axislabel_opts=opts.LabelOpts(formatter="{value}"),
                axistick_opts=opts.AxisTickOpts(is_show=True),
                splitline_opts=opts.SplitLineOpts(is_show=True),
            ),
            toolbox_opts=opts.ToolboxOpts(is_show=True,
                                          feature=opts.ToolBoxFeatureOpts(
                                              save_as_image=opts.ToolBoxFeatureSaveAsImageOpts(
                                                  background_color='white',
                                                  connected_background_color="white",
                                                  pixel_ratio=pixel_ratio,
                                                  name="pic",
                                              ),
                                          )
                                          )
        )
    )

    line = (
        Line(init_opts=opts.InitOpts(width=fig_width, height=fig_height))
            .add_xaxis(xaxis_data=x_data)
            .add_yaxis(
            series_name="累计发行数量",
            yaxis_index=0,
            y_axis=cummulative['累计发行数量'].tolist(),
            label_opts=opts.LabelOpts(is_show=False),

            is_smooth=True,
            is_symbol_show=True,
            symbol="circle",
            symbol_size=6,
            linestyle_opts=opts.LineStyleOpts(width=2),

        ).add_yaxis(
            series_name="累计发行总额",
            yaxis_index=1,
            is_smooth=True,
            is_symbol_show=True,
            symbol="circle",
            symbol_size=6,
            linestyle_opts=opts.LineStyleOpts(width=2),

            y_axis=cummulative['累计发行总额'].tolist(),
            label_opts=opts.LegendOpts(is_show=False),
        )
            .extend_axis(yaxis=opts.AxisOpts(
            name= "总额",
            type_="value",
            position='right',
            offset=60,
            axislabel_opts=opts.LabelOpts(formatter="{value}亿",position="right"),

        ),).extend_axis(
            yaxis=opts.AxisOpts(
                name="数量",
                type_="value",
                position="left",
                offset=0,
                axislabel_opts=opts.LabelOpts(formatter="{value}"),
            )
        )
            .extend_axis(
            yaxis=opts.AxisOpts(
                name="总额",
                type_="value",
                position="left",
                offset=60,
                axislabel_opts=opts.LabelOpts(formatter="{value}亿"),
            )
        )

        .set_global_opts(
            tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
            xaxis_opts=opts.AxisOpts(
                splitline_opts=opts.SplitLineOpts(
                    is_show=True, linestyle_opts=opts.LineStyleOpts(color="#E8E8E8")
                ),
            ),
            yaxis_opts=opts.AxisOpts(
                name = "数量",
                type_="value",
                position="right",
                offset=0,
                axisline_opts=opts.AxisLineOpts(
                    linestyle_opts=opts.LineStyleOpts(width=1)
                ),
                splitline_opts=opts.SplitLineOpts(
                    is_show=True, linestyle_opts=opts.LineStyleOpts(color='#E8E8E8')
                ),
            ),
            toolbox_opts=opts.ToolboxOpts(is_show=True,
                                          feature=opts.ToolBoxFeatureOpts(
                                              save_as_image=opts.ToolBoxFeatureSaveAsImageOpts(
                                                  background_color='white',
                                                  connected_background_color="white",
                                                  pixel_ratio=pixel_ratio,
                                                  name="pic",
                                              ),
                                          )
                                          ),

        )
    )
    line.overlap(bar)
    return line

def plot_all(data):
    bonds_data = raw_data_process(data,rate_columns_names="票面利率(发行时)\r\n[单位] %")
    bonds_data['省份'] = bonds_data['省份'].fillna("其他")
    coupon_rate = coupon_rate_summary(bonds_data,group_name="Wind债券二级分类")
    province_analysis = province_data_format(category_analysis(bonds_data, "省份")).round(4)
    industry_analysis = category_analysis(bonds_data, "所属申万行业名称\r\n[行业级别] 一级行业")

    province_analysis_2 = province_data_format(category_analysis(bonds_data, "省份",counts=False)).round(4)
    industry_analysis_2 = category_analysis(bonds_data, "所属申万行业名称\r\n[行业级别] 一级行业",counts=False)

    ranks_analysis = rank(bonds_data)
    hotspot_analysis = usage_analysis(bonds_data)

    daily, cummulative = daily_issue_analysis(bonds_data)

    tc,tq = expireTime(bonds_data)

    tab = Tab(page_title="疫情防控债统计分析")
    tab.add(table_base(coupon_rate), "利率统计")
    tab.add(rate_histogram_plot(bonds_data['票面利率(%)'].replace("--", np.nan).astype(np.float)), "利率分布直方图")
    tab.add(province_analysis_plot(province_analysis), "发行省份统计（数量）")
    tab.add(province_analysis_plot(province_analysis_2),"发行省份统计（金额）")

    tab.add(issuer_industry_plot(industry_analysis), "发行行业统计（数量）")
    tab.add(issuer_industry_plot(industry_analysis_2),"发行行业统计（金额）")

    tab.add(word_clouds(hotspot_analysis), "资金用途热点")

    tab.add(pie_plot(ranks_analysis.drop(["已公布评级","合计"])), "评级统计")

    tab.add(pie_plot(tc),"债券期限统计（数量）")
    tab.add(pie_plot(tq),"债券期限统计（金额）")

    tab.add(daily_issue_plot(daily,cummulative),"每日发行状况统计")

    # table
    province_analysis['占比'] = (province_analysis['占比'].round(2)).astype(str)+"%"
    province_analysis = province_analysis.sort_values(by='数量',ascending=False).astype(str)
    tab.add(table_base(province_analysis),"发行省份统计表（数量）")

    province_analysis_2['占比'] = (province_analysis_2['占比'].round(2)).astype(str)+"%"
    province_analysis_2 = province_analysis_2.sort_values(by='金额(亿)',ascending=False).astype(str)
    tab.add(table_base(province_analysis_2),"发行省份统计表（金额）")

    industry_analysis.index.name = "行业(申万)"
    industry_analysis["占比"] = (industry_analysis['占比']*100).round(2).astype('str')+"%"
    industry_analysis = industry_analysis.sort_values(by='数量',ascending=False)
    tab.add(table_base(industry_analysis),"发行行业统计表（数量）")

    industry_analysis_2.index.name = "行业(申万)"
    industry_analysis_2["占比"] = (industry_analysis_2['占比']*100).round(2).astype('str')+"%"
    industry_analysis_2 = industry_analysis_2.sort_values(by='金额(亿)',ascending=False)
    tab.add(table_base(industry_analysis_2),"发行行业统计表（金额）")

    hotspot_analysis_df = pd.DataFrame(hotspot_analysis).rename(columns={0:"关键词",1:"权重"}).set_index("关键词").round(4)
    tab.add(table_base(hotspot_analysis_df),"热点统计表")

    tab.add(table_base(ranks_analysis),"债券评级统计表")

    t = pd.concat([tc.rename("数量"),tq.rename("总金额(亿)")],axis=1).round(2)
    tab.add(table_base(t),"债券期限统计表")

    df = pd.concat([daily,cummulative],axis=1).round(2)
    df.index = df.index.date.astype(str)
    df.index.name = "日期"
    tab.add(table_base(df),"每日发行状况统计表")
    return tab

def expireTime(bonds_data):
    ex_time = bonds_data['债券期限(年)\r\n[单位] 年'].rename("期限")
    quantity = bonds_data['发行总额\r\n[单位] 亿元'].rename("金额")
    time_lists = [0,30/360,90/360,180/360,1,2,3,5,np.inf]
    labels = ['1个月以内',"1-3个月","3-6个月","6个月-1年","1-2年","2-3年","3-5年",'5年以上']
    all_ls = []
    for i,d in enumerate(time_lists[1:]):
        all_ls.append(pd.Series(labels[i],index= ex_time.where((ex_time<=d)&(ex_time>time_lists[i])).dropna().index.tolist()))

    all_ls = pd.concat(all_ls)

    _ = pd.concat([all_ls.rename("期限"),quantity],axis=1)

    counts = _.groupby(['期限']).apply(len)
    quantity = _.groupby("期限").apply(lambda x:x['金额'].sum())
    index = ['1个月以内','1-3个月','3-6个月','6个月-1年','1-2年','2-3年','3-5年','5年以上']

    return counts.reindex(index),quantity.reindex(index)




# rate_histogram_plot(bonds_data['票面利率(%)'].replace("--", np.nan).astype(np.float))
# _ = rate_histogram_plot(data,bins = 10)
# _.render("ll.html")





