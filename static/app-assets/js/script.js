function settingLocalRoute(route){
    console.log(route);
    localStorage.setItem("loginRoute" , route);
}
$(document).ready(function(){
    document.getElementById('loader-div').style.display='none';
});


//(function($){
//    $.fn.extend({
//        donetyping: function(callback,timeout){
//            timeout = timeout || 100; // 1 second default timeout
//            var timeoutReference,
//                doneTyping = function(el){
//                    if (!timeoutReference) return;
//                    timeoutReference = null;
//                    callback.call(el);
//                };
//            return this.each(function(i,el){
//                var $el = $(el);
//
//                // Chrome Fix (Use keyup over keypress to detect backspace)
//                // thank you @palerdot
//                $el.is(':input') && $el.on('keyup keypress paste',function(e){
//                    // This catches the backspace button in chrome, but also prevents
//                    // the event from triggering too preemptively. Without this line,
//                    // using tab/shift+tab will make the focused element fire the callback.
//                    if(e.keyCode==8){
//                        $('#search-list').hide();
//                    }
//                    if (e.type=='keyup' && e.keyCode!=8){$('#search-list').show();return;}
//
//                    // Check if timeout has been set. If it has, "reset" the clock and
//                    // start over again.
//                    if (timeoutReference) clearTimeout(timeoutReference);
//                    timeoutReference = setTimeout(function(){
//                        // if we made it here, our timeout has elapsed. Fire the
//                        // callback
//                        doneTyping(el);
//                    }, timeout);
//                }).on('input',function(){
//                    // If we can, fire the event since we're leaving the field
//                    doneTyping(el);
//                });
//            });
//        }
//    });
//})(jQuery);

function onInput(){
    if(document.getElementById('search_name').value==''){
        $('#search-list').hide();
    }
    else{
        $('#search-list').empty();
        $('#search-list').show();
        console.log("doing",document.getElementById('search_name').value);
        var searchName = document.getElementById('search_name').value;
        var channel_type=document.getElementById('channel_name').value;
        if(channel_type=='youtube'&&searchName!=''){
            $.ajax({
                type:'GET',
                url:'/getYoutubeSearchDropDownResults/'+searchName,
                success:function(res){
                    $('#search-list').empty();
                    for(var i =0;i<res.results.length;i++){
                        var options='<li id="'+res.results[i].channel_id+'" onclick="displayThisChannel(this.id,this)"><div style="display:flex;justify-content:space-between;"><div>'+res.results[i].title+'</div><div><img src="'+res.results[i].channel_img+'" width="30px" height="30px"></div></div></li>';
                        $('#search-list').append(options);
                    }

                }
            });
        }
        else if(channel_type=='twitter'&&searchName!=''){

            $.ajax({
                    type:'GET',
                    url:'/getTwitterSearchDropDownResults/'+searchName,
                    success:function(res){
                         console.log(res);
                        $('#search-list').empty();
                        for(var i =0;i<res.results.length;i++){
                            var options='<li id="'+res.results[i].screen_name+'" onclick="displayThisChannel(this.id,this)"><div style="display:flex;justify-content:space-between;"><div>'+res.results[i].screen_name+'</div><div><img src="'+res.results[i].channel_img+'" width="30px" height="30px"></div></div></li>';
                            $('#search-list').append(options);
                        }

                    }
            });

        }
        else{
            $('#search-list').empty();
        }
    }

};






//var typingTimer;                //timer identifier
//var doneTypingInterval = 300;  //time in ms, 5 second for example
//var $input = $('#search_name');
//
////on keyup, start the countdown
//$input.on('keyup', function (event) {
//  clearTimeout(typingTimer);
//  typingTimer = setTimeout(doneTyping, doneTypingInterval);
//});
//
////on keydown, clear the countdown
//$input.on('keydown', function () {
//  clearTimeout(typingTimer);
//});

//user is "finished typing," do something
//function doneTyping () {
//    var searchName = document.getElementById('search_name').value;
//    var channel_type=document.getElementById('channel_name').value;
//    if(channel_type=='youtube'&&searchName!=''){
//        $.ajax({
//            type:'GET',
//            url:'/getYoutubeSearchDropDownResults/'+searchName,
//            success:function(res){
//                $('#search-list').empty();
//                for(var i =0;i<res.results.length;i++){
//                    var options='<li id="'+res.results[i].channel_id+'" onclick="displayThisChannel(this.id,this)"><div style="display:flex;justify-content:space-between;"><div>'+res.results[i].title+'</div><div><img src="'+res.results[i].channel_img+'" width="30px" height="30px"></div></div></li>';
//                    $('#search-list').append(options);
//                }
//
//            }
//        });
////    }
//
//}

//------------------------------------------------------------
$('.what-next-button').click(function () {
    $('html,body').animate({
            scrollTop: $(window).scrollTop() + 400},
        'slow');
});
function settingDataDisplay() {
    document.getElementsByClassName('data-display')[0].style.display='none';
}
var massPopChart =null;

// function for calculating rating of influencer

function calculateRating(data) {
    if(data==0){
        return 0;
    }
    if(data<100){
        return 1;
    }
    else if(data>=100&&data<500){
        return 1.5;
    }
    else if(data>=500&&data<1000){
        return 2;
    }
    else if(data>=1000&&data<5000){
        return 2.5;
    }
    else if(data>=5000&&data<10000){
        return 3;
    }
    else if(data>=10000&&data<20000){
        return 4;
    }
    else if(data>=20000&&data<50000){
        return 4.5;
    }
    else{
        return 5;
    }
}

//----------------------------------------------

// function for getting the chart rendered with json data received

