
$(document).ready(function(){
	// // Set Up guage
	// var gaugeOptions = {
	// 	chart: {
	// 		type: 'solidgauge'
	// 	},  
	// 	title: null,  
	// 	pane: {
	// 		center: ['50%', '40%'],
	// 		size: '100%',
	// 		startAngle: -90,
	// 		endAngle: 90,
	// 		background: {
	// 			backgroundColor:
	// 				Highcharts.defaultOptions.legend.backgroundColor || '#EEE',
	// 			innerRadius: '60%',
	// 			outerRadius: '100%',
	// 			shape: 'arc'
	// 		}
	// 	},  
	// 	exporting: {
	// 		enabled: false
	// 	},  
	// 	tooltip: {
	// 		enabled: false
	// 	},  
	// 	// the value axis
	// 	yAxis: {
	// 		stops: [
	// 			[0.1, '#55BF3B'], // green
	// 			[0.7, '#DDDF0D'], // yellow
	// 			[0.9, '#DF5353'] // red
	// 		],
	// 		lineWidth: 0,
	// 		tickWidth: 0,
	// 		minorTickInterval: null,
	// 		tickAmount: 2,
	// 		title: {
	// 			y: -70
	// 		},
	// 		labels: {
	// 			y: 16
	// 		}
	// 	},  
	// 	plotOptions: {
	// 		solidgauge: {
	// 			dataLabels: {
	// 				y: 5,
	// 				borderWidth: 0,
	// 				useHTML: true
	// 			}
	// 		}
	// 	}
	//   };
	
	// var flowRateGuageOptions = {
	// 	yAxis: {
	// 		min: 0,
	// 		max: 500,
	// 	},  
	// 	credits: {
	// 		enabled: false
	// 	},  
	// 	series: [{
	// 		name: 'FlowRate',
	// 		data: [450],
	// 		dataLabels: {
	// 			format:
	// 				'<div style="text-align:center">' +
	// 				'<span style="font-size:25px">{y}</span><br/>' +
	// 				'<span style="font-size:12px;opacity:0.4">SLPM</span>' +
	// 				'</div>'
	// 		},
	// 		tooltip: {
	// 			valueSuffix: 'SLPM'
	// 		}
	// 	}]
	// };
	
	// var flowRateGauge_1 = Highcharts.chart('container-flowRateGauge_1', Highcharts.merge(gaugeOptions, flowRateGuageOptions));
	// var flowRateGauge_2 = Highcharts.chart('container-flowRateGauge_2', Highcharts.merge(gaugeOptions, flowRateGuageOptions));
	// var flowRateGauge_3 = Highcharts.chart('container-flowRateGauge_3', Highcharts.merge(gaugeOptions, flowRateGuageOptions));
	// var flowRateGauge_4 = Highcharts.chart('container-flowRateGauge_4', Highcharts.merge(gaugeOptions, flowRateGuageOptions));
	
	// HighCharts testing zone

	// var sensorOutputs = {
	// 	chart: {
	// 		type: 'spline',
	// 		animation: Highcharts.svg,

	// 		events: 
	// 	}
	// }


	//var flowRateGuage_1 = Highcharts.chart('container-flowRateGauge_1', Highcharts.merge(gaugeOptions, {
		// yAxis: {
		// 	min: 0,
		// 	max: 5,
		// },  
		// credits: {
		// 	enabled: false
		// },  
		// series: [{
		// 	name: 'FlowRate',
		// 	data: [80],
		// 	dataLabels: {
		// 		format:
		// 			'<div style="text-align:center">' +
		// 			'<span style="font-size:25px">{y}</span><br/>' +
		// 			'<span style="font-size:12px;opacity:0.4">SLPM</span>' +
		// 			'</div>'
		// 	},
		// 	tooltip: {
		// 		valueSuffix: 'SLPM'
		// 	}
		// }]  
	  //})); 
	
	
	  // Test Script with random guage values
	
	var smuDataCharts = {
		chart = {
			type: 'spline',
			animation: Highcharts.svg,
			marginRight: 10,

			events: {
				load: function() {
					var series = this.series[0];

					setInterval(function () {
						var x = (new Date()).getTime(),
						y = Math.random();
						series.addPoint([x,y], true, true);
					}, 1000);
				}
			}
		},

		title = {
			text: 'Data'
		},

		yAxis = {
			title: {
				text: 'Value'
			},
			plotLine: [{
				value: 0,
				width: 1,
				color: '#808080'
			}]
		},
		tooltip = {
			formatter: function () {
			return '<b>' + this.series.name + '</b><br/>' +
			   Highcharts.dateFormat('%Y-%m-%d %H:%M:%S', this.x) + '<br/>' +
			   Highcharts.numberFormat(this.y, 2);
			}
		},
		plotOptions = {
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
		 legend = {
			 enabled: false
		 },
		 exporting = {
			 enabled: false
		 },
		 series = [{
			name: 'Random data',
			data: (function () {
			   // generate an array of random data
			   var data = [],time = (new Date()).getTime(),i;
			   
			   for (i = -19; i <= 0; i += 1) {
				  data.push({
					 x: time + i * 1000,
					 y: Math.random()
				  });
			   }
			   return data;
			}())    
		 }],
	};

	//$('#container-outputs').highcharts(smuDataCharts);
	//var smuOutputDataPlot = Highcharts.chart('container-outputs', Highcharts.merge(smuDataCharts));

	//   // Bring life to the dials
	// setInterval(function () {
	// 	// Speed
	// 	var point,
	// 		newVal,
	// 		inc;
	  
	// 	if (flowRateGuage_1) {
	// 		point = flowRateGuage_1.series[0].points[0];
	// 		inc = Math.round((Math.random() - 0.5));
	// 		newVal = point.y + inc;
	  
	// 		if (newVal < 0 || newVal > 5) {
	// 			newVal = point.y - inc;
	// 		}
	  
	// 		point.update(newVal);
	// 	}
	  
	//   }, 2000);
	



	});