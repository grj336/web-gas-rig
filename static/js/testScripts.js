$(document).ready(function(){
var dataRecordState = 0

	// Change Flow Rate	
  function changeFlowRate(mfcIndex){
    //alert("The text has been changed.");
	var a = $("#changeFlow_1").val();
	//alert("New value is" + a);
	$.post("/updateMFC", {
	flowRate: a,
	mfcIndex: mfcIndex,
	}, function(data){
		//alert("Returned Value: " + data);
		$('#currentSetPoint').text(data);
		//alert("line 16")
	});
  };

  //Auto button
  $('#autoButton').click(function(){
	alert("Auto Activated")
	$.post("/autoExperimentModeStart")
  });

  $('#autoOffButton').click(function(){
	alert("Auto Off")
	$.post("/autoExperimentModeStop")
  });

  $('#starWars').click(function(){
	$.post("/playStarWars")
  });

  $('#saveDataON').click(function(){
	if(this.checked){
		dataRecordState = 1;
		$.post("/runDataLogger", {
			dataRecordState: 1,
		});
	}
	else{
		dataRecordState = 0;
		$.post("/runDataLogger", {
			dataRecordState: 0,
		});
	}
  });


//   $('#recordDataTrue').click(function(){
// 	alert("In the function");
// 	if(this.checked){
// 		$.post("/recordData", {
// 			dataRecordState: 1,
// 		});
// 	}
// 	else{
// 		alert("SMU Off");
// 		$.post("/recordData", {
// 			dataRecordState: 0,
// 		});
// 	}
// });


  // MFC 1
  $('#setFlowRate_1').click(function(){
	var a = $('#changeFlow_1').val();
	var mfcNo = 0;
	$.post("/updateMFC", {
		flowRate: a,
		mfcIndex: mfcNo,
	});
  });

  $('#increaseFlowRate_1').click(function(){
	var mfcNo = 0;
	$.post("/increaseMFC", {
		mfcIndex: mfcNo,
	});
  });

  $('#decreaseFlowRate_1').click(function(){
	var mfcNo = 0;
	$.post("/decreaseMFC", {
		mfcIndex: mfcNo,
	});
  });

  $('#setGas1').click(function(){
	var mfcNo = 0;
	var gasValue = $('#choseGas1').val();
	$.post("/setMFCGas", {
		mfcIndex: mfcNo,
		newGas: gasValue,
	});
  });

  //MFC 2
  $('#setFlowRate_2').click(function(){
	var a = $('#changeFlow_2').val();
	var mfcNo = 1;
	$.post("/updateMFC", {
		flowRate: a,
		mfcIndex: mfcNo,
	});
  });

  $('#increaseFlowRate_2').click(function(){
	var mfcNo = 1;
	$.post("/increaseMFC", {
		mfcIndex: mfcNo,
	});
  });

  $('#decreaseFlowRate_2').click(function(){
	var mfcNo = 1;
	$.post("/decreaseMFC", {
		mfcIndex: mfcNo,
	});
  });

  $('#setGas2').click(function(){
	var mfcNo = 1;
	var gasValue = $('#choseGas2').val();
	$.post("/setMFCGas", {
		mfcIndex: mfcNo,
		newGas: gasValue,
	});
  });

  //MFC 3 
  $('#setFlowRate_3').click(function(){
	var a = $('#changeFlow_3').val();
	var mfcNo = 2;
	$.post("/updateMFC", {
		flowRate: a,
		mfcIndex: mfcNo,
	});
  });

  $('#increaseFlowRate_3').click(function(){
	var mfcNo = 2;
	$.post("/increaseMFC", {
		mfcIndex: mfcNo,
	});
  });

  $('#decreaseFlowRate_3').click(function(){
	var mfcNo = 2;
	$.post("/decreaseMFC", {
		mfcIndex: mfcNo,
	});
  });

  $('#setGas3').click(function(){
	var mfcNo = 2;
	var gasValue = $('#choseGas3').val();
	$.post("/setMFCGas", {
		mfcIndex: mfcNo,
		newGas: gasValue,
	});
  });

  //Flow meter
  $('#setGas4').click(function(){
	var mfcNo = 3;
	var gasValue = $('#choseGas4').val();
	$.post("/setMFCGas", {
		mfcIndex: mfcNo,
		newGas: gasValue,
	});
  });

  $('#mfcShutDown').click(function(){
	  alert('MFC Shutting Down!')
	  $.get("/mfcShutdown")
  });

  $('#setHotwireParams').click(function(){
	  $.post("/setParams", {
		  tcrVal: $('#tcrValue').val(),
		  r0Val: $('#r0Value').val(),
		  t0Val: $('#t0Value').val(),
		  userNameVal: $('#userNameInput').val(),
		  testNameVal: $('#testName').val(),
	  });
  });

  $('#clearCharBTN').click(function(){
	smuOutputsContainer1.series[0].setData([]);
	smuOutputsContainer2.series[0].setData([]);
	smuOutputsContainer3.series[0].setData([]);
	adcOutputsContainer1.series[0].setData([]);
	adcOutputsContainer2.series[0].setData([]);
	adcOutputsContainer3.series[0].setData([]);

  })

  $('#setMultiFlow').click(function(){
	var a = $('#multiFlow_1').val();
	var b = $('#multiFlow_2').val();
	var c = $('#multiFlow_3').val();
	$.post("/updateMultiMFC", {
		flowRate1: a,
		flowRate2: b,
		flowRate3: c,
	});
  });



// Set Up guage

var gaugeOptions = {
	chart: {
		type: 'solidgauge'
	},  
	title: null,  
	pane: {
		center: ['50%', '40%'],
		size: '100%',
		startAngle: -90,
		endAngle: 90,
		background: {
			backgroundColor:
				Highcharts.defaultOptions.legend.backgroundColor || '#EEE',
			innerRadius: '60%',
			outerRadius: '100%',
			shape: 'arc'
		}
	},  
	exporting: {
		enabled: false
	},  
	tooltip: {
		enabled: false
	},  
	// the value axis
	yAxis: {
		stops: [
			[0.1, '#55BF3B'], // green
			[0.7, '#DDDF0D'], // yellow
			[0.9, '#DF5353'] // red
		],
		lineWidth: 0,
		tickWidth: 0,
		minorTickInterval: null,
		tickAmount: 2,
		title: {
			y: -70
		},
		labels: {
			y: 16
		}
	},  
	plotOptions: {
		solidgauge: {
			dataLabels: {
				y: 5,
				borderWidth: 0,
				useHTML: true
			}
		}
	}
  };

var flowRateGuageOptions = {
	yAxis: {
		min: 0,
		max: 500,
	},  
	credits: {
		enabled: false
	},  
	series: [{
		name: 'FlowRate',
		data: [450],
		dataLabels: {
			format:
				'<div style="text-align:center">' +
				'<span style="font-size:25px">{y}</span><br/>' +
				'<span style="font-size:12px;opacity:0.4">SLPM</span>' +
				'</div>'
		},
		tooltip: {
			valueSuffix: 'SCCM'
		}
	}]
};

var flowRateGauge_1 = Highcharts.chart('container-flowRateGauge_1', Highcharts.merge(gaugeOptions, flowRateGuageOptions));
var flowRateGauge_2 = Highcharts.chart('container-flowRateGauge_2', Highcharts.merge(gaugeOptions, flowRateGuageOptions));
var flowRateGauge_3 = Highcharts.chart('container-flowRateGauge_3', Highcharts.merge(gaugeOptions, flowRateGuageOptions));
var flowRateGauge_4 = Highcharts.chart('container-flowRateGauge_4', Highcharts.merge(gaugeOptions, flowRateGuageOptions));

setInterval(function(){
//Alternative #recordDataTrue
	$.post("/recordData", {
		dataRecordState: dataRecordState,
	},
	function(data){
	// $.get("/getMFCInfo" ,
	// function(data){
		//alert(data)
		//alert(data[1])
		//alert(data[1].gas)
		//alert(dataRecordState)
		if (dataRecordState == 1){
			//alert("line 257")
			$('#mfcFlowRate_1').text(String(data[1]));
			//alert(data[1]);
			$('#mfcFlowRate_2').text((data[2]));
			$('#mfcFlowRate_3').text(String(data[3]));
			$('#mfcFlowRate_4').text(String(data[4]));
			(flowRateGauge_1.series[0].points[0]).update(data[1]);
			(flowRateGauge_2.series[0].points[0]).update(data[2]);
			(flowRateGauge_3.series[0].points[0]).update(data[3]);
			(flowRateGauge_4.series[0].points[0]).update(data[4]);
		}
		else{		
		$('#mfcGasType_1').text(data[1].gas);
		$('#mfcSetPoint_1').text(data[1].setpoint);
		$('#mfcFlowRate_1').text(data[1].mass_flow);
		$('#mfcGasType_2').text(data[2].gas);
		$('#mfcSetPoint_2').text(data[2].setpoint);
		$('#mfcFlowRate_2').text(data[2].mass_flow);
		$('#mfcGasType_3').text(data[3].gas);
		$('#mfcSetPoint_3').text(data[3].setpoint);
		$('#mfcFlowRate_3').text(data[3].mass_flow);
		$('#mfcGasType_4').text(data[4].gas);
		$('#mfcFlowRate_4').text(data[4].mass_flow);

		(flowRateGauge_1.series[0].points[0]).update(data[1].mass_flow);
		(flowRateGauge_2.series[0].points[0]).update(data[2].mass_flow);
		(flowRateGauge_3.series[0].points[0]).update(data[3].mass_flow);
		(flowRateGauge_4.series[0].points[0]).update(data[4].mass_flow);
		}
		
		//$('#measuredTemperature').val(data[1][0]);
		$('#measuredCurrent').val(data[5].toFixed(3));
		$('#hotWireCardCurrent').text((data[5]*1000).toFixed(3));
		$('#measuredVoltage').val(data[6].toFixed(3));
		$('#hotWireCardVoltage').text(data[6].toFixed(3));
		$('#measuredTemperature').val(data[8].toFixed(3));
		$('#hotWireCardTemperature').text(data[8].toFixed(1));
		$('#measuredResistance').val(data[7].toFixed(3));
		$('#thermoUpStream').val(data[9].toFixed(3));
		$('#thermoDownStream').val(data[10].toFixed(3));
		//$('#saveDataIndicator').text(data[2]);
  
		var x = Date.now();
		//alert(x);
		/* (flowRateGauge_1.series[0].points[0]).update(data[1].mass_flow);
		(flowRateGauge_2.series[0].points[0]).update(data[2].mass_flow);
		(flowRateGauge_3.series[0].points[0]).update(data[3].mass_flow);
		(flowRateGauge_4.series[0].points[0]).update(data[4].mass_flow); */
		
		shift = (smuOutputsContainer1.series[0]).data.length > 100;

		smuOutputsContainer1.series[0].addPoint((data[8]), true, shift)
		smuOutputsContainer2.series[0].addPoint((data[6]), true, shift)
		smuOutputsContainer3.series[0].addPoint((data[5]), true, shift)
		adcOutputsContainer1.series[0].addPoint((data[9]), true, shift)
		adcOutputsContainer2.series[0].addPoint((data[10]), true, shift)
		adcOutputsContainer3.series[0].addPoint((data[10]-data[9]), true, shift)

		


	});
}, 1000);

var smuDataCharts = {
	chart: {
		type: 'spline',
		animation: Highcharts.svg,
		marginRight: 10,
		//events: {
			//load: function() {
				//var series = this.series[0];

				//setInterval(function () {
					//var x = (new Date()).getTime(),
					//y = Math.random();
					//series.addPoint([x,y], true, true);
				//}, 1000);
			//}
		//}
	},

	title: {
		text: 'Data'
	},

	yAxis: {
		title: {
			text: 'Value'
		},
		plotLine: [{
			value: 0,
			width: 1,
			color: '#808080'
		}]
	},
	tooltip: {
		formatter: function () {
		return '<b>' + this.series.name + '</b><br/>' +
		   //Highcharts.dateFormat('%Y-%m-%d %H:%M:%S', this.x) + '<br/>' +
		   Highcharts.numberFormat(this.y, 2);
		}
	},
	plotOptions: {
		area: {
		   pointStart: 1940,
		   marker: {
			  enabled: false,
			  symbol: 'circle',
			  radius: 2,
			  
			  states: {
				 hover: {
					enabled: true
				 }
			  }
		   }
		}
	},
	 legend: {
		 enabled: false
	 },
	 exporting: {
		 enabled: true
	 },
	 series: [{
		name: 'Random data',
		data: []
	 }],
};

var smuOutputsContainer1 = Highcharts.chart('container-outputs1', Highcharts.merge(smuDataCharts));
smuOutputsContainer1.setTitle({text: 'Hotwire Temperature'});
var smuOutputsContainer2 = Highcharts.chart('container-outputs2', Highcharts.merge(smuDataCharts));
smuOutputsContainer2.setTitle({text: 'Hotwire Voltage'});
var smuOutputsContainer3 = Highcharts.chart('container-outputs3', Highcharts.merge(smuDataCharts));
smuOutputsContainer3.setTitle({text: 'Hotwire Current'});
var adcOutputsContainer1 = Highcharts.chart('container-outputs4', Highcharts.merge(smuDataCharts));
adcOutputsContainer1.setTitle({text: 'Upstream TP Voltage'});
var adcOutputsContainer2 = Highcharts.chart('container-outputs5', Highcharts.merge(smuDataCharts));
adcOutputsContainer2.setTitle({text: 'Downstream TP Voltage'});
var adcOutputsContainer3 = Highcharts.chart('container-outputs6', Highcharts.merge(smuDataCharts));
adcOutputsContainer3.setTitle({text: 'Difference Up-Down'});


});