import os


html = '''
<!doctype html>
<html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="Author" content="qcy">
        <meta name="Keywords" content="tech indicator">
        <meta name="Description" content="buy sell tips">
        <title>技术指标</title>
    </head>

    <link rel="stylesheet" href="./tech.css" type="text/css">
    <script>
	   // 对Date的扩展，将 Date 转化为指定格式的String
	   // 月(M)、日(d)、小时(h)、分(m)、秒(s)、季度(q) 可以用 1-2 个占位符，
	   // 年(y)可以用 1-4 个占位符，毫秒(S)只能用 1 个占位符(是 1-3 位的数字)
	   // 例子pe="text/javascript">
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


    <body>
'''

html2 = '''

	      <div style="margin: 0 0px; background-color: white;">

		        <!-- <div style="margin-left: 55px; margin-top: 20px"> -->
		        <div style="margin-top: 20px; text-align:center">
			          <!-- <span class="arial_17">{ccy1_cn}兑{ccy2_cn}&nbsp;{pair}</span> -->
			          <span style="font-family:Helvetica; font-weight:bold; font-size:16px; text-align:center">{ccy1_cn}兑{ccy2_cn}&nbsp;{pair}</span>
                <!-- <span title="Euro Zone" class="ceFlags Europe">&nbsp;</span> -->
		        </div>

		        <div style="margin-top: 8px;">
			          <div style="margin-left: 0px;">
                            <img src="{arrow_pic}" style="width:22px; height:22px; margin-bottom: 12px"/>
				            <span class="inlineblock">

					              <span class="top bold inlineblock" style="float: left; margin-top: 5px;">

						                <span class="arial_12">{last_px}</span>
                            <span class="arial_12 greenFont" style="margin-left:1px;">{chg}</span>
						                <!-- <span dir="rtl"></span> -->
                            <span class="arial_12 greenFont  pid-166-pcp parentheses">{chgpct}</span>
					                  <!-- </div> -->
					                  <span class="bottom lighterGrayFont arial_11" style="margin-left: -154px;margin-top: 31px; float: left;"></span>
					                  <!-- <span class="inlineblock greenClockBigIcon" style=""></span> -->
                            <span id="timeShow" class="bold" style="margin-left: 3px; font-size: 10px">这里显示时间</span>
					              </span>
				            </span>
			          </div>
		        </div>
	      </div>

	      <div class="halfSizeColumn" style="margin-top: -30px;">
		        <h3>
			          <a href="#">&nbsp;移动平均 MA</a><span
				                                             class=" arial_11 bold lighterGrayFont h3TitleDate"> </span>
		        </h3>

		        <div class="clear"></div>
		        <table class="genTbl closedTbl movingAvgsTbl" id="curr_table">
			          <thead>
				            <tr>
					              <th class="first left">周期</th>
					              <th>简单均线&nbsp;SMA</th>
					              <th>指数均线&nbsp;EMA</th>
				            </tr>
			          </thead>
			          <tbody>
				            <tr>
					              <td class="first left symbol">MA5</td>
					              <td>{ma5_str}&nbsp; <span class="greenFont bold">{ma5_comment}</span>
					              </td>
					              <td>{ema5_str}&nbsp; <span class="greenFont bold">{ema5_comment}</span>
					              </td>
				            </tr>
				            <tr>
					              <td class="first left symbol">MA10</td>
					              <td>{ma10_str}&nbsp; <span class="greenFont bold">{ma10_comment}</span>
					              </td>
					              <td>{ema10_str}&nbsp; <span class="greenFont bold">{ema10_comment}</span>
					              </td>
				            </tr>
				            <tr>
					              <td class="first left symbol">MA20</td>
					              <td>{ma20_str}&nbsp; <span class="greenFont bold">{ma20_comment}</span>
					              </td>
					              <td>{ema20_str}&nbsp; <span class="greenFont bold">{ema20_comment}</span>
					              </td>
				            </tr>
				            <tr>
					              <td class="first left symbol">MA50</td>
					              <td>{ma50_str}&nbsp; <span class="greenFont bold">{ma50_comment}</span>
					              </td>
					              <td>{ema50_str}&nbsp; <span class="greenFont bold">{ema50_comment}</span>
					              </td>
				            </tr>
				            <tr>
					              <td class="first left symbol">MA100</td>
					              <td>{ma100_str}&nbsp; <span class="greenFont bold">{ma100_comment}</span>
					              </td>
					              <td>{ema100_str}&nbsp; <span class="greenFont bold">{ema100_comment}</span>
					              </td>
				            </tr>
				            <tr>
					              <td colspan="3" class="first left lastRow">
						                <p class="inlineblock">
							                  <span class="noBold">偏多:</span> <span>0</span>
						                </p>
						                <p class="inlineblock">
							                  <span class="noBold">偏空:</span> <span>12</span>
						                </p> <br>
						                <p class="inlineblock">
							                  综合研判：<span class="greenFont bold uppercaseText"> {shit} </span>
						                </p>
					              </td>
				            </tr>
			          </tbody>
		        </table>
	      </div>



	      <div class="halfSizeColumn tech_indicator_div"
		                style="margin-top: -20px;">
		        <h3>
			          <a href="#">&nbsp;技术指标</a><span
				                                          class=" arial_11 bold lighterGrayFont h3TitleDate"> </span>
			          <!-- 这里可以写点什么 -->

		        </h3>
		        <span class="clear"></span>
		        <table class="genTbl closedTbl movingAvgsTbl float_lang_base_2"
			                    id="curr_table">
			          <thead>
				            <tr>
					              <th class="first left">指标</th>
					              <th>数值</th>
					              <th class="left textNum">诊断</th>
				            </tr>
			          </thead>
			          <tbody>
				            <tr>
					              <td class="first left symbol">MACD(12,26,9)</td>
					              <td class="right">{macd:.4f}</td>
					              <td class="left textNum bold"><span class="greenFont bold">{macd_comment}</span>
					              </td>
				            </tr>
				            <tr>
					              <td class="first left symbol">RSI(14)</td>
					              <td class="right">{rsi:.2f}</td>
					              <td class="left textNum bold"><span class="bold">{rsi_comment}</span></td>
				            </tr>
				            <tr>
					              <td class="first left symbol">ADX(14)</td>
					              <td class="right">{adx_str}</td>
					              <td class="left textNum bold"><span class="bold">{adx_comment}</span></td>
				            </tr>
				            <tr>
					              <td class="first left symbol">STOCH(9,6)</td>
					              <td class="right">{stoch:.2f}</td>
					              <td class="left textNum bold"><span class="bold">{stoch_comment}</span></td>
				            </tr>
				            <tr>
					              <td class="first left symbol">CCI(14)</td>
					              <td class="right">{cci:.2f}</td>
					              <td class="left textNum bold"><span class="greenFont bold">{cci_comment}</span>
					              </td>
				            </tr>
				            <tr>
					              <td class="first left symbol">StochRSI</td>
					              <td class="right">{stochrsi:.2f}</td>
					              <td class="left textNum bold"><span class="greenFont bold">{stochrsi_comment}</span>
					              </td>
				            </tr>
				            <tr>
					              <td class="first left symbol">Ultimate Oscillator</td>
					              <td class="right">{uo:.2f}</td>
					              <td class="left textNum bold"><span class="greenFont bold">{uo_comment}</span>
				            </tr>
				            <tr>
					              <td class="first left symbol">ROC</td>
					              <td class="right">{roc:.4f}</td>
					              <td class="left textNum bold"><span class="greenFont bold">{roc_comment}</span></td>
				            </tr>
				            <tr>
					              <td class="first left symbol">SAR</td>
					              <td class="right">{sar_str}</td>
					              <td class="left textNum bold"><span class="greenFont bold">{sar_comment}</span>
					              </td>
				            </tr>
				            <tr>
					              <td colspan="3" class="first left lastRow">
						                <p class="inlineblock">
							                  <span class="noBold">偏多:</span> <span>0</span>
						                </p>
						                <p class="inlineblock">
							                  <span class="noBold">偏空:</span> <span>8</span>
						                </p>
						                <p class="inlineblock">
							                  <span class="noBold">中性:</span> <span>0</span>
						                </p> <br>
						                <p class="inlineblock">
							                  综合研判：<span class="greenFont bold uppercaseText"> {shit2} </span>
						                </p>
					              </td>
				            </tr>
			          </tbody>
		        </table>
	      </div>
    </body>
</html>
'''


# data = {'ma5':1111, 'ema5':12313, 'shit':'空头抛压极强', 'shit2':'blablabla'}


def gen_html_pic(data, filename):
    with open('./output/{}.html'.format(filename), 'w') as f:
        f.write(html + html2.format(**data))

    html_url = 'file:///home/yiju/wxpic/output/{}.html'.format(filename)
    pic_path = './output/{}.png'.format(filename)

    # os.system('CutyCapt --url={} --out={} --min-width=100 --min-height=10 --zoom-factor=2.0'.format(html_url, pic_path))
    os.system('CutyCapt --url={} --out={} --min-width=620 --zoom-factor=3.0'.format(html_url, pic_path))
