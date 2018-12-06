//menu

$(document).ready(function(){
	//view-img
$(".viewcon").find("img").each(function(index, element) {
        if($(this).width() > 950) {
	$(this).css({"height":"auto","width":"100%"});
		}
    });
	
$('.bottomnav a:last').css('border',0);
$('.news_list li:odd').addClass('newseven');
$('.pronav a:last').css('border',0);
$('.menu li:last a').css('border',0);

promain();
function promain(){
$('.case .iproimg').hover(function(){
	$(this).children('p,font').stop(true,true).slideDown()},function(){$(this).children('p,font').stop(true,true).slideUp();
	
	}
	
	)
}

//index-nav
$('.menu li').mouseover(function(){
	$(this).find('.nav').stop(true,true).slideDown();
	$(this).children("a").addClass("cur");
	});
$('.menu li').mouseleave(function(){
	$(this).find('.nav').stop(true,true).slideUp('fast');
	$(this).children("a").removeClass("cur");
	});

//index-product
$('.product a').hover(
function(){
	$(this).children('.pro_name').stop(true,true).slideDown()
	},function(){
		$(this).children('.pro_name').stop(true,true).slideUp()}
)

	//index-news
	$('.news ul li').mouseover(function(){
		$(this).addClass('one').siblings().removeClass('one');
		})
	//fixed
	$('.codepic').hover(function(){$('.code').fadeIn()},function(){$('.code').fadeOut()});
    $('.backup,.topbut').click(function(){
        $('body,html').animate({scrollTop:0},500)
    });
    $(".backup").hide();
    $(function () {
        $(window).scroll(function(){
            if ($(window).scrollTop()>500){
                $(".backup").fadeIn(1000);
            }else{
                $(".backup").fadeOut(1000);
            }
        })
   })
/*	$('.nav').each(function(index, element) {
		$(this).children('a').last().css('border',0)
    });
	$('.proTwo li').last().each(function(index, element) {
		$(this).children('a').css('border',0)
    });
*/	
})