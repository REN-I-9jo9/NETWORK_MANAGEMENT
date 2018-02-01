#!"C:\xampp\perl\bin\perl.exe"
print	"Content-type: text/html\n\n";
use SNMP_util;
($buf, $VIEW) = split(/=/, $ENV{'QUERY_STRING'});
read(STDIN, $pre, $ENV{'CONTENT_LENGTH'});
@_p = split(/&/, $pre);
foreach $p (@_p){
	($buf, $p) = split(/=/, $p);
	if($buf eq "ip"){
		$HOST=$p;
	}
	elsif($buf eq "set"){
		$SET=$p;
	}
	elsif($buf eq "value"){
		$VALUE=$p;
	}
	elsif($buf eq "type"){
		$TYPE=$p;
	}
}
if($SET){
	@r = &snmpset($HOST,$SET,$TYPE, $VALUE);
}



$MIBII=".1.3.6.1.2.1.1";
@sys=(	"sysDescr",
		"sysObjectID",
		"sysUpTime",
		"sysContact",
		"sysName",
		"sysLocation",
		"sysServices"
	);
for($i=1; $i <= 7; $i++){
	($value1)=&snmpget("$HOST","$MIBII.$i.0");
	$syshash{$sys[$i-1]}="$value1";
}



#--------------------------------------------------------------------------------------------------------------#

print	"<html>";
print		"<head>";
#--------------------------------------------------------------------------------------------------------------#
print		'<meta charset="utf-8" >';
print		"<title>Network Management</title>";

print		"<script>";
print		"function View(view){
				var s=document.getElementById('submit');
				s.action='index.cgi?view='+view;
				s.submit();
			}";
print		"</script>";

print		"<style></style>";
#--------------------------------------------------------------------------------------------------------------#
print		"</head>";
#--------------------------------------------------------------------------------------------------------------#
print		"<body style='text-align:center;'>";
#--------------------------------------------------------------------------------------------------------------#
print			"<div style='margin:".(($HOST)?50:150)."px auto; width:".(($HOST)?1000:500).";height:".(($HOST)?750:500).";background-color:#BBFFEE'>";

