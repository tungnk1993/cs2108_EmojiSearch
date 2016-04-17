var query = [];
$(function() {
	console.log("loaded js");

	$(".emoji").click(function() {
		emo_id = $(this).attr("alt");
		console.log(emo_id);
		emo_url = $(this).attr("src");
		console.log(emo_url);

		append_html = "<img src=" + emo_url + ">";
		console.log(append_html);		
		$("#query-box").append(append_html);
		query.push(emo_id);
		console.log(query);
	});

	$("#clear").click(function() {
		console.log("Clear click");
		$("#query-box").html("");
		query = [];
		event.preventDefault();
	});

	$("#submit").click(function() {
		console.log("Submit click");
		console.log(query);

		// add random simulation
		random_emo = [2, 4, 18, 22];
		emo_name = ["Anger", "Surprise", "Neutral", "Happy"];
		random_number = Math.floor((Math.random() * 4));

		console.log(random_emo[random_number], emo_name[random_number]);
		$("#RF").html("Simutation = " + emo_name[random_number]);

		$.ajax({
			url: "http://127.0.0.1:8000/query/",
			type: "post",
			data: {"query" : JSON.stringify(query), "rf" : random_emo[random_number]},
			success: function(response) {
				console.log("AJAX OK");
				console.log(response);

				$("#result").html("");
				
				for (var i = 0; i < response.length; i++) 
				{
					var x = response[i];
					console.log(x);
					var image_html = '<div class="col-lg-2"><img src="/static/images/' + x + '" "></div>';
					$("#result").append(image_html);					
				}
			}
		});
		event.preventDefault();
	})
});