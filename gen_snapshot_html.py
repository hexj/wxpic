import os

html = '''
<!doctype html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="Author" content="qcy">
<meta name="Keywords" content="tech indicator">
<meta name="Description" content="buy sell tips">
<title>市场快照</title>
</head>

<!-- <link rel="stylesheet" href="./tech.css" type="text/css"> -->
<link rel="stylesheet" href="./mkt_snapshot.css" type="text/css">
<script type="text/javascript">
	// 对Date的扩展，将 Date 转化为指定格式的String
	// 月(M)、日(d)、小时(h)、分(m)、秒(s)、季度(q) 可以用 1-2 个占位符，
	// 年(y)可以用 1-4 个占位符，毫秒(S)只能用 1 个占位符(是 1-3 位的数字)
	// 例子：
	// (new Date()).Format("yyyy-MM-dd hh:mm:ss.S") ==> 2006-07-02 08:09:04.423
	// (new Date()).Format("yyyy-M-d h:m:s.S")      ==> 2006-7-2 8:9:4.18
	Date.prototype.Format = function(fmt) { //author: meizz
		var o = {
			"M+" : this.getMonth() + 1, //月份
			"d+" : this.getDate(), //日
			"h+" : this.getHours(), //小时
			"m+" : this.getMinutes(), //分
			"s+" : this.getSeconds(), //秒
			"q+" : Math.floor((this.getMonth() + 3) / 3), //季度
			"S" : this.getMilliseconds()
		//毫秒
		};
		if (/(y+)/.test(fmt))
			fmt = fmt.replace(RegExp.$1, (this.getFullYear() + "")
					.substr(4 - RegExp.$1.length));
		for ( var k in o)
			if (new RegExp("(" + k + ")").test(fmt))
				fmt = fmt.replace(RegExp.$1, (RegExp.$1.length == 1) ? (o[k])
						: (("00" + o[k]).substr(("" + o[k]).length)));
		return fmt;
	};
	var time1 = new Date().Format("yyyy/MM/dd");
	var dateTime = new Date().Format("yyyy/MM/dd hh:mm:ss");

	/*document.write(dateTime);*/
</script>

<script type="text/javascript">
	var t = null;
	function time() {
		var dateTime = new Date().Format("yyyy/MM/dd hh:mm:ss");
		document.getElementById("timeShow").innerHTML = dateTime;
		t = setTimeout(time, 1000);
	}
	window.onload = function() {
		time();
	};
</script>

<script type="text/javascript" src="./jquery-1.7.2.min.js"></script>
<script src="jquery-1.8.3.min.js" type="text/javascript"></script>
<script src="highstock.js" type="text/javascript"></script>
<script type="text/javascript" src="./jquery.sparkline.js"></script>

<body>
	<div
		style="margin: 0 0px; width: 320px; border: 0px;">

		<!-- 标题 -->
		<div style="align:center; margin-top: -10px;">
            <h2 style="text-align:center">市场快照</h2>
				<p id="timeShow" style="margin:-10px auto 2px auto; text-align:center; color: gray; font-weight: bold; font-size: 8pt;">这里显示时间</p>
		</div>
		<!-- 显示时间 -->
'''


html2 = '''
		<!-- 主要货币的表格 -->
		<div style="float:left; background-color: white; border: 0px silver solid; ">

			<!-- 第一行 旗帜、名称、上涨下跌-->
			<!-- <table class="genTbl closedTbl " id="curr_table"> -->
			<table class="genTbl closedTbl " id="curr_table">
				<thead>
					<tr style="height: 30px;">
						<th style="width: 50px; text-align: left;">
							<span style="float: left; margin-top: 3px; margin-left: 2px;"><img
								src="{ccy1}-icon.png" style="width: 18px; height: 18px;" /> <img
								src="{ccy2}-icon.png" style="width: 18px; height: 18px;" /></span>
						</th>
						<th style="width:120px; font-size: 10pt; text-align: left;">{ccy1_cn}兑{ccy2_cn}</th>
            <th>
                        <img src="{arrow_pic}" style="width: 20px; height: 20px; margin-bottom: -7px;">
            </th>
						<th style="width:54px; padding-top:2px; font-size: 10pt;">
                        <span style="width:80px">{last_px}</span>
            </th>
            <th style="width:52px; padding-top:2px">
            <span style="font-size:8pt" class="{chgcolor}">{chgpct}</span>
            </th>
					</tr>
				</thead>
			</table>

			<!--  -->
			<table class="genTbl closedTbl " id="curr_table">
				<tbody>
					<tr style="">
						<td style=""><span class="blueFont bold" style="float:left; padding-left: 2px; width: 48px">小时均线</span></td>
						<td style="text-align: left; width: 60px;">&nbsp;偏多:&nbsp;<span class="redFont">{n_long1}</span></td>
						<td style="text-align: left; width: 60px;">&nbsp;偏空:&nbsp;<span class="greenFont">{n_short1}</span></td>
						<!-- 折线图 -->
                        <td rowspan="3"><div id="container_{ccy1}{ccy2}" style="width: 128px; height: 68px; margin-right: -30px;  padding-right: 0px;"></div>
						</td>
					</tr>
					<tr style="">
						<td rowspan="2" style=""><span class="blueFont bold" style="float: left; padding-left:2px; width: 48px">技术指标</span></td>
						<td style="text-align: left; width: 60px;">&nbsp;偏多:&nbsp;<span class="redFont">{n_long2}</span></td>
						<td style="text-align: left; width: 60px;">&nbsp;偏空:&nbsp;<span class="greenFont">{n_short2}</span></td>
					</tr>
					<tr>
						<td style="text-align: left; width: 60px;">&nbsp;超买:&nbsp;<span class="">{n_ob}</span></td>
						<td style="text-align: left; width: 60px;">&nbsp;超卖:&nbsp;<span class="">{n_os}</span></td>
					</tr>
				</tbody>
			</table>
		</div>


<script type="text/javascript">
	var ichart = new Highcharts.stockChart({{
		chart : {{
			renderTo : "container_{ccy1}{ccy2}",
			animation : false
		}},
		credits : {{
			enabled : false
		}},
		scrollbar : {{
			enabled : false
		}},
		exporting : {{
			enabled : false
		}},
		rangeSelector : {{
			enabled : false
		}},
		navigator : {{
			enabled : false
		}},
		xAxis : {{
			visible : false,
		}},
		yAxis : {{
			visible : false,
			minPadding : 0,
			maxPadding : 0
		}},
		series : [ {{
			name : 'AAPL Stock Price',
            animation: false,

			data : {px_data},

			type : 'area',
			threshold : null,
			tooltip : {{
				enabled: false
			}},
			fillColor : {{
				linearGradient : {{
					x1 : 0,
					y1 : 0,
					x2 : 0,
					y2 : 1
				}},
				stops : [
						[ 0, Highcharts.getOptions().colors[0] ],
						[
								1,
								Highcharts.Color(
										Highcharts.getOptions().colors[0])
										.setOpacity(0).get('rgba') ] ]
			}}
		}} ]
	}});
</script>
'''


html3 = '''
        </div>
    </body>
</html>
'''

def gen_snapshot_tr(data):
    return html2.format(**data)

