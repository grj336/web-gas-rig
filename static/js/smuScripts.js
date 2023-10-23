$(document).ready(function(){
	//var slider = $("#ex7").slider();
	var slider = $("#ex8").slider();
	//var slider = $("#pTermSlider").slider();
	//var slider = $("#iTermSlider").slider();
	//var slider = $("#dTermSlider").slider();
	//var slider = $("#temperatureSlider").slider();
	var source = 0
	$('#smuTabsDiv').hide();
	$('#ctTab').hide();
	
	//Current/Voltate Slider
/* 	$("#ex7-enabled").click(function() {
		if(this.checked) {
			$("#ex7").slider("enable");
		}
		else {
			$("#ex7").slider("disable");
		}
	}); */

/* 	$("#ex8-enabled").click(function() {
		if(this.checked) {
			$("#ex8").slider("enable");
		}
		else {
			$("#ex8").slider("disable");
		}
	}); */

	$("#ex7").on('change', function() {
		var a = $('#ex7').val();
		a = a/1000;
		$('#measuredCurrent').val(a);
		setTimeout(
		$.post("/updateSMUCurrent", {
			newCurrent: a,
			source: source,
		}), 500
		);
	});

	$("#smuPeriod").on('change', function() {
		var a = $('#smuPeriod').val();
		setTimeout(
		$.post("/updateSMUPeriod", {
			newPeriod: a,
		}), 500
		);
	});

	$("#smuDutyRatio").on('change', function() {
		var a = $('#smuDutyRatio').val();
		setTimeout(
		$.post("/updateSMUDutyRatio", {
			newRatio: a,
		}), 500
		);
	});


	$("#ex8").on('change', function() {
		var a = slideEvt.value;
		$('#measuredCurrent').val(a);
		setTimeout(
		$.post("/updateSMUCurrent", {
			newCurrent: a,
			source: source,
		}), 500
		);
	});

/* 	//Temperature Slider
	$("#temperatureSlider-enabled").click(function() {
		if(this.checked) {
			$("#temperatureSlider").slider("enable");
		}
		else {
			$("#temperatureSlider").slider("disable");
		}
	}); */
	
/* 	$("#temperatureSlider").on('slide', function(slideEvt) {
		var a = slideEvt.value;
		$('#temperatureInputBox').val(a);
	}); */

	//SMU Output State
	$('#smuOutputON').click(function(){
		//alert("In the function");
		if(this.checked){
			alert("SMU ON");
			$.post("/smuOnOff", {
				smuOutputState: 1,
			});
		}
		else{
			//alert("SMU Off");
			$.post("/smuOnOff", {
				smuOutputState: 0,
			});
			alert("SMU Off");
		}
	});

	$('#smuOutputPulse').click(function(){
		//alert("In the function");
		if(this.checked){
			alert("Pulse ON");
			$.post("/smuOutputPulse", {
				smuPulseState: 1,
			});
		}
		else{
			//alert("SMU Off");
			$.post("/smuOutputPulse", {
				smuPulseState: 0,
			});
			alert("Pulse Off");
		}
	});

	//SMU Source (Voltage or Current)
	$('#sourceSelector input').on('change', function(){
		$('#smuTabsDiv').show();
		var a = $('input[name=optradio]:checked', '#sourceSelector').val();
		if (a == "voltage"){
			source = 1;
		}
		else {
			source = 0;
		}
		$.post("/smuSourceSelect", {
			source: source,
		});
	});

	//SMU Sense Mode (2 or 4 Wire)
	$('#senseMode input').on('change', function(){
		//alert("Its changed")
		var a = $('input[name=senseRadio]:checked', '#senseMode').val();
		$.post("/smuSenseSelect", {
			senseMode: a,
		});
	});	



	$('#updateCompliance').click(function(){
		//alert("Updating compliance")
		var a = $('#complianceLimitValue').val();
		var b = $('input[name=optradio]:checked', '#sourceSelector').val();
		if(b == 'current'){
			//b = 'voltage';
			b = 0;
		}
		else if(b == 'voltage'){
			//b = 'current';
			b = 1;
		}
		else{
			alert("Error: No Source Selected");
			return
		}
		$.post("/updateCompliance", {
			newLimit: a,
			limitType: b,
		}, function(data){
			$('#complianceLimitValue').val(data);
		});
	});
}); 