function getChart(label,like) {
    Chart.pluginService.register({
        beforeDraw: function (chart, easing) {
            if (chart.config.options.chartArea && chart.config.options.chartArea.backgroundColor) {
                var helpers = Chart.helpers;
                var ctx = chart.chart.ctx;
                var chartArea = chart.chartArea;

                ctx.save();
                ctx.fillStyle = chart.config.options.chartArea.backgroundColor;
                ctx.fillRect(chartArea.left, chartArea.top, chartArea.right - chartArea.left, chartArea.bottom - chartArea.top);
                ctx.restore();
            }
        }
    });

    document.getElementById('mainChart').innerText='';
    $('#mainChart').append('<canvas id="myChart"></canvas>');
    var myChart = document.getElementById('myChart').getContext('2d');

    Chart.defaults.global.defaultFontColor = "#fff";
    var fontSizeT=18;
    var aspectRatio=true;
    if($(window).width()<748){
        aspectRatio=false;
        fontSizeT=10;
    }
    massPopChart = new Chart(myChart, {
        type:'line',
        data:{
            labels:label,
            datasets:[{
                label:'NUMBER OF LIKES',
                data: like,
                backgroundColor:[
                    'rgba(255,99,132,0.6)',
                    'rgba(255,99,132,0.6)',
                    'rgba(255,99,132,0.6)',
                    'rgba(255,99,132,0.6)',
                    'rgba(255,99,132,0.6)'
                ],
                borderWidth: 1,
                borderColor: '#b8b8b8',
                hoverBorderWidth: 3,
                hoverBorderColor: '#00f01a',
                hoverPointer: 'cursor'
            }]
        },
        options:{
            responsive:true,
            maintainAspectRatio:aspectRatio,
            title:{
                display:true,
                text:'LIKES VS POSTS'
            },
            legend:{
                position:'bottom',
                display: true,
                labels: {
                fontColor: "white",
                fontSize: fontSizeT
                }
            },
            scales: {
                xAxes: [{
                    scaleLabel: {
                        display: true,
                        labelString: 'LAST FIVE POSTS'
                    },
                    ticks: {
                        autoSkip: false,
                        maxRotation: 90,
                        minRotation: 90
                    }
                }],
                yAxes: [{
                    scaleLabel: {
                        display: true,
                        labelString: 'NUMBER OF LIKES'
                    }
                }]
            },
            chartArea: {
                backgroundColor: 'rgb(255, 255, 255)'
            },
            plugins: {
                datalabels: {
                    anchor: 'end',
                    align: 'end',
                    backgroundColor: null,
                    borderColor: null,
                    borderRadius: 4,
                    borderWidth: 1,
                    color: '#223388',
                    font: function (context) {
                        var width = context.chart.width;
                        var size = Math.round(width / 32);
                        return {
                            size: size,
                            weight: 600
                        };
                    },
                    offset: 4,
                    padding: 0,
                    formatter: function (value) {
                        return Math.round(value * 10) / 10
                    }
                }
            }
        }
    });
}

//----------------------------------------------


// function for calculating average likes, comments and views

function calcaulateAverage(data) {
    var arr={};
    var views=0;
    var likes=0;
    var comments=0;
    for(var i=0;i<data.length;i++){
        views=views+data[i].no_of_post_views;
        likes=likes+data[i].no_of_post_likes;
        comments=comments+data[i].no_of_post_comments;
    }
    arr.avg_views=Math.round(views/data.length);
    arr.avg_likes=Math.round(likes/data.length);
    arr.avg_comments=Math.round(comments/data.length);
    if(isNaN(arr.avg_likes)){
        arr.avg_likes=0;
    }
    if(isNaN(arr.avg_views)){
        arr.avg_views=0;
    }
    if(isNaN(arr.avg_comments)){
        arr.avg_comments=0;
    }
    return arr;
}

//----------------------------------------------


//function for conversion of followers, views, likes and comments into M and K

function convertion(data) {
    var value;
    if(data>999999){

        data=data/1000000;
        var m = Math.round(data * 100) / 100;
        value = m+'M';
    }
    else if(data>1000){
        data=data/1000;
        var m = Math.round(data * 100) / 100;
        value=m+'K';
    }
    else{
        value=data
    }
    return value;
}

//-------------------------------------------------

// function to check empty object


function isEmpty(obj) {
    for (var key in obj) {
        if (Object.prototype.hasOwnProperty.call(obj, key)) {
            return false;
        }
    }
    return true;
}


//--------------------------------------------------
//function for calculating score of an influencer

function calculateScore(followers,Rate){

    var pointFollowers=0;
    var pointEngagementRate=0;
    if(Rate>4.5){
        pointEngagementRate=10;
    }
    else if(Rate>4){
        pointEngagementRate=9;
    }
    else if(Rate>3.5){
        pointEngagementRate=8;
    }
    else if(Rate>3){
        pointEngagementRate=7;
    }
    else if(Rate>2.5){
        pointEngagementRate=6;
    }
    else if(Rate>2){
        pointEngagementRate=5;
    }
    else if(Rate>1.5){
        pointEngagementRate=4;
    }
    else if(Rate>1){
        pointEngagementRate=3;
    }
    else if(Rate>0.5){
        pointEngagementRate=2;
    }
    else{
        pointEngagementRate=1;
    }

    if(followers>100000000){
        pointFollowers=10;
    }
    else if(followers>10000000){
        pointFollowers=9;
    }
    else if(followers>5000000){
        pointFollowers=8;
    }
    else if(followers>1000000){
        pointFollowers=7;
    }
    else if(followers>250000){
        pointFollowers=6;
    }
    else if(followers>50000){
        pointFollowers=5;
    }
    else if(followers>5000){
        pointFollowers=4;
    }
    else if(followers>2500){
        pointFollowers=3;
    }
    else if(followers>1000){
        pointFollowers=2;
    }
    else{
        pointFollowers=1;
    }
    return ((pointFollowers+pointEngagementRate)/2);
}

//--------------------------------------------------

// rendering youtube category graph