if($HOST){
	
	print	"<div>網路管理<br>Network Management System<br><br><br>IP:$HOST</div><br>";
	print	(($SET&&$VALUE)?((@r)?("節點:".$SET." 數值:".$r[0]."設置成功!<br>"):"設置失敗!<br>"):"<br>")."<br>";
	if($VIEW eq "all"||!$VIEW){
		print	"System Infomation";
		print	"<table border='1' style='margin:auto;'>";
		print	"<tr><th>system</th><th></th><th rowspan='11'>&emsp;</th><th>sysInfo</th><th></th></tr>";
		@sysinfomib=(	"PlatformMajorVers",
						"PlatformMinorVers",
						"ModelString",
						"VersionControlNbr",
						"Day",
						"Month",
						"Year",
						"MajorVers",
						"MinorVers",
						"SerialNumber"
					);
		for($i=1; $i <= 10; $i++){
			$MIB=".".$syshash{'sysObjectID'}.".1.$i.0";
			($value)=&snmpget("$HOST","$MIB");
			print	"<tr>";
			print	"<td>$sys[$i-1]</td><td>";
			print	(($i ~~ [4,5,6])?	"<form action='index.cgi?view=all' method='post'>".
											"<input type='hidden' name='ip' value=$HOST>".
											"<input type='hidden' name='set' value=$MIBII.$i.0>".
											"<input type='text' name='value' value=".($syshash{$sys[$i-1]}).">".
											"<input type='hidden' name='type' value='string'>".
											"<input type='submit' value='set'>".
										"</form>":($syshash{$sys[$i-1]}));
			print	"</td>";
			print	"<td>$sysinfomib[$i-1]</td><td>".(($value)?"$value":"");
			print	"</td></tr>";
		}
		print	"</table>";
	}
	elsif($VIEW eq "connect"){
		$ifNumber=&snmpget("$HOST",".1.3.6.1.2.1.2.1.0");
	
		print	"portOpModePort";
		print	"<table border='1' style='margin:auto;'>";
		print	"<tr>".
				"<th>Port</th>".
				"<th>SpeedDuplex</th>".
				"<th>FlowCntl</th>".
				"<th>Name</th>".
				"<th>ModuleType</th>".
				"<th>LinkUpType</th>".
				"<th>IntrusionLock</th>".
				"<th>LBTestStatus</th>".
				"</tr>";
		for($j=1; $j <= $ifNumber; $j++){
			print "<tr><th>$j</th>";
			for($i=1; $i <= 7; $i++){
				$MIB1=".".$syshash{'sysObjectID'}.".19.1.1.$i.$j";
				($value)=&snmpget("$HOST","$MIB1");
				if($i==1){
					$value=	"<form action='index.cgi?view=connect' method='post'><input type='hidden' name='ip' value=$HOST><input type='hidden' name='set' value=$MIB1>".
							"<select name='value'>".
							"<option value='1' ".(($value==1)?"selected":"").">speed_10/half</option>".
							"<option value='2' ".(($value==2)?"selected":"").">speed_10/full</option>".
							"<option value='3' ".(($value==3)?"selected":"").">speed_100/half</option>".
							"<option value='4' ".(($value==4)?"selected":"").">speed_100/full</option>".
							"<option value='0' ".((!$value)?"selected":"").">auto</option>".
							"</select>".
							"<input type='hidden' name='type' value='integer'><input type='submit' value='set'></form>";
				}
				elsif($i==2){
					$value=	"<form action='index.cgi?view=connect' method='post'><input type='hidden' name='ip' value=$HOST><input type='hidden' name='set' value=$MIB1>".
							"<select name='value'>".
							"<option value='1' ".(($value==1)?"selected":"").">On</option>".
							"<option value='0' ".((!$value)?"selected":"").">Off</option>".
							"</select>".
							"<input type='hidden' name='type' value='integer'><input type='submit' value='set'></form>";
				}
				elsif($i==3){
					$value=	"<form action='index.cgi?view=connect' method='post'>".
							"<input type='hidden' name='ip' value=$HOST>".
							"<input type='hidden' name='set' value=$MIB1>".
							"<input type='text' name='value' value=".(($value)?($value):"").">".
							"<input type='hidden' name='type' value='string'>".
							"<input type='submit' value='set'>".
							"</form>";
				}
				elsif($i==4){
					$value=	($value==1)?"gigabit_ethernet_100/1000":(!$value)?"fast_ethernet_10/100":"";
				}
				elsif($i==5){
					$value=	($value==1)?"<font color='0000FF'>copper</font>":($value==2)?"fiber":(!$value)?"<font color='FF0000'>down</font>":"";
				}
				elsif($i==6){
					$value=	($value==1)?"enabled":($value==2)?"disabled":"";
				}
				elsif($i==7){
					$value=	($value==1)?"underTesting":($value==2)?"success":($value==3)?"fail":(!$value)?"none":"";
				}

				print	"<td>".(($value)?"$value":"0");
				
				print	"</td>";
			}
			print "</tr>";
		}
		print	"</table>";
	}
	elsif($VIEW eq "connect2"){
		$ifNumber=&snmpget("$HOST",".1.3.6.1.2.1.2.1.0");
	
		print	"ifTable";
		print	"<table border='1' style='margin:auto;'>";
		print	"<tr>".
				"<th rowspan='11'>Port</th>".
				"<th rowspan='2'>名稱</th>".
				"<th rowspan='2'>頻寬</th>".
				"<th rowspan='2'>速度</th>".
				"<th rowspan='2'>狀態</th>".
				"<th rowspan='2'>最終更新時間</th>".
				"<th colspan='4'>收到</th>".
				"<th colspan='3'>發送</th>".
				"</tr>".
				"<tr>".
				"<th rowspan='1'>位元組</th>".
				"<th rowspan='1'>被丟棄封包</th>".
				"<th rowspan='1'>錯誤</th>".
				"<th rowspan='1'>未知</th>".
				"<th rowspan='1'>位元組</th>".
				"<th rowspan='1'>無法發送</th>".
				"<th rowspan='1'>錯誤</th>".
				"</tr>";
		for($j=1; $j <= $ifNumber; $j++){
			foreach $i (2,4,5,8,9,10,13,14,15,16,19,20){
				$MIB1=".1.3.6.1.2.1.2.2.1.$i.$j";
				($value)=&snmpget("$HOST","$MIB1");
				if($i==8){
					($value)=($value==1)?"up":($value==2)?"down":($value==3)?"testing":"";
				}
				print "<td>".(($value)?"$value":"")."</td>";
			}
			print "</tr>";
		}
		print	"</table>";
	}
	elsif($VIEW eq "iptable"){
		@iptable=&snmpwalk("$HOST",".1.3.6.1.2.1.4.20.1");
		$iptablelength=$#iptable+1;
		print	"ipAddrTable";
		print	"<table border='1' style='margin:auto;'>";
		print	"<tr>".
				"<th></th>".
				"<th>Addr</th>".
				"<th>IfIndex</th>".
				"<th>NetMask</th>".
				"<th>BcastAddr</th>".
				"<th>ReasmMaxSize</th>".
				"</tr>";
		for($i=0;$i<$iptablelength/5;$i++){
			print	"<tr><th>".($i+1)."</th>";
			for($j=0;$j<5;$j++){
				($buf,$n)=split(/:/, $iptable[$j*($iptablelength/5)+$i]);
				print	"<td>".$n."</td>";
			}
			print	"</tr>";
		}
		print	"</table>";
	}
	elsif($VIEW eq "alarm"){
		@alarmtable=&snmpwalk("$HOST",".1.3.6.1.2.1.16.3.1.1");
		$alarmtablelength=$#alarmtable+1;
		print	"alarmTable";
		print	"<table border='1' style='margin:auto;'>";
		print	"<tr>".
				"<th rowspan='2'>Index</th>".
				"<th rowspan='2'>Interval</th>".
				"<th rowspan='2'>Variable</th>".
				"<th rowspan='2'>SampleType</th>".
				"<th rowspan='2'>Value</th>".
				"<th rowspan='2'>StartupAlarm</th>".
				"<th colspan='2'>Threshold</th>".
				"<th colspan='2'>EventIndex</th>".
				"<th rowspan='2'>Owner</th>".
				"<th rowspan='2'>Status</th>".
				"</tr>".
				"<tr>".
				"<th>Rising</th>".
				"<th>Falling</th>".
				"<th>Rising</th>".
				"<th>Falling</th>".
				"</tr>";
		for($i=0;$i<$alarmtablelength/12;$i++){
			print	"<tr><th>".($i+1)."</th>";
			for($j=0;$j<12;$j++){
				($buf,$n)=split(/:/, $alarmtable[$j*($alarmtablelength/12)+$i]);
				print	"<td>".$n."</td>";
			}
			print	"</tr>";
		}
		if(!@alarmtable){
			print	"<tr><td colspan='12'>No Alarm</td></tr>";
		}
		print	"</table>";
	}
	elsif($VIEW eq "free"){
		print	"<form action='index.cgi?view=free' method='post'>".
				"<input type='hidden' name='ip' value=$HOST>".
				"OID:<input type='text' name='set'><br>".
				"VALUE:<input type='text' name='value'><br>".
				"TYPE:<input type='text' name='type'><br>".
				"<input type='submit' value='set'>".
				"</form>";
	}
	else{
	}
	
	print	"<br>";
	print	"<form id='submit' action='index.cgi?view=all' method='post'>";
	print	"<input type='hidden' name='ip' value=$HOST>";
	print	"<div style='background-color:#DDDDDD; display:inline-block;' onclick=View('alarm')>Alarm</div>&emsp;";
	print	"<div style='background-color:#DDDDDD; display:inline-block;' onclick=View('connect')>連接控制</div>&emsp;";
	print	"<div style='background-color:#DDDDDD; display:inline-block;' onclick=View('connect2')>連接資訊</div>&emsp;";
	print	"<div style='background-color:#DDDDDD; display:inline-block;' onclick=View('iptable')>位址表</div>&emsp;";
	print	"<div style='background-color:#DDDDDD; display:inline-block;' onclick=View('free')>自由輸入</div>&emsp;";
	print	"<div style='background-color:#DDDDDD; display:inline-block;' onclick=View('all')>回首頁</div>";
	print	"</form>";
}
else{
	print	"<br><br><br><br>Network Management System<br><br><br><br><br><br><br><br>";
	print	"<form id='submit' action='index.cgi' method='post'>";
	print	"Switch IP: <input type='text' name='ip'>";
	print	"<input type='submit' value='Submit' >";
	print	"</form>";
}
print	"</div>";
#--------------------------------------------------------------------------------------------------------------#
print		"</body>";
print	"</html>";
#--------------------------------------------------------------------------------------------------------------#