# -*- coding: utf-8 -*-
"""
Created on Sat Jun  3 17:25:49 2017

@author: qcy
"""

import codecs
f = codecs.open("技术指标_out.html", "w", "utf-8")

ATR = 1000000


#style="width:380px; height:520px;"

html_head = '''
<!doctype html>
<html lang="en">
 <head>
  <meta charset="UTF-8">
  <meta name="Generator" content="EditPlus">
  <meta name="Author" content="">
  <meta name="Keywords" content="">
  <meta name="Description" content="">
  <title>Document</title>
 </head>

<link rel="stylesheet" href="./newMainCssMin_v38p.css" type="text/css">

 <body style="font-size:10pt">

<div style="margin-top:-14px;">
<table class="genTbl closedTbl technicalIndicatorsTbl smallTbl float_lang_base_1"

id="curr_table">
	<thead>
		<tr>
			<th class="first left">指标</th>
			<th>Value</th>
			<th class="left textNum">Action</th>
		</tr>
	</thead>
	<tbody>'''
    
html_tail = '''<tr>
			<td colspan="3" class="first left lastRow">
				<p class="inlineblock">
					<span class="noBold">Buy:</span> <span>7</span>
				</p>
				<p class="inlineblock">
					<span class="noBold">Sell:</span> <span>0</span>
				</p>
				<p class="inlineblock">
					<span class="noBold">Neutral:</span> <span>0</span>
				</p>
								<br>
				<p class="inlineblock">
					Summary:<span class="greenFont bold uppercaseText">Strong Buy</span>
				</p>
							</td>
		</tr>
			</tbody>
</table>

</div>

<div>


 </body>
</html>'''    

def get_color_by_action(action):
    if 'Buy' == action:
        return 'greenFont bold'    
    elif 'Sell' == action:
        return 'redFont bold'
    return 'bold'

def gen_tri(t_name, t_value, t_action):
    
    t_color = get_color_by_action(t_action);
                                 
    # #DE3E3E ---- Red
    # #FF0000 ---- Green
    
    s = '''
    		<tr>
			<td class="first left symbol">'''+t_name+'''</td>
			<td class="right">'''+t_value+'''</td>
			<td class="left textNum bold">
				<span class="'''+t_color+'''">'''+t_action+'''</span>
			</td>
		</tr>'''
    
    return s


html_body = ''

data = [['aaa',12,'Buy'],
        ['xfsd',213.2,'Sell'],
        ['xfsd',213.2,'Sell'],
        ['xfsd',213.2,'Sell'],
        ['xfsd',213.2,'Sell'],
        ['xfsd',213.2,'Sell']
        ]
for i in data:
    html_body += gen_tri(i[0], str(i[1]), i[2])



h = '''
<!doctype html>
<html lang="en">
 <head>
  <meta charset="UTF-8">
  <meta name="Generator" content="EditPlus">
  <meta name="Author" content="">
  <meta name="Keywords" content="">
  <meta name="Description" content="">
  <title>Document</title>
 </head>

<link rel="stylesheet" href="./newMainCssMin_v38p.css" type="text/css">

 <body style="font-size:20pt">

<div style="margin-left:10px;">
<table class="genTbl closedTbl technicalIndicatorsTbl smallTbl float_lang_base_1"
id="curr_table"
>
	<thead>
		<tr>
			<th class="first left">指标</th>
			<th>Value</th>
			<th class="left textNum">Action</th>
		</tr>
	</thead>
	<tbody>
    
    
		<tr>
			<td class="first left symbol">RSI(14)</td>
			<td class="right">79.040</td>
			<td class="left textNum bold">
				<span class="bold">Overbought</span>
			</td>
		</tr>
					<tr>
			<td class="first left symbol">STOCH(9,6)</td>
			<td class="right">70.201</td>
			<td class="left textNum bold">
				<span class="greenFont bold">Buy</span>
			</td>
		</tr>
					<tr>
			<td class="first left symbol">STOCHRSI(14)</td>
			<td class="right">100.000</td>
			<td class="left textNum bold">
				<span class="bold">Overbought</span>
			</td>
		</tr>
					<tr>
			<td class="first left symbol">MACD(12,26)</td>
			<td class="right">0.440</td>
			<td class="left textNum bold">
				<span class="greenFont bold">Buy</span>
			</td>
		</tr>
					<tr>
			<td class="first left symbol">ADX(14)</td>
			<td class="right">37.052</td>
			<td class="left textNum bold">
				<span class="greenFont bold">Buy</span>
			</td>
		</tr>
					<tr>
			<td class="first left symbol">Williams %R</td>
			<td class="right">-3.687</td>
			<td class="left textNum bold">
				<span class="bold">Overbought</span>
			</td>
		</tr>
					<tr>
			<td class="first left symbol">CCI(14)</td>
			<td class="right">162.5949</td>
			<td class="left textNum bold">
				<span class="greenFont bold">Buy</span>
			</td>
		</tr>
					<tr>
			<td class="first left symbol">ATR(14)</td>
			<td class="right">'''+str(ATR)+'''</td>
			<td class="left textNum bold">
				<span class="bold">High Volatility</span>
			</td>
		</tr>
					<tr>
			<td class="first left symbol">Highs/Lows(14)</td>
			<td class="right">1.1064</td>
			<td class="left textNum bold">
				<span class="greenFont bold">Buy</span>
			</td>
		</tr>
					<tr>
			<td class="first left symbol">Ultimate Oscillator</td>
			<td class="right">72.009</td>
			<td class="left textNum bold">
				<span class="bold">Overbought</span>
			</td>
		</tr>
					<tr>
			<td class="first left symbol">ROC</td>
			<td class="right">2.127</td>
			<td class="left textNum bold">
				<span id='ROC_span' class="greenFont bold">Buy</span>
			</td>
		</tr>
					<tr>
			<td class="first left symbol">Bull/Bear Power(13)</td>
			<td class="right">1.6860</td>
			<td class="left textNum bold">
				<span class="greenFont bold">Buy</span>
			</td>
		</tr>
					<tr>
			<td colspan="3" class="first left lastRow">
				<p class="inlineblock">
					<span class="noBold">Buy:</span> <span>7</span>
				</p>
				<p class="inlineblock">
					<span class="noBold">Sell:</span> <span>0</span>
				</p>
				<p class="inlineblock">
					<span class="noBold">Neutral:</span> <span>0</span>
				</p>
								<br>
				<p class="inlineblock">
					Summary:<span class="greenFont bold uppercaseText">Strong Buy</span>
				</p>
							</td>
		</tr>
			</tbody>
</table>

</div>

<div>


 </body>
</html>
'''


h_content = html_head+html_body+html_tail

#file_object2 = open('技术指标_out.html','w','utf-8')
try:
#    file_object2.write(h)
#
    f.write(h_content)
   

finally:
#     file_object2.close( )
     f.close()