function renderYoutubeCategoryGraph(channelId){

    $.ajax({
            type:'GET',
            url:'/getYoutubeVideoCategory/'+channelId,
            success:function(res){
                data=res.results.data;
                console.log("graph data",res);
                var labels=[];
                var dat=[];
                for(var i=0;i<data.length;i++){
                    dat.push(data[i].category_count);
                    labels.push(data[i].video_cat_name);
                }

                if(res.results.data.length!=0&&res.results.data.length<=5){
                    $('#myChart').show();
                    var data2 = {
                        labels: labels,
                        datasets: [
                          {
                            data: dat,
                            backgroundColor: [
                              "#FAEBD7",
                              "#DCDCDC",
                              "#E9967A",
                              "#F5DEB3",
                              "#9ACD32"
                            ],
                            borderColor: [
                              "#E9DAC6",
                              "#CBCBCB",
                              "#D88569",
                              "#E4CDA2",
                              "#89BC21"
                            ],
                            borderWidth: [1, 1, 1, 1, 1]
                          }
                        ]
                     };
                    var aspectRatio=true;
                    var fontSizeT=18;
                    if($(window).width()<748){
                        aspectRatio=false;
                        fontSizeT=10
                    }
                    var options = {
                        innerRadius:10,
                        responsive: true,
                        maintainAspectRatio:aspectRatio,
                        title: {
                          display: true,
                          position: "top",
                          text: "Video Category Count",
                          fontSize: fontSizeT,
                          fontColor: "white"
                        },
                        legend: {
                          display: true,
                          position: "top",
                          labels: {
                            fontColor: "white",
                            fontSize: fontSizeT
                          }
                        }
                    };
                    document.getElementById('mainChart').innerText='';
                    $('#mainChart').append('<canvas id="myChart"></canvas>');

                    var chart1 = new Chart('myChart', {
                        type: "doughnut",
                        data: data2,
                        options: options
                    });

                }
                else if(res.results.data.length!=0&&res.results.data.length>5){
                    $('#myChart').show();
                    var aspectRatio=true;
                    var fontSizeT=18;
                    if($(window).width()<748){
                        aspectRatio=false;
                        fontSizeT=10
                    }
                    var data2 = {
                        labels: labels,
                        datasets: [
                          {
                            data: dat,
                            backgroundColor: [
                              "#FAEBD7",
                              "#DCDCDC",
                              "#E9967A",
                              "#F5DEB3",
                              "#9ACD32"
                            ],
                            borderColor: [
                              "#E9DAC6",
                              "#CBCBCB",
                              "#D88569",
                              "#E4CDA2",
                              "#89BC21"
                            ],
                            borderWidth: [1, 1, 1, 1, 1]
                          }
                        ]
                     };
                    var options = {
                        innerRadius:10,
                        responsive: true,
                        maintainAspectRatio:aspectRatio,
                        title: {
                          display: true,
                          position: "top",
                          text: "Video Category Count",
                          fontSize: fontSizeT,
                          fontColor: "white"
                        },
                        legend: {
                          display: true,
                          position: "top",
                          labels: {
                            fontColor: "white",
                            fontSize: fontSizeT
                          }
                        }
                    };
                    document.getElementById('mainChart').innerText='';
                    $('#mainChart').append('<canvas id="myChart"></canvas>');
                    var chart1 = new Chart('myChart', {
                        type: "bar",
                        data: data2,
                        options: options
                    });

                }




            }
        });

}

//--------------------------------------------------
// function youtube channel when clicked

