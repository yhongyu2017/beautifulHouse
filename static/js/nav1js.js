$("#select1 li").click(function () {
	$(this).addClass("selected").siblings().removeClass("selected");
		var copyThisA = $(this).clone();
		//console.log(copyThisA);
		if ($("#selectA").length > 0) {
			$("#selectA a").html($(this).text());
		} else {
			$(".select-result ul").append(copyThisA.attr("id", "selectA"));
		}
});
$("#select2 li").click(function() {
	$(this).addClass("selected").siblings().removeClass("selected");
	var copyThisB = $(this).clone();
	if ($("#selectB").length > 0) {
		$("#selectB a").html($(this).text());
	} else {
		$(".select-result ul").append(copyThisB.attr("id", "selectB"));
	}

});
$("#select3 li").click(function () {
	$(this).addClass("selected").siblings().removeClass("selected");
		var copyThisC = $(this).clone();
		if ($("#selectC").length > 0) {
			$("#selectC a").html($(this).text());
		} else {
			$(".select-result ul").append(copyThisC.attr("id", "selectC"));
		}
});
$("#select4 li").click(function () {
	$(this).addClass("selected").siblings().removeClass("selected");
		var copyThisC = $(this).clone();
		if ($("#selectD").length > 0) {
			$("#selectD a").html($(this).text());
		} else {
			$(".select-result ul").append(copyThisC.attr("id", "selectD"));
		}
});
$("#selectA").live("click", function () {
	$(this).remove();
	$("#select1 li").removeClass("selected");
});
$("#selectB").live("click", function () {
	$(this).remove();
	$("#select2 li").removeClass("selected");
});
// $(".select-result ul").delegate("li","click", function(){
//         var type = $(this).attr("date-type");
//         $(this).fadeOut();
//         $("#select2 li[date-type='" + type + "']").removeClass("selected");
//     });
$("#selectC").live("click", function () {
	$(this).remove();
	$("#select3 li").removeClass("selected");
});
$("#selectD").live("click", function () {
	$(this).remove();
	$("#select4 li").removeClass("selected");
});