function displayThisChannel(x,y){
    console.log(x,y.childNodes[0].childNodes[0].innerText);
    $('#search-list').hide();
    $('#search_name').val(y.childNodes[0].childNodes[0].innerText);
    document.getElementById("check_button_inside").disabled = true;
    document.getElementById('loader-div').style.display='block';
    if($('#channel_name').val()=='youtube'){
        $.ajax({
                type: 'GET',
                url: "/getYoutubeUserFromYoutubeApi/"+x,
                success:function(res){
                    if(res.results.data.length==0){
                        document.getElementById("check_button_inside").disabled = false;
                        document.getElementById('loader-div').style.display='none';
                        document.getElementsByClassName('message')[0].style.display='flex';
                        document.getElementsByClassName('errorMessage')[0].childNodes[1].innerText='Cannot Get Data For This User';

                        setTimeout(function(){
                            document.getElementsByClassName('message')[0].style.display='none';
                            document.getElementsByClassName('errorMessage')[0].childNodes[1].innerText='';
                        },3000);
                        return;
                    }
                    document.getElementById('loader-div').style.display='none';
                    data=res.results.data[0];
                    console.log("hello");
                    console.log(data);
                    influencer_name=data.title;
                    business_category_name=data.desc;
                    if(business_category_name.length>20){
                        business_category_name='';
                    }
                    influencer_image=data.channel_img;
                    total_followers=data.subscriberCount_gained;
                    // engagement rate calculation
                    var engagementRate=((data.total_100video_comments+data.total_100video_views+data.total_100video_likes)/(total_followers)).toFixed(2);
                    console.log(engagementRate);

                    //------------------------------
                    var score=calculateScore(total_followers,engagementRate);
                    var loc=window.location.href;
                    loc=loc.split('/');
                    loc=loc[loc.length-1];
                    if(loc=='influencer'){
                        if(score<4){
                        document.getElementsByClassName('score-4')[0].style.display="none";
                        document.getElementsByClassName('score-not-4')[0].style.display="block";
                        }
                        else{
                            document.getElementsByClassName('score-4')[0].style.display="block";
                            document.getElementsByClassName('score-not-4')[0].style.display="none";
                        }
                    }
                    console.log(score);
                    total_followers=convertion(total_followers);
                    average_views=convertion(data.total_100video_views);
                    average_likes=convertion(data.total_100video_likes);
                    average_comments=convertion(data.total_100video_comments);
                    if(average_comments==0){
                        average_comments='N/A';
                    }
                    if(average_likes==0){
                        average_likes='N/A';
                    }
                    if(average_views==0){
                        average_views='N/A';
                    }
                    document.getElementsByClassName('message')[0].style.display='none';
                    document.getElementsByClassName('data-display')[0].style.display='block';
                    document.getElementsByClassName('influencer-name')[0].childNodes[1].innerText=influencer_name;
                    document.getElementsByClassName("influence-img")[0].childNodes[1].src=influencer_image;
                    document.getElementsByClassName("influence-rating")[0].childNodes[1].innerText=engagementRate+'%';
                    document.getElementsByClassName("influence-followers")[0].childNodes[1].innerText=total_followers;
                    document.getElementsByClassName("influence-average-views")[0].childNodes[1].innerText=average_views;
                    document.getElementsByClassName("influence-average-likes")[0].childNodes[1].innerText=average_likes;
                    document.getElementsByClassName("influence-average-comments")[0].childNodes[1].innerText=average_comments;
                    console.log();
                    var label=[];
                    var like=[];
                    $('#myChart').hide();
                    renderYoutubeCategoryGraph(x);
                    var influencerItem = document.getElementsByClassName("influence-rating");
                    var engagementBar = document.getElementsByClassName('engagement-bar');
                    var max=4;
                    var min=0.5;
                    var diff=(max-min)/3;
                    for(var i =0;i<influencerItem.length;i++){
                        var value = parseFloat(influencerItem[i].innerText.split(' ')[0]);
                        if(value>=max){
                            engagementBar[i].childNodes[1].style.backgroundColor="rgb(0, 133, 15)";
                            engagementBar[i].childNodes[3].style.backgroundColor="rgb(0, 133, 15)";
                            engagementBar[i].childNodes[5].style.backgroundColor="rgb(0, 133, 15)";
                            engagementBar[i].childNodes[7].style.backgroundColor="rgb(0, 133, 15)";
                            engagementBar[i].childNodes[9].style.backgroundColor="rgb(0, 133, 15)";
                        }
                        else if(value<max&&value>max-diff){
                            engagementBar[i].childNodes[1].style.backgroundColor="rgb(96, 165, 55)";
                            engagementBar[i].childNodes[3].style.backgroundColor="rgb(96, 165, 55)";
                            engagementBar[i].childNodes[5].style.backgroundColor="rgb(96, 165, 55)";
                            engagementBar[i].childNodes[7].style.backgroundColor="rgb(96, 165, 55)";
                            engagementBar[i].childNodes[9].style.backgroundColor="lightgrey";
                        }
                        else if(value<=max-diff&&value>min+diff){
                            engagementBar[i].childNodes[1].style.backgroundColor="rgb(129, 212, 82)";
                            engagementBar[i].childNodes[3].style.backgroundColor="rgb(129, 212, 82)";
                            engagementBar[i].childNodes[5].style.backgroundColor="rgb(129, 212, 82)";
                            engagementBar[i].childNodes[7].style.backgroundColor="lightgrey";
                            engagementBar[i].childNodes[9].style.backgroundColor="lightgrey";
                        }
                        else if(value<=min+diff&&value>min){
                            engagementBar[i].childNodes[1].style.backgroundColor="rgb(230, 169, 0)";
                            engagementBar[i].childNodes[3].style.backgroundColor="rgb(230, 169, 0)";
                            engagementBar[i].childNodes[5].style.backgroundColor="lightgrey";
                            engagementBar[i].childNodes[7].style.backgroundColor="lightgrey";
                            engagementBar[i].childNodes[9].style.backgroundColor="lightgrey";
                        }
                        else if(value<=min){
                            engagementBar[i].childNodes[1].style.backgroundColor="rgb(204,0,0)";
                            engagementBar[i].childNodes[3].style.backgroundColor="lightgrey";
                            engagementBar[i].childNodes[5].style.backgroundColor="lightgrey";
                            engagementBar[i].childNodes[7].style.backgroundColor="lightgrey";
                            engagementBar[i].childNodes[9].style.backgroundColor="lightgrey";
                        }
                    }


                    setTimeout(function () {

                        document.getElementsByClassName('score-display-name')[0].childNodes[1].innerText='Your Influencer Score Is';
                        $('html,body').animate({
                                scrollTop: $(".data-display").offset().top},
                            'slow');
                        var progressbar = $('#progress_bar');
                        max = progressbar.attr('aria-valuemax');
                        time = 100;
                        value = 0;
                        numberValue=0;
                        var loading = function () {
                            value += 2;
                            numberValue=Math.floor((value/2)/5);
                            document.getElementById('progress_bar').style.width=value+'%';
                            document.getElementsByClassName('score-display-number')[0].childNodes[1].innerText=numberValue;
                            document.getElementsByClassName('score-display-name')[0].childNodes[1].innerText='Calculating Your Score';
                            if(value<20){
                                document.getElementById('progress_bar').style.backgroundColor='red';
                                document.getElementsByClassName('score-display-number')[0].childNodes[1].style.color='red';
                            }
                            else if(value>=20&&value<=30){
                                document.getElementById('progress_bar').style.backgroundColor='orange';
                                document.getElementsByClassName('score-display-number')[0].childNodes[1].style.color='orange';
                            }
                            else if(value>30&&value<=40){
                                document.getElementById('progress_bar').style.backgroundColor='yellow';
                                document.getElementsByClassName('score-display-number')[0].childNodes[1].style.color='yellow';
                            }
                            else if(value>40&&value<=50){
                                document.getElementById('progress_bar').style.backgroundColor='limegreen';
                                document.getElementsByClassName('score-display-number')[0].childNodes[1].style.color='limegreen';
                            }
                            else{
                                document.getElementById('progress_bar').style.backgroundColor='rgb(80, 181, 30)';
                                document.getElementsByClassName('score-display-number')[0].childNodes[1].style.color='rgb(80, 181, 30)';
                            }
                            if(value>=100){
                                value=0;
                                numberValue=0;
                                document.getElementById('progress_bar').style.width='0%';
                                document.getElementById('progress_bar').style.backgroundColor='limegreen';
                            }
                        };
                        var animate = setInterval(function () {
                            loading();
                        }, time);
                        setTimeout(function () {
                            clearInterval(animate);
                            document.getElementById('progress_bar').style.width=(score*10)+'%';
                            document.getElementsByClassName('score-display-number')[0].childNodes[1].innerText=score;
                            document.getElementsByClassName('score-display-name')[0].childNodes[1].innerText='Your Influencer Score Is';
                            if(score>5){
                                document.getElementById('progress_bar').style.backgroundColor='green';
                                document.getElementsByClassName('score-display-number')[0].childNodes[1].style.color='green';
                            }
                            else if(score>4){
                                document.getElementById('progress_bar').style.backgroundColor='limegreen';
                                document.getElementsByClassName('score-display-number')[0].childNodes[1].style.color='limegreen';
                            }
                            else if(score>3){
                                document.getElementById('progress_bar').style.backgroundColor='yellow';
                                document.getElementsByClassName('score-display-number')[0].childNodes[1].style.color='yellow';
                            }
                            else if(score>2){
                                document.getElementById('progress_bar').style.backgroundColor='orange';
                                document.getElementsByClassName('score-display-number')[0].childNodes[1].style.color='orange';
                            }
                            else{
                                document.getElementById('progress_bar').style.backgroundColor='red';
                                document.getElementsByClassName('score-display-number')[0].childNodes[1].style.color='red';
                            }

                            document.getElementsByClassName('what-next-button')[0].style.display='block';
                            document.getElementById("check_button_inside").disabled = false;
                        },10000);
                    },500);

                }
            });
    }
    else if($('#channel_name').val()=='twitter'){
        $.ajax({
                type: 'GET',
                url: "/getTwitterUserFromTwitterApi/"+x,
                success:function(res){
                    if(res.results.data.length==0){
                        document.getElementById("check_button_inside").disabled = false;
                        document.getElementById('loader-div').style.display='none';
                        document.getElementsByClassName('message')[0].style.display='flex';
                        document.getElementsByClassName('errorMessage')[0].childNodes[1].innerText='Cannot Get Data For This User';

                        setTimeout(function(){
                            document.getElementsByClassName('message')[0].style.display='none';
                            document.getElementsByClassName('errorMessage')[0].childNodes[1].innerText='';
                        },3000);
                        return;
                    }
                    document.getElementById('loader-div').style.display='none';
                    data=res.results.data[0];
                    console.log("hello");
                    console.log(data);
                    influencer_name=data.title;
                    business_category_name=data.desc;
                    if(business_category_name.length>20){
                        business_category_name='';
                    }
                    influencer_image='../static/images/imageNotAvailable.jpeg';
                    total_followers=data.subscriberCount_gained;
                    // engagement rate calculation
                    var engagementRate=((data.total_100video_comments+data.total_100video_views+data.total_100video_likes)/(total_followers)).toFixed(2);
                    console.log(engagementRate);

                    //------------------------------
                    var score=calculateScore(total_followers,engagementRate);
                    var loc=window.location.href;
                    loc=loc.split('/');
                    console.log(loc);
                    loc=loc[loc.length-1];
                    if(loc=='influencer'){
                        if(score<4){
                        document.getElementsByClassName('score-4')[0].style.display="none";
                        document.getElementsByClassName('score-not-4')[0].style.display="block";
                        }
                        else{
                            document.getElementsByClassName('score-4')[0].style.display="block";
                            document.getElementsByClassName('score-not-4')[0].style.display="none";
                        }
                    }

                    console.log(score);
                    total_followers=convertion(total_followers);
                    average_views=convertion(data.total_100video_views);
                    average_likes=convertion(data.total_100video_likes);
                    average_comments=convertion(data.total_100video_comments);
                    if(average_comments==0){
                        average_comments='N/A';
                    }
                    if(average_likes==0){
                        average_likes='N/A';
                    }
                    if(average_views==0){
                        average_views='N/A';
                    }
                    document.getElementsByClassName('message')[0].style.display='none';
                    document.getElementsByClassName('data-display')[0].style.display='block';
                    document.getElementsByClassName('influencer-name')[0].childNodes[1].innerText=influencer_name;
                    document.getElementsByClassName("influence-img")[0].childNodes[1].src=influencer_image;
                    document.getElementsByClassName("influence-rating")[0].childNodes[1].innerText=engagementRate+'%';
                    document.getElementsByClassName("influence-followers")[0].childNodes[1].innerText=total_followers;
                    document.getElementsByClassName("influence-average-views")[0].childNodes[1].innerText=average_views;
                    document.getElementsByClassName("influence-average-likes")[0].childNodes[1].innerText=average_likes;
                    document.getElementsByClassName("influence-average-comments")[0].childNodes[1].innerText=average_comments;
                    console.log();
                    var label=[];
                    var like=[];
                    $('#myChart').hide();
//                    if(isEmpty(data[0].post_data)){
//                        document.getElementsByClassName("chart-mine")[0].style.display="none";
//                    }
//                    else{
//                        document.getElementsByClassName("chart-mine")[0].style.display="block";
//                        for(var j=0;j<data[0].post_data.length&&j<5;j++){
//                            label.push((data[0].post_data[j].post_time).substring(0,10));
//                            like.push(data[0].post_data[j].no_of_post_likes);
//                        }
//                        getChart(label,like);
//                    }
                    var influencerItem = document.getElementsByClassName("influence-rating");
                    var engagementBar = document.getElementsByClassName('engagement-bar');
                    var max=4;
                    var min=0.5;
                    var diff=(max-min)/3;
                    for(var i =0;i<influencerItem.length;i++){
                        var value = parseFloat(influencerItem[i].innerText.split(' ')[0]);
                        if(value>=max){
                            engagementBar[i].childNodes[1].style.backgroundColor="rgb(0, 133, 15)";
                            engagementBar[i].childNodes[3].style.backgroundColor="rgb(0, 133, 15)";
                            engagementBar[i].childNodes[5].style.backgroundColor="rgb(0, 133, 15)";
                            engagementBar[i].childNodes[7].style.backgroundColor="rgb(0, 133, 15)";
                            engagementBar[i].childNodes[9].style.backgroundColor="rgb(0, 133, 15)";
                        }
                        else if(value<max&&value>max-diff){
                            engagementBar[i].childNodes[1].style.backgroundColor="rgb(96, 165, 55)";
                            engagementBar[i].childNodes[3].style.backgroundColor="rgb(96, 165, 55)";
                            engagementBar[i].childNodes[5].style.backgroundColor="rgb(96, 165, 55)";
                            engagementBar[i].childNodes[7].style.backgroundColor="rgb(96, 165, 55)";
                            engagementBar[i].childNodes[9].style.backgroundColor="lightgrey";
                        }
                        else if(value<=max-diff&&value>min+diff){
                            engagementBar[i].childNodes[1].style.backgroundColor="rgb(129, 212, 82)";
                            engagementBar[i].childNodes[3].style.backgroundColor="rgb(129, 212, 82)";
                            engagementBar[i].childNodes[5].style.backgroundColor="rgb(129, 212, 82)";
                            engagementBar[i].childNodes[7].style.backgroundColor="lightgrey";
                            engagementBar[i].childNodes[9].style.backgroundColor="lightgrey";
                        }
                        else if(value<=min+diff&&value>min){
                            engagementBar[i].childNodes[1].style.backgroundColor="rgb(230, 169, 0)";
                            engagementBar[i].childNodes[3].style.backgroundColor="rgb(230, 169, 0)";
                            engagementBar[i].childNodes[5].style.backgroundColor="lightgrey";
                            engagementBar[i].childNodes[7].style.backgroundColor="lightgrey";
                            engagementBar[i].childNodes[9].style.backgroundColor="lightgrey";
                        }
                        else if(value<=min){
                            engagementBar[i].childNodes[1].style.backgroundColor="rgb(204,0,0)";
                            engagementBar[i].childNodes[3].style.backgroundColor="lightgrey";
                            engagementBar[i].childNodes[5].style.backgroundColor="lightgrey";
                            engagementBar[i].childNodes[7].style.backgroundColor="lightgrey";
                            engagementBar[i].childNodes[9].style.backgroundColor="lightgrey";
                        }
                    }


                    setTimeout(function () {

                        document.getElementsByClassName('score-display-name')[0].childNodes[1].innerText='Your Influencer Score Is';
                        $('html,body').animate({
                                scrollTop: $(".score-display").offset().top},
                            'slow');
                        var progressbar = $('#progress_bar');
                        max = progressbar.attr('aria-valuemax');
                        time = 100;
                        value = 0;
                        numberValue=0;
                        var loading = function () {
                            value += 2;
                            numberValue=Math.floor((value/2)/5);
                            document.getElementById('progress_bar').style.width=value+'%';
                            document.getElementsByClassName('score-display-number')[0].childNodes[1].innerText=numberValue;
                            document.getElementsByClassName('score-display-name')[0].childNodes[1].innerText='Calculating Your Score';
                            if(value<20){
                                document.getElementById('progress_bar').style.backgroundColor='red';
                                document.getElementsByClassName('score-display-number')[0].childNodes[1].style.color='red';
                            }
                            else if(value>=20&&value<=30){
                                document.getElementById('progress_bar').style.backgroundColor='orange';
                                document.getElementsByClassName('score-display-number')[0].childNodes[1].style.color='orange';
                            }
                            else if(value>30&&value<=40){
                                document.getElementById('progress_bar').style.backgroundColor='yellow';
                                document.getElementsByClassName('score-display-number')[0].childNodes[1].style.color='yellow';
                            }
                            else if(value>40&&value<=50){
                                document.getElementById('progress_bar').style.backgroundColor='limegreen';
                                document.getElementsByClassName('score-display-number')[0].childNodes[1].style.color='limegreen';
                            }
                            else{
                                document.getElementById('progress_bar').style.backgroundColor='rgb(80, 181, 30)';
                                document.getElementsByClassName('score-display-number')[0].childNodes[1].style.color='rgb(80, 181, 30)';
                            }
                            if(value>=100){
                                value=0;
                                numberValue=0;
                                document.getElementById('progress_bar').style.width='0%';
                                document.getElementById('progress_bar').style.backgroundColor='limegreen';
                            }
                        };
                        var animate = setInterval(function () {
                            loading();
                        }, time);
                        setTimeout(function () {
                            clearInterval(animate);
                            document.getElementById('progress_bar').style.width=(score*10)+'%';
                            document.getElementsByClassName('score-display-number')[0].childNodes[1].innerText=score;
                            document.getElementsByClassName('score-display-name')[0].childNodes[1].innerText='Your Influencer Score Is';
                            if(score>5){
                                document.getElementById('progress_bar').style.backgroundColor='green';
                                document.getElementsByClassName('score-display-number')[0].childNodes[1].style.color='green';
                            }
                            else if(score>4){
                                document.getElementById('progress_bar').style.backgroundColor='limegreen';
                                document.getElementsByClassName('score-display-number')[0].childNodes[1].style.color='limegreen';
                            }
                            else if(score>3){
                                document.getElementById('progress_bar').style.backgroundColor='yellow';
                                document.getElementsByClassName('score-display-number')[0].childNodes[1].style.color='yellow';
                            }
                            else if(score>2){
                                document.getElementById('progress_bar').style.backgroundColor='orange';
                                document.getElementsByClassName('score-display-number')[0].childNodes[1].style.color='orange';
                            }
                            else{
                                document.getElementById('progress_bar').style.backgroundColor='red';
                                document.getElementsByClassName('score-display-number')[0].childNodes[1].style.color='red';
                            }

                            document.getElementsByClassName('what-next-button')[0].style.display='block';
                            document.getElementById("check_button_inside").disabled = false;
                        },10000);
                    },500);

                }
            });
    }

}
//--------------------------------------------------
// function on submitting the form for channel search

function searchChannel(channelId) {
    var channel_type=document.getElementById('channel_name').value;
    if(channel_type=='youtube'){


    }
    else if(channel_type=='instagram'){
        // ready all code after if else is for instagram
        var channelName = document.getElementById('search_name').value;
        if(channelName.includes(" ")){
            document.getElementsByClassName('data-display')[0].style.display='none';
            document.getElementsByClassName('message')[0].style.display='flex';
            document.getElementsByClassName('errorMessage')[0].childNodes[1].innerText='Username cannot contain spaces';

            setTimeout(function(){
                document.getElementsByClassName('message')[0].style.display='none';
                document.getElementsByClassName('errorMessage')[0].childNodes[1].innerText='';
            },3000);
            return false;
        }
        if(channelName==''){
            document.getElementsByClassName('data-display')[0].style.display='none';
            document.getElementsByClassName('message')[0].style.display='flex';
            document.getElementsByClassName('errorMessage')[0].childNodes[1].innerText='Username cannot be empty';

            setTimeout(function(){
                document.getElementsByClassName('message')[0].style.display='none';
                document.getElementsByClassName('errorMessage')[0].childNodes[1].innerText='';
            },3000);
            return false;
        }

        var influencer_name;
        var influencer_image;
        var total_followers;
        var average_views;
        var average_likes;
        var average_comments ;
        document.getElementById('loader-div').style.display='block';
        $.ajax({
                type: 'GET',
                url: "/getInstgramUserFromInstagramApi/"+channelName,
                success:function(res){
                    if(res.results.length==0){
                        document.getElementById("check_button_inside").disabled = false;
                        document.getElementById('loader-div').style.display='none';
                        document.getElementsByClassName('message')[0].style.display='flex';
                        document.getElementsByClassName('errorMessage')[0].childNodes[1].innerText='Cannot Get Data For This User';

                        setTimeout(function(){
                            document.getElementsByClassName('message')[0].style.display='none';
                            document.getElementsByClassName('errorMessage')[0].childNodes[1].innerText='';
                        },3000);
                        return;
                    }
                    document.getElementById('loader-div').style.display='none';
                    data=res.results;
                    console.log("hello");
                    console.log(data);
                    influencer_name=data[0].page_data.title;
                    business_category_name=data[0].page_data.business_category_name;
                    influencer_image=data[0].page_data.channel_img;
                    total_followers=data[0].page_data.no_of_followers;
                    var v = calcaulateAverage(data[0].post_data);
                    // engagement rate calculation
                    var engagementRate=0;
                    if((data[0].post_data).length!=0){
                        engagementRate=((v.avg_comments+v.avg_views+v.avg_likes)/(data[0].page_data.no_of_followers)).toFixed(2);
                    }
                    console.log(engagementRate);

                    //------------------------------
                    var score=calculateScore(data[0].page_data.no_of_followers,engagementRate);
                    var loc=window.location.href;
                    loc=loc.split('/');
                    console.log(loc);
                    loc=loc[loc.length-1];
                    if(loc=='influencer'){
                        if(score<4){
                        document.getElementsByClassName('score-4')[0].style.display="none";
                        document.getElementsByClassName('score-not-4')[0].style.display="block";
                        }
                        else{
                            document.getElementsByClassName('score-4')[0].style.display="block";
                            document.getElementsByClassName('score-not-4')[0].style.display="none";
                        }
                    }
                    console.log(score);
                    total_followers=convertion(total_followers);
                    average_views=convertion(v.avg_views);
                    average_likes=convertion(v.avg_likes);
                    average_comments=convertion(v.avg_comments);
                    if(average_comments==0){
                        average_comments='N/A';
                    }
                    if(average_likes==0){
                        average_likes='N/A';
                    }
                    if(average_views==0){
                        average_views='N/A';
                    }
                    document.getElementsByClassName('message')[0].style.display='none';
                    document.getElementsByClassName('data-display')[0].style.display='block';
                    document.getElementsByClassName('influencer-name')[0].childNodes[1].innerText=influencer_name;
                    document.getElementsByClassName("influence-img")[0].childNodes[1].src=influencer_image;
                    document.getElementsByClassName("influence-rating")[0].childNodes[1].innerText=engagementRate+'%';
                    document.getElementsByClassName("influence-followers")[0].childNodes[1].innerText=total_followers;
                    document.getElementsByClassName("influence-average-views")[0].childNodes[1].innerText=average_views;
                    document.getElementsByClassName("influence-average-likes")[0].childNodes[1].innerText=average_likes;
                    document.getElementsByClassName("influence-average-comments")[0].childNodes[1].innerText=average_comments;
                    console.log();
                    var label=[];
                    var like=[];
                    if(isEmpty(data[0].post_data)){
                        document.getElementsByClassName("chart-mine")[0].style.display="none";
                    }
                    else{
                        document.getElementsByClassName("chart-mine")[0].style.display="block";
                        for(var j=0;j<data[0].post_data.length&&j<5;j++){
                            label.push((data[0].post_data[j].post_time).substring(0,10));
                            like.push(data[0].post_data[j].no_of_post_likes);
                        }
                        getChart(label,like);
                    }
                    var influencerItem = document.getElementsByClassName("influence-rating");
                    var engagementBar = document.getElementsByClassName('engagement-bar');
                    var max=4;
                    var min=0.5;
                    var diff=(max-min)/3;
                    for(var i =0;i<influencerItem.length;i++){
                        var value = parseFloat(influencerItem[i].innerText.split(' ')[0]);
                        if(value>=max){
                            engagementBar[i].childNodes[1].style.backgroundColor="rgb(0, 133, 15)";
                            engagementBar[i].childNodes[3].style.backgroundColor="rgb(0, 133, 15)";
                            engagementBar[i].childNodes[5].style.backgroundColor="rgb(0, 133, 15)";
                            engagementBar[i].childNodes[7].style.backgroundColor="rgb(0, 133, 15)";
                            engagementBar[i].childNodes[9].style.backgroundColor="rgb(0, 133, 15)";
                        }
                        else if(value<max&&value>max-diff){
                            engagementBar[i].childNodes[1].style.backgroundColor="rgb(96, 165, 55)";
                            engagementBar[i].childNodes[3].style.backgroundColor="rgb(96, 165, 55)";
                            engagementBar[i].childNodes[5].style.backgroundColor="rgb(96, 165, 55)";
                            engagementBar[i].childNodes[7].style.backgroundColor="rgb(96, 165, 55)";
                            engagementBar[i].childNodes[9].style.backgroundColor="lightgrey";
                        }
                        else if(value<=max-diff&&value>min+diff){
                            engagementBar[i].childNodes[1].style.backgroundColor="rgb(129, 212, 82)";
                            engagementBar[i].childNodes[3].style.backgroundColor="rgb(129, 212, 82)";
                            engagementBar[i].childNodes[5].style.backgroundColor="rgb(129, 212, 82)";
                            engagementBar[i].childNodes[7].style.backgroundColor="lightgrey";
                            engagementBar[i].childNodes[9].style.backgroundColor="lightgrey";
                        }
                        else if(value<=min+diff&&value>min){
                            engagementBar[i].childNodes[1].style.backgroundColor="rgb(230, 169, 0)";
                            engagementBar[i].childNodes[3].style.backgroundColor="rgb(230, 169, 0)";
                            engagementBar[i].childNodes[5].style.backgroundColor="lightgrey";
                            engagementBar[i].childNodes[7].style.backgroundColor="lightgrey";
                            engagementBar[i].childNodes[9].style.backgroundColor="lightgrey";
                        }
                        else if(value<=min){
                            engagementBar[i].childNodes[1].style.backgroundColor="rgb(204,0,0)";
                            engagementBar[i].childNodes[3].style.backgroundColor="lightgrey";
                            engagementBar[i].childNodes[5].style.backgroundColor="lightgrey";
                            engagementBar[i].childNodes[7].style.backgroundColor="lightgrey";
                            engagementBar[i].childNodes[9].style.backgroundColor="lightgrey";
                        }
                    }


                    setTimeout(function () {

                        document.getElementsByClassName('score-display-name')[0].childNodes[1].innerText='Your Influencer Score Is';
                        $('html,body').animate({
                                scrollTop: $(".data-display").offset().top},
                            'slow');
                        var progressbar = $('#progress_bar');
                        max = progressbar.attr('aria-valuemax');
                        time = 100;
                        value = 0;
                        numberValue=0;
                        var loading = function () {
                            value += 2;
                            numberValue=Math.floor((value/2)/5);
                            document.getElementById('progress_bar').style.width=value+'%';
                            document.getElementsByClassName('score-display-number')[0].childNodes[1].innerText=numberValue;
                            document.getElementsByClassName('score-display-name')[0].childNodes[1].innerText='Calculating Your Score';
                            if(value<20){
                                document.getElementById('progress_bar').style.backgroundColor='red';
                                document.getElementsByClassName('score-display-number')[0].childNodes[1].style.color='red';
                            }
                            else if(value>=20&&value<=30){
                                document.getElementById('progress_bar').style.backgroundColor='orange';
                                document.getElementsByClassName('score-display-number')[0].childNodes[1].style.color='orange';
                            }
                            else if(value>30&&value<=40){
                                document.getElementById('progress_bar').style.backgroundColor='yellow';
                                document.getElementsByClassName('score-display-number')[0].childNodes[1].style.color='yellow';
                            }
                            else if(value>40&&value<=50){
                                document.getElementById('progress_bar').style.backgroundColor='limegreen';
                                document.getElementsByClassName('score-display-number')[0].childNodes[1].style.color='limegreen';
                            }
                            else{
                                document.getElementById('progress_bar').style.backgroundColor='rgb(80, 181, 30)';
                                document.getElementsByClassName('score-display-number')[0].childNodes[1].style.color='rgb(80, 181, 30)';
                            }
                            if(value>=100){
                                value=0;
                                numberValue=0;
                                document.getElementById('progress_bar').style.width='0%';
                                document.getElementById('progress_bar').style.backgroundColor='limegreen';
                            }
                        };
                        var animate = setInterval(function () {
                            loading();
                        }, time);
                        setTimeout(function () {
                            clearInterval(animate);
                            document.getElementById('progress_bar').style.width=(score*10)+'%';
                            document.getElementsByClassName('score-display-number')[0].childNodes[1].innerText=score;
                            document.getElementsByClassName('score-display-name')[0].childNodes[1].innerText='Your Influencer Score Is';
                            if(score>5){
                                document.getElementById('progress_bar').style.backgroundColor='green';
                                document.getElementsByClassName('score-display-number')[0].childNodes[1].style.color='green';
                            }
                            else if(score>4){
                                document.getElementById('progress_bar').style.backgroundColor='limegreen';
                                document.getElementsByClassName('score-display-number')[0].childNodes[1].style.color='limegreen';
                            }
                            else if(score>3){
                                document.getElementById('progress_bar').style.backgroundColor='yellow';
                                document.getElementsByClassName('score-display-number')[0].childNodes[1].style.color='yellow';
                            }
                            else if(score>2){
                                document.getElementById('progress_bar').style.backgroundColor='orange';
                                document.getElementsByClassName('score-display-number')[0].childNodes[1].style.color='orange';
                            }
                            else{
                                document.getElementById('progress_bar').style.backgroundColor='red';
                                document.getElementsByClassName('score-display-number')[0].childNodes[1].style.color='red';
                            }

                            document.getElementsByClassName('what-next-button')[0].style.display='block';

                        },10000);
                    },500);

                }
            });

    }
    else if(channel_type=='twitter'){

    }


    return false;


}
