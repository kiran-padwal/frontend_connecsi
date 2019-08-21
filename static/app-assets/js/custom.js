$(window).bind('beforeunload',function(){
     document.getElementById('loader-div').style.display="block";

});



function submitNewClassifiedAdd(val){
//alert('inside');
     if(valueClassified <= 0){
        document.getElementsByClassName('content-wrapper')[0].style.filter='blur(3px)';
        document.getElementsByClassName('content-wrapper')[0].style.pointerEvents='none';
        document.getElementsByClassName('subscription-message')[0].style.display="block";
        document.getElementById('subscription-message-close').style.display='block';
     }
     else{

//    document.getElementById('loader-div').style.display="block";
        $.ajax({
            type:'GET',
            url:'/getClassified/'+val,
            success:function(data){
//                alert(data['data'][0]);
                classifiedData=data['data'][0]

                var max_upper=classifiedData['max_upper_followers']
                var min_lower=classifiedData['min_lower_followers']
                var video_cat_id=classifiedData['video_cat_id']
                delete classifiedData['video_cat_id']
                delete classifiedData['classified_id']
                delete classifiedData['posted_date']
                delete classifiedData['user_id']
                delete classifiedData['no_of_replies']
                delete classifiedData['no_of_views']
                delete classifiedData['deleted']
                delete classifiedData['min_lower_followers']
                delete classifiedData['max_upper_followers']
                classifiedData['max_upper']=(max_upper);
                classifiedData['min_lower']=(min_lower);
                classifiedData['video_cat']=video_cat_id;
                classifiedData['convert_to_campaign']='FALSE'

//document.getElementById('loader-div').style.display="block";
                $.ajax({
                    type:'POST',
                    url:'/saveClassifiedAds',
                    data:classifiedData,
                    success:function(data1){
//                        document.getElementById('loader-div').style.display="block";
                        window.location='/viewAllClassifiedAds'

                    }
                })
            }
        })
     }

}

function showMultipleMenu(val){
        if($('#delete-option'+val)[0].style.display=="none"){
            $('#delete-option'+val).fadeToggle('100');

            setTimeout(function(){
                $('#edit-option'+val).fadeToggle('100');
            },200);
            setTimeout(function(){
                $('#copy-option'+val).fadeToggle('100');
            },400);
        }
        else{

            $('#copy-option'+val).fadeToggle('100');
            setTimeout(function(){
                $('#edit-option'+val).fadeToggle('100');
            },200);
            setTimeout(function(){
                $('#delete-option'+val).fadeToggle('100');

            },400);
        }
}




$(document).ready(function () {

//    ashish code starts
$('#count1').change(function(){
    console.log("yes");
    console.log($('#count1').val())
    document.getElementById('price1').value=$('#count1').val();
    document.getElementById('totalPrice').innerHTML=$('#count1').val();
    document.getElementById('total_amount').innerHTML=$('#count1').val();
    document.getElementById('total_units').innerHTML=$('#count1').val();

})



    $('[data-toggle="tooltip"]').on('click', function () {
    $(this).tooltip('hide')
})
$('#upgrade-button').click(function(){
    $('.subscription-popup').fadeIn("slow");

})
$('#subscription-close').click(function(){
    $('.subscription-popup').fadeOut("slow");
})

$('#subscription-message-close').click(function(){
    $('.subscription-message').fadeOut("slow");
})
$('#customSubButton').click(function(){
    console.log("clicked on custom button")
})

$('#upgradeSubButton').click(function(){
    console.log("clicked on upgrade button")
})




    var influencerItem = document.getElementsByClassName('engagement-col');
      var engagementBar = document.getElementsByClassName('engagement-bar');
      var max=4;
      var min=0.5;
      var diff=(max-min)/3;
      for(var i =0;i<influencerItem.length;i++){
            var value = parseFloat(influencerItem[i].childNodes[5].innerText.split(' ')[0]);
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

    document.getElementById('loader-div').style.display="none";
// ends

    setTimeout(function(){
        $('body').removeClass('loading');
    }, 2000);

    var sum = function (a, b) {
        return a + b
    };

    function showNextQuote(items, index) {
        ++index;
        items.eq(index % items.length).fadeIn(2000).delay(2000).fadeOut(2000, function () {
            showNextQuote(items, index);
        });
    }

    function textShortcut(text, length){
        if (text.length > length) {
            return text.substr(0, length) + '...';
        }

        return text;
    }

    function hasAttr($obj, $name) {
        if (undefined !== $obj.attr($name) && $obj.attr($name).length > 0) {
            return true;
        }
        return false;
    }

    function check(Form_Name, password, confirm_password) {
        var pass1 = document.getElementById(password).value;
        var pass2 = document.getElementById(confirm_password).value;
        <!--alert(pass1);-->
        if (pass2 != pass1) {
            <!--M.toast({html: 'Password Doesnt Match.'})-->
            alert("Password Doesnt Match")
            return false;
        }
    }

    function readURL(input) {
        if (window.File && window.FileList && window.FileReader) {

            var files = event.target.files; //FileList object
            var output = document.querySelector(".displayFiles");

            for (var i = 0; i < files.length; i++) {
                var file = files[i];
                //Only pics
                if (!file.type.match('image')) continue;

                var picReader = new FileReader();
                picReader.addEventListener("load", function (event) {
                    var picFile = event.target;
                    $('.displayFiles').append("<img class='width-68 mr-1 my-1' src='" + picFile.result + "'" + "title='" + file.name + "'/>");
                });
                //Read the image
                picReader.readAsDataURL(file);
                $('#profile_pic').css('display', 'none');

            }
        } else {
            console.log("Your browser does not support File API");
        }
    }

    function readURLProfile(input) {
        if (input.files && input.files[0]) {
            var reader = new FileReader();
            reader.onload = function(e) {
                $(".displayFilesProfile").empty();
                $(".displayFilesProfile").append('<img id="filePreview" src="'+e.target.result+'" class=" img-border img-fluid width-150" alt="Card image">');
            }
            reader.readAsDataURL(input.files[0]);
        }
    }

   $('a').on('click', function(event){
     if($(this).attr('href')==undefined){
         return;
     }
     if($(this).attr('href').charAt(0)!="#"){
         if(($(this).attr('target'))||($(this).attr('download')!=undefined)){
             document.getElementById('loader-div').style.display="none";
         }
         else{
             document.getElementById('loader-div').style.display="block";
         }
     }
     else{
         document.getElementById('loader-div').style.display="none";
     }
     if(event.ctrlKey){
         document.getElementById('loader-div').style.display="none";
     }
 });


    $('button').on('click', function(event){

        if($(this).attr('name')=="search_inf"){

                document.getElementById('loader-div').style.display="block";

        }
        if($(this).attr('id')=="btn-search-inf"){
            document.getElementById('loader-div').style.display="block";
        }
        if(event.ctrlKey){
            document.getElementById('loader-div').style.display="none";
        }
    });

    $('button').on('click', function(){
        var $this = $(this);
        var $clicked = false;

        if(hasAttr($this,'data-clicked')){
            if($this.attr('data-clicked')=="true"){
                $clicked = true
            }
        }

        if($clicked == false){
            $this.attr('data-clicked', 'true');
            console.log('click');
            setTimeout(function(){
                console.log('click ready');
                $this.attr('data-clicked', 'false');
            }, 3000);
        }
    });

    $('input[type="submit"]').on('click', function(){
        var $this = $(this);
        var $clicked = false;

        if(hasAttr($this,'data-clicked')){
            if($this.attr('data-clicked')=="true"){
                $clicked = true
            }
        }
        if($clicked == false){
            $this.attr('data-clicked', 'true');
            console.log('click');
            setTimeout(function(){
                console.log('click ready');
                $this.attr('data-clicked', 'false');
            }, 3000);
        }
    });

    $('#profile_pic_fileinp').change(function () {
            $("#profile_pic").css("display","none");
//        alert('hello');
        readURLProfile(this);
    });

    $(document).on('change', 'input:file',function(){
        readURL(this);
        $(this).hide();
        $(".displayFiles").before('<input type = "file" name="campaign_files">');
    });



    function updateChannelStatusForCampaign(channel_id,campaign_id) {
        $.ajax({
            type: "GET",
            url: '/channel_status_for_campaign_by_channel_id_and_campaign_id/' + channel_id+'/'+campaign_id,
            contentType: 'application/json;charset=UTF-8',
            success: function (data) {
//                $('#status' + channel_id).find('.tab-content-item-list-container').empty();
//                $( '#status'+channel_id).empty();
                var $ul = $("<ul class='tab-content-item-list'></ul>");
                if (data.results.length != 0) {
                    jQuery.each(data.results, function (i, val) {
                        alert(val.campaign_name);
                        alert(val.status);
                        //$ul.append();
                        $ul.append($('<li>' + val.campaign_name + ' <span class="color1">' + val.status + '</span></li>'));
                        $('#status' + channel_id).find('.tab-content-item-list-container').append($ul);
                    });
                } else {
                    $ul.append($('<li>No Campaigns</li>'));
//                    $('#status' + channel_id).find('.tab-content-item-list-container').append($ul);
                }
            }
        });

    }



    //inbox
    // files and agreements
    function getMessageFiles(message_id){
        $.ajax({
            type: "GET",
            url: '/getMessageFiles/'+message_id,
            success: function(data)
            {
                jQuery.each(data.results, function(i, val) {
                    var message_files = val.message_files.split(",");
                    for(i=0;i<message_files.length;i++){
                        $('#tab-files .tab-list').append('<li><a class="file" href="../static/message_files/'+message_files[i]+'"><i class="fa fa-file"></i> ' + textShortcut(message_files[i], 16) + '</a> <div class="action-icons-container"><span data-toggle="tooltip" title="Download"><a href="../static/message_files/'+message_files[i]+'" download class="info"><img height="19px" width = "17px" src="../static/icons/download_icon.png"></a></span></div></li>');
                    }
                });
            }
        });
    }

    function getMessageAgreements(message_id){
        $.ajax({
            type: "GET",
            url: '/getMessageAgreements/'+message_id,
            success: function(data)
            {
                jQuery.each(data.results, function(i, val) {
                    var message_agreements = val.message_agreements.split(",");
                    for(i=0;i<message_agreements.length;i++){
                        $('#tab-agreements .tab-list').append('<li><a class="file" href="../static/message_agreements/'+message_agreements[i]+'" download><i class="fa fa-file"></i> '+textShortcut(message_agreements[i], 16)+'</a> <div class="action-icons-container"><span data-toggle="tooltip" title="Download"><a href="../static/message_agreements/'+message_agreements[i]+'" download class="info"><img height="19px" width = "17px" src="../static/icons/download_icon.png"></a></span></div></li>');
                    }
                });
            }
        });
    }

    $('#message_files_form').on('change', 'input:file',function(){
        readURL_files(this);
        //$('#message_files_form').submit();
         $('.file_message_input').hide();
         $(".displayMessageFiles").before('<label class="file_message_input btn btn-raised btn-primary bg-color1 w-100 custom-file-upload">Add File<input  type="file" name="message_files"  class="message_files"></label>');
    });

    function readURL_files(input) {
        if (input.files && input.files[0]) {
            var reader = new FileReader();
            reader.onload = function(e) {
                 $(".displayMessageFiles").after('<img id="messagefilesPreview" src="static/app-assets/img/portrait/avatars/avatar-08.png" class=" img-border gradient-summer width-50" alt="Card image">');
                 $('#messagefilesPreview').attr('src', e.target.result);
            }
            reader.readAsDataURL(input.files[0]);
        }
    }

    $('#message_agreements_form').on('change', 'input:file',function(){
        readURL_agreements(this);
       // $('#message_agreements_form').submit();
        $('.agreement_file_input').hide();
         $(".displayMessageAgreements").before('<label class="agreement_file_input btn btn-raised btn-primary bg-color1 w-100 custom-file-upload">Add Agreement<input  type="file" name="message_agreements"  class="message_agreements"></label>');

    });

    function readURL_agreements(input) {
        if (input.files && input.files[0]) {
            var reader = new FileReader();
            reader.onload = function(e) {
                 $(".displayMessageAgreements").after('<img id="messageagreementsPreview" src="static/app-assets/img/portrait/avatars/avatar-08.png" class=" img-border gradient-summer width-50" alt="Card image">');
                 $('#messageagreementsPreview').attr('src', e.target.result);
            }
            reader.readAsDataURL(input.files[0]);
        }
    }
    // files and agreements ends





    function replyMessage(from_email_id,subject,first_name) {
        <!--alert(channel_id);-->
//        alert('i m here');
        $("#reply_message_first_name").val(first_name);
        $("#to_email_id").val(from_email_id);
        $("#to_subject").val(subject);
    }

//    function getAllMappedChannel_ids(channel_id){
//        // alert(channel_id);
//        <!--alert('mapped = '+channel_id);-->
//        var $uniqid = Date.now();
//        var $var = "";
//        $.ajax({
//            type: "GET",
//            url: '/getMappedChannels/'+channel_id,
//            contentType: 'application/json;charset=UTF-8',
//            success: function(data)
//            {
//                $( '#proposal_channels').empty();
//                <!--$( '#twitter_channel_id').empty();-->
//                if (data.results.length != 0){
//                    jQuery.each(data.results, function(i, val) {
//                        // alert(val.youtube_channel_id);
//                        // alert(val.twitter_channel_id);
//                        $uniqid = $uniqid + 1;
//                        if(val.youtube_channel_id){
//                            <!--$( '#youtube_channel_id').val(val.youtube_channel_id);-->
//                            <!--$( '#youtube_channel_id').val('youtube');-->
//                            $var = '<div class="custom-control custom-control-inline-block custom-checkbox custom-control-inline text-left"><input checked type="checkbox" class="filled-in custom-control-input custom-control-input" multiple value="youtube@'+val.youtube_channel_id+'" name="proposal_channels" id="ch_youtube_id_'+$uniqid+'"><label class="custom-control-label campaignCheckbox" for="ch_youtube_id_'+$uniqid+'"><span data-toggle="tooltip" title="'+val.youtube_first_name+'"><a target="_blank" href="https://www.youtube.com/channel/'+val.youtube_channel_id+'" class="fa fa-youtube red"></a></span></label></div>';
//                            $("#proposal_channels").append($var);
//                        }
//                        if(val.twitter_channel_id){
//                            <!--$( '#twitter_channel_id').val(val.twitter_channel_id);-->
//                            <!--$( '#twitter_channel_id').val('twitter');-->
//                            $var = '<div class="custom-control custom-control-inline-block custom-checkbox custom-control-inline text-left"><input checked type="checkbox" class="filled-in custom-control-input custom-control-input" multiple value="twitter@'+val.twitter_channel_id+'" name="proposal_channels" id="ch_twitter_id_'+$uniqid+'"><label class="custom-control-label campaignCheckbox" for="ch_twitter_id_'+$uniqid+'"><span data-toggle="tooltip" title="'+val.twitter_first_name+'"><a target="_blank" href="#" class="fa fa-twitter"></a></span></label></div>';
//                            $("#proposal_channels").append($var);
//                        }
//
//                    });
//                }
//                else{
////                $('#status'+channel_id).append('<b>No Campaigns</b>');
//                alert('no channels mapped');
//                }
//            }
//        });
//
//    }

//    function getCampaignsAddedToMessage() {
//        var message_id = $("#message_id").val();
//        $.ajax({
//            type: "GET",
//            url: '/getCampaignsAddedToMessage/' + message_id,
//            contentType: 'application/json;charset=UTF-8',
//            success: function (data) {
//                var myjson = JSON.stringify(data);
//                $("#campaignNameList").empty();
//                $("#proposal_campaign_name").empty();
//                $("#tab-proposal .tab-list").empty();
//                $('#proposal_campaign_name').append('<option value=""></option>');
//                jQuery.each(data.results, function (i, val) {
//                    var status = val.status;
//                    var cname = textShortcut(val.campaign_name, 16);
//
//                    var proposal = '<li><a href="#" data-message-id="' + val.message_id + '" data-campaign-id="' + val.campaign_id + '" class="get-proposal">' + cname + '<a/> <div class="actions-icons-container"><span><a href="#" class="danger"><i class="fa fa-remove"></i></a></span></div></li>';
//
//                    if($('body').attr('id') == "influencer-view"){
//                        var proposal = '<li><a href="#" data-message-id="' + val.message_id + '" data-campaign-id="' + val.campaign_id + '" class="get-proposal">' + cname + '<a/> <div class="actions-icons-container"></div></li>';
//                    }
//
//                    if ($('#email-application').attr('data-email') == "true") {
//                        if (val.status == 'Proposal Sent') {
//                            status = 'Proposal Received';
//                            proposal = '<li><a href="#" data-message-id="' + val.message_id + '" data-campaign-id="' + val.campaign_id + '" class="get-proposal">' + cname + '<a/> <div class="actions-icons-container"><span><a href="#" class="danger"><i class="fa fa-remove"></i></a></span> <span><a href="#" data-message-id="' + val.message_id + '" data-campaign-id="' + val.campaign_id + '" data-status="Reject" data-toggle = "tooltip" title="Decline" class="accept-decline fa fa-thumbs-down red"></a></span> <span><a href="#" data-message-id="' + val.message_id + '" data-campaign-id="' + val.campaign_id + '" data-status="Accept" data-toggle = "tooltip" title="Accept" class="accept-decline fa fa-thumbs-up green"></a></span></div></li>';
//                            if($('body').attr('id') == "influencer-view"){
//                                proposal = '<li><a href="#" data-message-id="' + val.message_id + '" data-campaign-id="' + val.campaign_id + '" class="get-proposal">' + cname + '<a/> <div class="actions-icons-container"><span><a href="#" data-message-id="' + val.message_id + '" data-campaign-id="' + val.campaign_id + '" data-status="Reject" data-toggle = "tooltip" title="Decline" class="accept-decline fa fa-thumbs-down red"></a></span> <span><a href="#" data-message-id="' + val.message_id + '" data-campaign-id="' + val.campaign_id + '" data-status="Accept" data-toggle = "tooltip" title="Accept" class="accept-decline fa fa-thumbs-up green"></a></span></div></li>';
//                            }
//                        }else if(val.status != 'Current Partner'){
//                            proposal = '';
//                        }
//                    }else{
//                        if(val.status != 'Proposal Sent' && val.status != 'Current Partner'){
//                            proposal = '';
//                        }
//                    }
//                    $('#tab-proposal .tab-list').append(proposal);
//                    $('#campaignNameList').append('<li class="text-bold-400 font-medium-1">' + val.campaign_name + ' <div class="text-bold-300 font-small-3">' + status + '</div></li>');
//                    $('#proposal_campaign_name').append('<option value="' + val.campaign_id + '">' + val.campaign_name + '</option>');
//
//                    $("#proposal_campaign_name").selectpicker('refresh');
//                });
//            }
//        });
//    }

    $("#update_proposal_form").submit(function(e) {
                var edit_proposal_channels_boxes = $('.edit_proposal_channels_checkbox:checkbox');
                if(edit_proposal_channels_boxes.length > 0) {
                    if( $('.edit_proposal_channels_checkbox:checkbox:checked').length < 1) {
                        alert('Please select at least one Channel');
                        edit_proposal_channels_boxes[0].focus();
                        return false;
                    }
                }
                var edit_proposal_arrangements_boxes = $('.edit_proposal_arrangements_checkbox:checkbox');
                if(edit_proposal_arrangements_boxes.length > 0) {
                    if( $('.edit_proposal_arrangements_checkbox:checkbox:checked').length < 1) {
                        alert('Please select at least one Arrangement');
                        edit_proposal_arrangements_boxes[0].focus();
                        return false;
                    }
                }

                var edit_proposal_kpis_boxes = $('.edit_proposal_kpis_checkbox:checkbox');
                if(edit_proposal_kpis_boxes.length > 0) {
                    if( $('.edit_proposal_kpis_checkbox:checkbox:checked').length < 1) {
                        alert('Please select at least one Kpi');
                        edit_proposal_kpis_boxes[0].focus();
                        return false;
                    }
                }


        <!--alert('i m after');-->
        var form = $(this);
        var url = form.attr('action');
        $.ajax({
               type: "POST",
               url: url,
               async:false,
               data: form.serialize(), // serializes the form's elements.
               success: function(data)
               {
                   alert(data); // show response from the python script.
                   $('#editProposal').modal('toggle');
                   <!--getCampaignsAddedToMessage();-->
                   <!--window.location.reload();-->
               }
             });
        e.preventDefault(); // avoid to execute the actual submit of the form.
    });


    $(document).on('click', '.get-proposal', function(){
        getProposal($(this).attr('data-message-id'), $(this).attr('data-campaign-id'));
    });




//    $(document).on('click', '.accept-decline', function(){
//        accept_decline($(this).attr('data-message-id'), $(this).attr('data-campaign-id'), $(this).attr('data-status'));
//    });

    if($('#email-application').length){
        getCampaignsAddedToMessage();
        getMessageAgreements($('#message_id').val());
        getMessageFiles($('#message_id').val());
    }

    $(".list-group-item-url").on("click",function(e){
        if ($(this).hasClass('bg-lighten-5')) {
            e.preventDefault();
            $(".email-app-mail-content").removeClass("hide-email-content");
        }
    });

    $('.email-app-sidebar-toggle').on('click', function(e){
       e.preventDefault();
       $(this).toggleClass('active');
       $('.email-app-sidebar').toggleClass('hide');

    });

    $('.reply-message').on('click', function(e){
        e.preventDefault();
        e.stopPropagation();
        replyMessage($(this).attr('data-from-email-id'),$(this).attr('data-subject'),$(this).attr('data-first_name'));
        $($(this).attr('data-modal-target')).modal('toggle');
    });

    $('.delete-message').on('click', function(e){
        e.preventDefault();
        e.stopPropagation();
        var action_url = $(this).attr('data-location');
//        alert(action_url);
        $.ajax({
            type: "GET",
            url: action_url,
//            data: new FormData(form[0]),
//            cache: false,
//            contentType: false,
//            processData: false,
            success: function(data)
            {
                alert(data);
                window.location.reload();
            }
        });
    });

    $('.reply-message-sent').on('click', function(e){
        e.preventDefault();
        e.stopPropagation();
        window.location.href = $(this).attr('data-location');
    });

    $("#message_agreements_form").submit(function(e) {
        var form = $(this);
        var url = form.attr('action');
        $.ajax({
            type: "POST",
            url: url,
            data: new FormData(form[0]),
            cache: false,
            contentType: false,
            processData: false,
            success: function(data)
            {
                alert(data);
                window.location.reload();
            }
        });
        e.preventDefault(); // avoid to execute the actual submit of the form.
    });

    $("#message_files_form").submit(function(e) {
        var form = $(this);
        var url = form.attr('action');
        $.ajax({
            type: "POST",
            url: url,
            data: new FormData(form[0]),
            cache: false,
            contentType: false,
            processData: false,

            success: function(data)
            {
                alert(data);
                window.location.reload();
            }
        });
        e.preventDefault(); // avoid to execute the actual submit of the form.
    });

    $('.influencerMenu').each(function (index ) {
        $(this).click(function () {
            $(this).find("i").toggleClass("icon-reversed");
            var id = $(this).data('inf');
            $('#influencers-table').find('tr.'+id).toggle();
        });
    });

    $('.menu').each(function () {
       $(this).on('mouseenter mousemove',function () {
           $(this).find('.submenu').show();
       });

        $(this).mouseout(function () {
            $(this).find('.submenu').hide();
        });
    });

    $("#add_campaign_to_message").submit(function(e) {
        var form = $(this);
        var url = form.attr('action');
        $.ajax({
            type: "POST",
            url: url,
            data: form.serialize(), // serializes the form's elements.
            success: function(data)
            {
                alert(data);
                $('#campaignList').modal('toggle');
                <!--getCampaignsAddedToMessage();-->
                window.location.reload();
            }
        });
        e.preventDefault(); // avoid to execute the actual submit of the form.
    });

    $("#reply_message_form").submit(function(e) {
        var form = $(this);
        var url = form.attr('action');
        var channel_id = $('#reply_channel_id').val();
        $.ajax({
            type: "POST",
            url: url,
            <!--contentType: 'application/json;charset=UTF-8',-->
            data: form.serialize(), // serializes the form's elements.
            success: function(data)
            {
                alert(data);
                $('#replyMessage').modal('toggle');
                window.location.reload();
                <!--updateChannelStatusForCampaign(channel_id);-->
            }
        });
        e.preventDefault(); // avoid to execute the actual submit of the form.
    });

//    $("#sent_proposal_form").submit(function(e) {
//        var form = $(this);
//        var url = form.attr('action');
//        $.ajax({
//            type: "POST",
//            url: url,
//            data: form.serialize(), // serializes the form's elements.
//            success: function(data)
//            {
//                alert(data);
//                $('#proposal').modal('toggle');
//                <!--getCampaignsAddedToMessage();-->
//                window.location.reload();
//            }
//        });
//        e.preventDefault(); // avoid to execute the actual submit of the form.
//    });


    $("#sent_proposal_form").submit(function(e) {
//        alert('i m before');

                var proposal_channels_boxes = $('.proposal_channels_checkbox:checkbox');
                if(proposal_channels_boxes.length > 0) {
                    if( $('.proposal_channels_checkbox:checkbox:checked').length < 1) {
                        alert('Please select at least one Channel');
                        proposal_channels_boxes[0].focus();
                        return false;
                    }
                }
                var proposal_arrangements_boxes = $('.proposal_arrangements_checkbox:checkbox');
                if(proposal_arrangements_boxes.length > 0) {
                    if( $('.proposal_arrangements_checkbox:checkbox:checked').length < 1) {
                        alert('Please select at least one Arrangement');
                        proposal_arrangements_boxes[0].focus();
                        return false;
                    }
                }

                var proposal_kpis_boxes = $('.proposal_kpis_checkbox:checkbox');
                if(proposal_kpis_boxes.length > 0) {
                    if( $('.proposal_kpis_checkbox:checkbox:checked').length < 1) {
                        alert('Please select at least one Kpi');
                        proposal_kpis_boxes[0].focus();
                        return false;
                    }
                }


//        alert('i m after');
        var form = $(this);
        var url = form.attr('action');
        $.ajax({
               type: "POST",
               url: url,
               data: form.serialize(), // serializes the form's elements.
               success: function(data)
               {
                   alert(data); // show response from the python script.
                   $('#proposal').modal('toggle');
                   <!--getCampaignsAddedToMessage();-->
                   window.location.reload();
               }
             });
        e.preventDefault(); // avoid to execute the actual submit of the form.
    });

// backup code for proposal onchange ///

//    $("#proposal_campaign_name").on("change",function(){
////        alert('first here');
//        getAllMappedChannel_ids($(this).attr('data-channel-id'));
//        $("#proposal_description").empty();
//        $("#proposal_from_date").empty();
//        $("#proposal_to_date").empty();
//        $("#proposal_target_url").empty();
//        $("#proposal_arrangements").empty();
//        $("#proposal_kpis").empty();
//        var campaign_id = $("#proposal_campaign_name").val();
//        var $var = '';
//        var $uniqid = Date.now();
//
//        $.ajax({
//            type: "GET",
//            url: '/getCampaignDetails/'+campaign_id,
//            success: function(data)
//            {
//                jQuery.each(data.results, function(i, val) {
//
//                    $("#proposal_description").val(val.campaign_description);
//
//                    $("#proposal_from_date").val(val.from_date);
//
//                    $("#proposal_to_date").val(val.to_date);
//                    $("#proposal_target_url").val(val.target_url);
//
//                    var arrangements = val.arrangements.split(",");
//                    for(i=0;i<arrangements.length;i++){
//                        $uniqid = $uniqid + 1;
////                        $var = '<div class="custom-control custom-control-inline-block custom-checkbox custom-control-inline text-left"><input checked type="checkbox" class="filled-in custom-control-input custom-control-input" multiple value="'+arrangements[i]+'" name="proposal_arrangements" id="arrangements_id_'+$uniqid+'"><label class="custom-control-label campaignCheckbox" for="arrangements_id_'+$uniqid+'">'+arrangements[i]+'</label></div>';
////                        $("#proposal_arrangements").append($var);
//                        $("#proposal_arrangements").append('<input checked class="custom-control-inline proposal_arrangements_checkbox" multiple type ="checkbox" name="proposal_arrangements" value="'+arrangements[i]+'">'+arrangements[i]);
//                    }
//                    var kpis = val.kpis.split(",");
//                    for(i=0;i<kpis.length;i++){
//                        $uniqid = $uniqid + 1;
////                        $var = '<div class="custom-control custom-control-inline-block custom-checkbox custom-control-inline text-left"><input checked type="checkbox" class="filled-in custom-control-input custom-control-input" multiple value="'+kpis[i]+'" name="proposal_kpis" id="kpis_id_'+$uniqid+'"><label class="custom-control-label campaignCheckbox" for="kpis_id_'+$uniqid+'">'+kpis[i]+'</label></div>';
////                        $("#proposal_kpis").append($var);
//                           $("#proposal_kpis").append('<input checked class="custom-control-inline proposal_kpis_checkbox" multiple type ="checkbox" name="proposal_kpis" value="'+kpis[i]+'">'+kpis[i]);
//                    }
//
//                });
//
//            }
//        });
//    });

// backup code //

// ashish code proposal channel onchange //

$("#proposal_campaign_name").on("change",function(){
//        alert('first here');
        getAllMappedChannel_ids($(this).attr('data-channel-id'));
        $("#proposal_description").empty();
        $("#proposal_from_date").empty();
        $("#proposal_to_date").empty();
        $("#proposal_target_url").empty();
        $("#proposal_arrangements").empty();
        $("#proposal_kpis").empty();
        var campaign_id = $("#proposal_campaign_name").val();
        var $var = '';
        var $uniqid = Date.now();

        $.ajax({
            type: "GET",
            url: '/getCampaignDetails/'+campaign_id,
            success: function(data)
            {
                jQuery.each(data.results, function(i, val) {

                    $("#proposal_description").val(val.campaign_description);

                    $("#proposal_from_date").val(val.from_date);

                    $("#proposal_to_date").val(val.to_date);
                    $("#proposal_target_url").val(val.target_url);

                    var arrangements = val.arrangements.split(",");
                    for(i=0;i<arrangements.length;i++){
                        $uniqid = $uniqid + 1;
//                        $var = '<div class="custom-control custom-control-inline-block custom-checkbox custom-control-inline text-left"><input checked type="checkbox" class="filled-in custom-control-input custom-control-input" multiple value="'+arrangements[i]+'" name="proposal_arrangements" id="arrangements_id_'+$uniqid+'"><label class="custom-control-label campaignCheckbox" for="arrangements_id_'+$uniqid+'">'+arrangements[i]+'</label></div>';
//                        $("#proposal_arrangements").append($var);
                        $("#proposal_arrangements").append('<div class="custom-control custom-checkbox custom-control-inline"><input type="checkbox" checked id="proposal-arrangements-box-'+i+'" class="proposal_arrangements_checkbox filled-in custom-control-input custom-control-input"  multiple name="proposal_arrangements" value="'+arrangements[i]+'"><label class="custom-control-label campaignCheckbox" for="proposal-arrangements-box-'+i+'"></label><span>'+arrangements[i]+'</span></div>');
                    }
                    var kpis = val.kpis.split(",");
                    for(i=0;i<kpis.length;i++){
                        $uniqid = $uniqid + 1;
//                        $var = '<div class="custom-control custom-control-inline-block custom-checkbox custom-control-inline text-left"><input checked type="checkbox" class="filled-in custom-control-input custom-control-input" multiple value="'+kpis[i]+'" name="proposal_kpis" id="kpis_id_'+$uniqid+'"><label class="custom-control-label campaignCheckbox" for="kpis_id_'+$uniqid+'">'+kpis[i]+'</label></div>';
//                        $("#proposal_kpis").append($var);
                           $("#proposal_kpis").append('<div class="custom-control custom-checkbox custom-control-inline"><input type="checkbox" checked id="proposal-kpis-box-'+i+'" class="proposal_kpis_checkbox filled-in custom-control-input custom-control-input" multiple name="proposal_kpis" value="'+kpis[i]+'"><label class="custom-control-label campaignCheckbox" for="proposal-kpis-box-'+i+'"></label><span>'+kpis[i]+'</span></div>');
                    }

                });

            }
        });
    });
// ashish code end //


    $("#getCampaignsAddedToMessage").on("click",function(){
        getCampaignsAddedToMessage();
    });





    //endinbox

    $('.password-check').on('click', function(){
        var pass1 = document.getElementById('password').value;
        var pass2 = document.getElementById('confirm_password').value;
        <!--alert(pass1);-->
        if (pass2 != pass1) {
            <!--M.toast({html: 'Password Doesnt Match.'})-->
            alert("Password Doesnt Match")
            return false;
        }
    });

    $('.search-influencers').on('click', function(){
        $("#campaign_name").val($(this).attr('data-campaign-name'));
        $("#campaign_id").val($(this).attr('data-campaign-id'));
        $("#string_word").val($(this).attr('data-video-cat-name'));
        $("#min_lower").val($(this).attr('data-min-followers'));
        $("#max_upper").val($(this).attr('data-max-followers'));
        var country = $(this).attr('data-regions').split(',');
//        alert(country);
        $("#country").val(country[0]);
    });

//    $('.delete-fav-inf').on('click', function(e){
//    var channel_id = $(this).attr('data-channel-id');
//    var user_id = $(this).attr('data-user-id');
//
//    alert('i m in delete fav inf');
//
//        $.ajax({
//            type: "GET",
//            url: '/delFavInf/'+channel_id+'/'+user_id,
//            contentType: 'application/json;charset=UTF-8',
//            success: function(data)
//            {
//                location.reload();
//            }
//        });
//    });


    $('.create-alert').on('click', function(e){
//        alert($(this).attr('data-channel-id'));
        $("#create_alert_channel_id").val($(this).attr('data-channel-id'));
        $("#create_alert_channel_name").val($(this).attr('data-channel-name'));
        $("#total_followers").val($(this).attr('data-followers'));
        $("#total_views").val(0);
        $("#total_likes").val(0);
        $("#total_comments").val(0);
    });

//    $("#create_alert_form").submit(function (e) {
//        var form = $(this);
//        var url = form.attr('action');
//        var channel_id = $('#create_alert_channel_id').val();
//        $.ajax({
//            type: "POST",
//            url: url,
//            data: form.serialize(), // serializes the form's elements.
//            success: function (data) {
//                alert(data); // show response from the python script.
//                $('#create_alert_modal').modal('toggle');
//                getFavInfList();
//                <!--$( '#status'+channel_id).empty();-->
////                $( 'div[id*=alert]').empty();
//            }
//        });
//        e.preventDefault(); // avoid to execute the actual submit of the form.
//    });


$("#create_alert_form").submit(function (e) {
//        alert('i m here');
        var form = $(this);
        var url = form.attr('action');
        var channel_id = $('#create_alert_channel_id').val();
        var checkIf=$( '#alert'+channel_id)[0].childNodes[1].childNodes[1].childNodes[1].innerHTML;
//        alert(checkIf);
        if(checkIf=="No Alerts Set"){
//            alert('inside if');
//            alert(url);
            $.ajax({
                type: "POST",
                url: url,
                data: form.serialize(), // serializes the form's elements.
                success: function (data) {
//                    alert(data); // show response from the python script.
//                    alert(countAlerts);
                    countAlerts=countAlerts-1;
                    countAddToFavorites=countAddToFavorites-1;
                    $('#create_alert_modal').modal('toggle');
                    getFavInfList();
                }
            });
            e.preventDefault(); // avoid to execute the actual submit of the form.
        }
        else{
            console.log("nothing ji")
            $.ajax({
                type: "POST",
                url: '/createAlerts1',
                data: form.serialize(), // serializes the form's elements.
                success: function (data) {
                    alert(data); // show response from the python script.
                    $('#create_alert_modal').modal('toggle');
                    getFavInfList();
                    <!--$( '#status'+channel_id).empty();-->
    //                $( 'div[id*=alert]').empty();

                }
            });
            e.preventDefault(); // avoid to execute the actual submit of the form.
        }


    });



    $('.influencer-item').each(function () {
        if(hasAttr($(this), 'data-channel-id')) {
            //updateChannelStatusForCampaign($(this).attr('data-channel-id'));
        }
    });


    $('.analyse-result').each(function () {
//        if(hasAttr($(this), 'subscriber-count')) {
            //updateChannelStatusForCampaign($(this).attr('data-channel-id'));
            var res = abbrNum($(this).attr('data-integers'),2);
            $(this).text(res)
//            alert(res);
//        }
    });

    $('.send-message').on('click', function (e) {
//        alert('i m here');
        $("#message_channel_id").val($(this).attr('data-channel-id'));
        $("#to_email_id").val($(this).attr('data-business-email'));
        $("#title").val($(this).attr('data-title'));
//        $( "input.campaign_ids" ).prop('checked', false);
//        $( "input.campaign_ids" ).prop('disabled', false);
//        $("#campaign_channel_id").val($channel_id);
        var $channel_id = $(this).attr('data-channel-id');
//        alert($channel_id);
        var $channel_id = $channel_id.split('@');
        var $channel_id = $channel_id[0];
//        alert($channel_id);
        $('#message_campaign_id option').prop('disabled', false);
        $.ajax({
            type: "GET",
            url: '/getCampaignsAddedToMessageByChannelId/' + $channel_id,
            contentType: 'application/json;charset=UTF-8',
            success: function (data) {
                if (data.results.length != 0) {
                    jQuery.each(data.results, function (i, val) {
//                        if($('#campaign_id'+val.campaign_id).length){
//                            alert(val.campaign_id);
//                            alert(val.status);
                            if(val.status != 'Added'){
                                $('#message_campaign_id'+val.campaign_id).attr('disabled', true);
                            }
//                        }
                    });
                }
            }
        });
    });




    $('.add-to-campaign').on('click', function (e) {
        var $channel_id = $(this).attr('data-channel-id');
        $("input.campaign_id").prop('checked', false);
        $("input.campaign_id").prop('disabled', false);
        $("#youtube_channel_id").val($channel_id);
        $('input.campaign_id').each(function () {
            var $dccid = $(this).attr('data-campaign-channel-id');
            if ($dccid.indexOf($channel_id) !== -1) {
                $(this).attr('disabled', true);
            } else {
                $(this).attr('disabled', false);
            }
        });
    });





    $("#brand_report_form").submit(function(e) {
        var form = $(this);
        var url = form.attr('action');

        $.ajax({
            type: "POST",
            url: url,
            data: form.serialize(), // serializes the form's elements.
            success: function(data)
            {
                alert(data); // show response from the python script.
                $('#addReport').modal('toggle');
                location.reload();
                <!--updateChannelStatusForCampaign(channel_id);-->
            }
        });
        e.preventDefault(); // avoid to execute the actual submit of the form.
    });

    $("#edit_brand_report_form").submit(function(e) {
        var form = $(this);
        var url = form.attr('action');
        $.ajax({
            type: "POST",
            url: url,
            data: form.serialize(), // serializes the form's elements.
            success: function(data)
            {
                alert(data); // show response from the python script.
                $('#edit_brand_Report_modal').modal('toggle');
                location.reload();
                <!--updateChannelStatusForCampaign(channel_id);-->
            }
        });
        e.preventDefault(); // avoid to execute the actual submit of the form.
    });

//    $(window).lazyScript({
//        selectorClass: 'lazy',
//        callback: jQuery.noop,
//        threshold: 0,
//        scrollInterval: 500
//    });


    $('.filter-toggle').on('click touch', function (e) {
        e.preventDefault();
        if ($(this).hasClass('closed')) {
            $(this).removeClass('closed');
            $(this).closest('.card').find('.card-body').show();
        } else {
            $(this).addClass('closed');
            $(this).closest('.card').find('.card-body').hide();
        }
    });

    $("#team-members").addClass("disabledbutton");
    $(".noUi-handle").css("background-color", "white");
    $(".noUi-handle").css("height", "20px");
    $(".noUi-handle").css("width", "20px");
    $(".noUi-handle").css('border-radius', '100px');

    $("#btn-search-inf").click(function () {
        var min_lower = $(".noUi-handle-lower").text();
        var max_upper = $(".noUi-handle-upper").text();
        <!--alert(min_lower);-->
        <!--alert(max_upper);-->
        $("#min_lower").val(min_lower);
        $("#max_upper").val(max_upper);
    });

    $("#save").click(function () {
        var min_lower = $(".noUi-handle-lower").text();
        var max_upper = $(".noUi-handle-upper").text();
        <!--alert(min_lower);-->
        <!--alert(max_upper);-->
        $("#min_lower").val(min_lower);
        $("#max_upper").val(max_upper);
    });

    $(".users-list-padding a").on('click', function () {
        var href = $(this).attr('href');
        <!--alert(href);-->
        if (href != '#') {
            localStorage.setItem('messageHref', href);
        }
    });

    //search button click event
    $("#btn-search-inf").click(function () {
        var min_lower = $("#lower-value").text();
        var max_upper = $("#upper-value").text();
        <!--alert(min_lower);-->
        <!--alert(max_upper);-->
        $("#min_lower").val(min_lower);
        $("#max_upper").val(max_upper);
    });
    // search button click event ends

    $('[data-toggle="tooltip"]').tooltip();
    $('.nav-item a').filter(function () {
        return this.href == location.href
    }).parent().addClass('active').siblings().removeClass('active').parents("li").addClass('open');


    var selectedMessageHref = localStorage.getItem('messageHref');
    $("a[href$='" + selectedMessageHref + "']").addClass('bg-blue-grey bg-lighten-5');

    if ($('#donut-dashboard-chart').length) {
        //dashboard chart
        var $series = [];

        $('.chart-item').each(function(){
            $series.push({
                "name" : $(this).attr('data-name'),
                "className" : $(this).attr('data-class'),
                "value" : parseInt($(this).attr('data-value'))
                });
        });

        var Donutdata = {
            series: $series
        };

        var donut = new Chartist.Pie('#donut-dashboard-chart', {
            series: Donutdata.series
        }, {
            donut: true,
            startAngle: 0,
            labelInterpolationFnc: function (value) {
                var total = Donutdata.series.reduce(function (prev, series) {
                    return prev + series.value;
                }, 0);
                return total + '%';
            }
        });

        donut.on('draw', function (data) {
            if (data.type === 'label') {
                if (data.index === 0) {
                    data.element.attr({
                        dx: data.element.root().width() / 2,
                        dy: data.element.root().height() / 2
                    });
                } else {
                    data.element.remove();
                }
            }
        });
    }
    //dashboard tails
    $(".quotes").each(function () {
        var $items = $(this).find('.quote-item');
        showNextQuote($items, -1);
    });

    //searchinfluencers chart
//    $('.line-chart').each(function () {
//        var $this = $(this);
//        var $datasets = [];
//        var $items = [];
//        var $labels = [];
//
//        if (hasAttr($this, "data-labels")) {
//            $labels = $this.attr('data-labels').split(',').map(function (value) {
//                return value.trim();
//            });
//        }
//
//        if (hasAttr($this, "data-grafs")) {
//            $items = $this.attr('data-grafs').split(';').map(function (value) {
//                return value.trim();
//            });
//
//            $.each($items, function (key, value) {
//                if (value.trim().length > 0) {
//                    var $fields = value.split(':');
//                    var $data = [];
//                    $data = $fields[3].split(',').map(function (value) {
//                        return parseInt(value, 10);
//                    });
//                    $datasets.push({
//                        label: $fields[0].trim(),
//                        fill: true,
//                        backgroundColor: $fields[1].trim(),
//                        borderColor: $fields[2].trim(),
//                        borderCapStyle: 'butt',
//                        borderDash: [],
//                        borderWidth: 1,
//                        borderDashOffset: 0.0,
//                        borderJoinStyle: 'miter',
//                        pointBorderColor: "rgba(0,0,0,1)",
//                        pointBackgroundColor: "#fff",
//                        pointBorderWidth: 0.3,
//                        pointHoverRadius: 2,
//                        pointHoverBackgroundColor: "rgba(0,0,0,1)",
//                        pointHoverBorderColor: "rgba(0,0,0,1)",
//                        pointHoverBorderWidth: 1,
//                        pointRadius: 1,
//                        pointHitRadius: 10,
//                        data: $data,
//                    });
//                }
//            });
//        }
//
//        new Chart(document.getElementById($this.attr('id')), {
//            type: 'line',
//            data: {
//                labels: $labels,
//                datasets: $datasets
//            },
//            options: {
//                legend: {
//                    display: true,
//                },
//                scales: {
//                    yAxes: [{
//                        ticks: {
//                            beginAtZero: true
//                        }
//                    }]
//                }
//            }
//        });
//
//    });

    // range slider starts
    $('.sliderUI').each(function () {
        var $this = $(this);
        var $lv = $this.closest('.sliderContainer').find('.lower-value');
        var $uv = $this.closest('.sliderContainer').find('.upper-value');
        if ($lv.length > 0 && $uv.length > 0) {
            var keypressSlider = document.getElementById($this.attr('id'));
            var input0 = document.getElementById($lv.attr('id'));
            var input1 = document.getElementById($uv.attr('id'));
            var inputs = [input0, input1];
            noUiSlider.create(keypressSlider, {
                start: [parseInt(input0.value), parseInt(input1.value)],
                step: 10000,
                connect: true,
                //tooltips: [true, wNumb({ decimals: 1 })],
                range: {
                    'min': parseInt(input0.getAttribute('data-range')),
                    'max': parseInt(input1.getAttribute('data-range'))
                },
                format: {
                    from: function (value) {
                        return parseInt(value);
                    },
                    to: function (value) {
                        return parseInt(value);
                    }
                }
            });

            keypressSlider.noUiSlider.on('update', function (values, handle) {
                inputs[handle].value = values[handle];
            });

            function setSliderHandle(i, value) {
                var r = [null, null];
                r[i] = value;
                keypressSlider.noUiSlider.set(r);

            }

            inputs.forEach(function (input, handle) {

                input.addEventListener('change', function () {
                    setSliderHandle(handle, this.value);

                });

                input.addEventListener('keydown', function (e) {

                    var values = keypressSlider.noUiSlider.get();
                    var value = Number(values[handle]);

                    // [[handle0_down, handle0_up], [handle1_down, handle1_up]]
                    var steps = keypressSlider.noUiSlider.steps();

                    // [down, up]
                    var step = steps[handle];

                    var position;

                    // 13 is enter,
                    // 38 is key up,
                    // 40 is key down.
                    switch (e.which) {

                        case 13:
                            setSliderHandle(handle, this.value);
                            break;

                        case 38:

                            // Get step to go increase slider value (up)
                            position = step[1];

                            // false = no step is set
                            if (position === false) {
                                position = 1;
                            }

                            // null = edge of slider
                            if (position !== null) {
                                setSliderHandle(handle, value + position);
                            }

                            break;

                        case 40:

                            position = step[0];

                            if (position === false) {
                                position = 1;
                            }

                            if (position !== null) {
                                setSliderHandle(handle, value - position);
                            }

                            break;
                    }
                });
            });
        }
    });

    $('.tabs').on('click', '.tab', function (e) {
        e.preventDefault();
        var $this = $(this);
        $this.closest('.tabs').find('.tab').removeClass('active');
        $this.addClass('active');
        $this.closest('.tabs-container').find('.tabs-content-item').removeClass('active');
        $($this.find('a').first().attr('href')).addClass('active');
    });

    $("#saveclassified").click(function () {
        var min_lower = $("#lower-value").text();
        var max_upper = $("#upper-value").text();
        $("#min_lower").val(min_lower);
        $("#max_upper").val(max_upper);
    });

    $("#savecampaign").click(function () {
        var min_lower = $("#lower-value").text();
        var max_upper = $("#upper-value").text();
        $("#min_lower").val(min_lower);
        $("#max_upper").val(max_upper);
    });

    $('.datepicker').datepicker({
        format: 'yyyy-mm-dd',
        todayHighlight: true
    });

    $("#search_classifieds").submit(function(e) {
        var form = $(this);
        var url = form.attr('action');
        var min_lower = $("#lower-value").text();
        var max_upper = $("#upper-value").text();
        var min_lower_price = $("#lower-value-price").text();
        var max_upper_price = $("#upper-value-price").text();

        $("#min_lower").val(min_lower);
        $("#max_upper").val(max_upper);
        $("#min_lower_price").val(min_lower_price);
        $("#max_upper_price").val(max_upper_price);
        $('#classifiedData').empty();

        $.ajax({
            type: "POST",
            url: url,
            data: form.serialize(), // serializes the form's elements.
            success: function(data)
            {
                console.log(data);
            // <!--alert(data); // show response from the python script.-->
                jQuery.each(data.results, function(index, value) {
                    var file = value.files.split(",");
                    var channel = value.channels.split(",");
                    var fix_img = 'fixed_image.png';
                        $('#classifiedData').append('<div class="col-sm-6">' +
                            '<div class="card offers_item">' +
                            '<div class="card-header">' +
                            '<div class="row offers_item__header">' +
                            '<div class="col-6"><i class="ft ft-eye"></i> Views:</div>' +
                            '<div class="col-6 text-right"><i class="ft ft-calendar"></i> posted on:</div>' +
                            '</div>' +
                            '<div class="row offers_item__header">' +
                            '<div class="col-6">' + value.no_of_views + '</div>' +
                            '<div class="col-6 text-right">' + value.posted_date + '</div>' +
                            '</div>' +
                            '<div class="row">' +
                            '<div class="col-12">' +
                            '<div class="offers_item__title">'
                            + value.classified_name +
                            '</div>' +
                            '</div>' +
                            '</div>' +
                            '</div>' +

                            '<div class="card-body">' +

                            '<div class="row">' +
                            '<div class="col-xl-6 col-lg-12">' +
                            '<div class="row photo__row">' +
                            '<div class="col-12">' +
                            '<div class="main__image" style="background-image: url(static/campaign_files/' + file[0] + ')"></div>'+
                            '</div>' +
                            '</div>'+
                            '</div>'+

                            '<div class="col-xl-6 col-lg-12">' +
                            '<div class="row">' +
                            '<div class="col-12">' +
                            '<span>General Info:</span>' +
                            '</div>' +

                            '<div class="col-12">' +
                            '<div class="engagement">' +
                            '<div class="rating">' + value.min_lower_followers + ' - ' + value.max_upper_followers +
                            '</div>' +
                            '<div class="rating-txt">' + 'Followers' +
                            '</div>' +
                            '</div>' +
                            '</div>' +

                            '<div class="col-xl-12 col-lg-12">' +
                            '<div class="engagement">' +
                            '<div class="rating">' + value.budget +
                            '</div>' +
                            '<div class="rating-txt">' + value.currency +
                            '</div>' +
                            '</div>'+
                            '</div>' +
                            '</div>'+
                            '</div>'+
                            '</div>'+

                            '<div class="row">' +
                            '<div class="col-xl-6 col-lg-12">' +
                            '<div class="row">' +
                            '<div class="col-12">' +
                            '<span class="social">Channels: ' +
                            '<span class="facebook-' + index + '"></span>' +
                            '<span class="youtube-' + index + '">' +
                            '</span><span class="twitter-' + index + '">' +
                            '</span><span class="instagram-' + index + '">' +
                            '</span>' +
                            '</span>' +

                            '<hr>'+
                            '</div>' +

                            '<div class="col-12">' +
                            '<span>Content Type: </span>' +
                            '</div>' +

                            '<div class="col-12 arrangements__container">' +
                            '<div id="arrangements-' + index + '"></div>' +
                            '</div>'+
                            '</div>'+
                            '</div>'+
                            '<div class="col-xl-6 col-lg-12">' +
                            '<div class="row">' +
                            '<div class="col-12">' +
                            '<span>Categories: </span>' +
                            '</div>' +

                            '<div class="col-12 categories__container">' +
                            '<div id="cat-' + index + '" class="cat d-flex flex-wrap"></div>' +
                            '</div>' +
                            '</div>'+
                            '</div>'+
                            '</div>'+
                            '</div>'+

                            '<div class="card-footer">' +
                            '<div class="offers_item__footer">' +
                            '<div class="row d-flex align-items-center mt-2">' +
                            ' <div class="col-md-6 d-flex flex-row align-items-center">' +
                            (value.profile_pic != "" ? '<img src="/static/img/'+value.profile_pic+'" class="rounded offers_item__profile-thumb d-block" alt="Card image">' : '<img src="/static/img/'+fix_img+'" class="rounded offers_item__profile-thumb d-block" alt="Card image">') +
                            '<span>'+value.first_name + ' ' + value.last_name +'</span>'+
                            '</div>' +
                            ' <div class="col-md-6 text-right">' +
                            '<a  href="#"   class="reply-classified btn btn-raised btn-primary bg-color2 mt-0 mr-1 mb-0"'+
                                                   'data-business-email="'+value.email_id+'"'+
                                                   'data-title="'+value.first_name+'"'+
                                                   'data-backdrop="true" data-toggle="modal" data-target="#sendMessage">Reply</a>' +
                            '<a href="/viewClassifiedDetails/' + value.classified_id + '" class="btn btn-raised btn-primary bg-color1 mt-0 mb-0">Details</a>' +
                            '</div>' +
                            '</div>' +
                            '</div>' +
                            '</div>' +
                            '</div>' +
                            '</div>' +
                            '</div>');
                    $.each(this.channels.split(','), function (key, val) {
                        if (val === 'youtube') {
                            $(".youtube-" + index).append("<a href='#' class='fa fa-youtube-square'></a>");
                        }
                        if (val === 'instagram') {
                            $(".instagram-" + index).append("<a href='#' class='fa fa-instagram'></a>");
                        }
                        if (val === 'facebook') {
                            $(".facebook-" + index).append("<a href='#' class='fa fa-facebook-square'></a>");
                        }
                        if (val === 'twitter') {
                            $(".twitter-" + index).append("<a href='#' class='fa fa-twitter-square'></a>");
                        }
                    })
                    $.each(this.video_cat_name.split(','), function (key, val) {
                        $("#cat-" + index).append('<span class="offers_item__categories">' + val + '</span>');
                    })
                    $.each(this.arrangements.split(','), function (key, val) {
                        $("#arrangements-" + index).append('<span class="arrangement color1">' + val + ', </span>');
                    })
                    $('#classifiedData').show("slow");
                });
            }
        });
        e.preventDefault(); // avoid to execute the actual submit of the form.
    });


    $("#search_offers").submit(function (e) {
        var $this = $(this);
        var $clicked = $this.attr('data-clicked');
        var form = $(this);
        var url = form.attr('action');
        var min_lower = $("#lower-value").text();
        var max_upper = $("#upper-value").text();
        var min_lower_price = $("#lower-value-price").text();
        var max_upper_price = $("#upper-value-price").text();

        $("#min_lower").val(min_lower);
        $("#max_upper").val(max_upper);
        $("#min_lower_price").val(min_lower_price);
        $("#max_upper_price").val(max_upper_price);
        $('#offerData').empty();

        if($clicked == "false") {
        $this.attr('data-clicked', 'true');

        $.ajax({
            type: "POST",
            url: url,
            data: form.serialize(),
            dataType: "json"
        }).done(function (res) {
            $this.attr('data-clicked', 'false');
            $.each(res.results, function (index, value) {
                    var file = value.files.split(",");
                    var fix_img ="fixed_img.png";
                    $('#offerData').append('<div class="col-sm-6">' +
                        '<div class="card offers_item">' +
                        '<div class="card-header">' +
                        '<div class="row offers_item__header">' +
                        '<div class="col-6"><i class="ft ft-eye"></i> Views:</div>' +
                        '<div class="col-6 text-right"><i class="ft ft-calendar"></i> posted on:</div>' +
                        '</div>' +
                        '<div class="row offers_item__header">' +
                        '<div class="col-6">' + value.no_of_views + '</div>' +
                        '<div class="col-6 text-right">' + value.posted_date + '</div>' +
                        '</div>' +
                        '<div class="row">' +
                        '<div class="col-12">' +
                        '<div class="offers_item__title">'
                        + value.offer_name +
                        '</div>' +
                        '</div>' +
                        '</div>' +
                        '</div>' +

                        '<div class="card-body">' +

                        '<div class="row">' +
                        '<div class="col-xl-6 col-lg-12">' +
                        '<div class="row photo__row">' +
                        '<div class="col-12">' +
                        '<div class="main__image" style="background-image: url(static/offer_files/' + file[0] + ')"></div>' +
                        '</div>' +
                        '</div>' +
                        '</div>' +

                        '<div class="col-xl-6 col-lg-12">' +
                        '<div class="row">' +
                        '<div class="col-12">' +
                        '<span>General Info:</span>' +
                        '</div>' +

                        '<div class="col-12">' +
                        '<div class="engagement">' +
                        '<div class="rating">' + value.min_lower_followers + ' - ' + value.max_upper_followers +
                        '</div>' +
                        '<div class="rating-txt">' + 'Followers' +
                        '</div>' +
                        '</div>' +
                        '</div>' +

                        '<div class="col-xl-12 col-lg-12">' +
                        '<div class="engagement">' +
                        '<div class="rating">' + value.budget +
                        '</div>' +
                        '<div class="rating-txt">' + value.currency +
                        '</div>' +
                        '</div>' +
                        '</div>' +
                        '</div>' +
                        '</div>' +
                        '</div>' +

                        '<div class="row">' +
                        '<div class="col-xl-6 col-lg-12">' +
                        '<div class="row">' +
                        '<div class="col-12">' +
                        '<span class="social">Channels: ' +
                        '<span class="facebook-' + index + '"></span>' +
                        '<span class="youtube-' + index + '">' +
                        '</span><span class="twitter-' + index + '">' +
                        '</span><span class="instagram-' + index + '">' +
                        '</span>' +
                        '</span>' +

                        '<hr>' +
                        '</div>' +

                        '<div class="col-12">' +
                        '<span>Content Type: </span>' +
                        '</div>' +

                        '<div class="col-12 arrangements__container">' +
                        '<div id="arrangements-' + index + '"></div>' +
                        '</div>' +
                        '</div>' +
                        '</div>' +

                        '<div class="col-xl-6 col-lg-12">' +
                        '<div class="row">' +
                        '<div class="col-12">' +
                        '<span>Categories: </span>' +
                        '</div>' +

                        '<div class="col-12 categories__container">' +
                        '<div id="cat-' + index + '" class="cat d-flex flex-wrap"></div>' +
                        '</div>' +
                        '</div>' +
                        '</div>' +
                        '</div>' +
                        '</div>' +

                        '<div class="card-footer">' +
                        '<div class="offers_item__footer">' +
                        '<div class="row d-flex align-items-center mt-2">' +
                        ' <div class="col-md-6 d-flex flex-row align-items-center">' +
                        (value.channel_img != "" ? '<img src="'+value.channel_img+'" class="rounded offers_item__profile-thumb d-block" alt="Card image">' : '<img src="/static/img/'+fix_img+'" class="rounded offers_item__profile-thumb d-block" alt="Card image">') +
                        '<span>' + value.first_name + ' ' + value.last_name + '</span>' +
                        '</div>' +
                        ' <div class="col-md-6 text-right">' +
                        '<a  href="#"   class="reply-offer btn btn-raised btn-primary bg-color2 mt-0 mr-1 mb-0"'+
                                                   'data-business-email="'+value.email_id+'"'+
                                                   'data-title="'+value.first_name+'"'+
                                                   'data-backdrop="true" data-toggle="modal" data-target="#sendMessage" onclick="openMessage()">Reply</a>' +
                        '<a href="/viewOfferDetails/' + value.offer_id + '" class="btn btn-raised btn-primary bg-color1 mt-0 mb-0">Details</a>' +
                        '</div>' +
                        '</div>' +
                        '</div>' +
                        '</div>' +
                        '</div>' +
                        '</div>' +
                        '</div>');
                    $.each(this.channels.split(','), function (key, val) {
                        if (val === 'youtube') {
                            $(".youtube-" + index).append("<a href='#' class='fa fa-youtube-square'></a>");
                        }
                        if (val === 'instagram') {
                            $(".instagram-" + index).append("<a href='#' class='fa fa-instagram'></a>");
                        }
                        if (val === 'facebook') {
                            $(".facebook-" + index).append("<a href='#' class='fa fa-facebook-square'></a>");
                        }
                        if (val === 'twitter') {
                            $(".twitter-" + index).append("<a href='#' class='fa fa-twitter-square'></a>");
                        }
                    });
                    $.each(this.video_cat_name.split(','), function (key, val) {
                        $("#cat-" + index).append('<span class="offers_item__categories">' + val + '</span>');
                    });
                    $.each(this.arrangements.split(','), function (key, val) {
                        $("#arrangements-" + index).append('<span class="arrangement color1">' + val + ', </span>');
                    });
                    $('#offerData').show("slow");

                });
               });
        }

        e.preventDefault(); // avoid to execute the actual submit of the form.

    });

    $('select').selectpicker({
        dropupAuto: false
    });

    $('.slider-for').slick({
        slidesToShow: 1,
        slidesToScroll: 1,
        arrows: false,
        fade: false,
        asNavFor: '.slider-nav',
        infinite: true
    });

    $('.slider-nav').slick({
        slidesToShow: 5,
        slidesToScroll: 1,
        asNavFor: '.slider-for',
        dots: false,
        infinite: true,
        centerMode: true,
        focusOnSelect: true,
        swipeToSlide: true,
        swipe: true,
        variableWidth: true
    });

    $('.slick-next').on('click', function(e){
        e.preventDefault();
        $('.slider-nav').slick('slickNext');
    });

    $('.slick-prev').on('click', function(e){
        e.preventDefault();
        $('.slider-nav').slick('slickPrev');
    });


    if ($('#calendar').length){
        var $this = $('#calendar');
        var $items = [];
        var $events = [];

        if (hasAttr($this, "data-calendar")) {
            $items = $this.attr('data-calendar').split(';').map(function (value) {
                return value.trim();
            });
            $.each($items, function (key, value) {
                if (value.trim().length > 0) {
                    var $fields = value.split(':');
                    $events.push({title : $fields[0].trim(), start : $fields[1].trim(), end : $fields[2].trim(), color : $fields[3].trim()})
                }
            });
        }


        $('#calendar').fullCalendar({
            header:{},
            events: $events
        });
    }

    $('#alert').fadeOut('fast');

//    if($('textarea#email-message').length) {
//        tinymce.init({selector: 'textarea#email-message', branding: false});
//    }

    $('.add-campaign').on('click', function(e) {
        alert('imhere');
        var $channel_id = $(this).attr('data-channel-id');
        var $message_id = $(this).attr('data-message-id');
        $( "input.campaign_ids" ).prop('checked', false);
        $( "input.campaign_ids" ).prop('disabled', false);
        $("#campaign_channel_id").val($channel_id);

        $.ajax({
            type: "GET",
            url: '/getCampaignsAddedToMessageByChannelId/' + $channel_id,
            contentType: 'application/json;charset=UTF-8',
            success: function (data) {
                if (data.results.length != 0) {
                    jQuery.each(data.results, function (i, val) {
                        if($('#campaign_id'+val.campaign_id).length){
                            if(val.status != 'Added'){
                            $('#campaign_id'+val.campaign_id).attr('disabled', true);
                            }
                        }
                    });
                }
            }
        });
    });

    // $('.add-campaign').on('click', function(){
    //     var $channel_id = $(this).attr('data-channel-id');
    //     $("input.campaign_ids").prop('checked', false);
    //     $("input.campaign_ids").prop('disabled', false);
    //     $("#campaign_channel_id").val($channel_id);
    //     $('input.campaign_ids').each(function () {
    //         var $dccid = $(this).attr('data-campaign-channel-id');
    //         if ($dccid.indexOf($channel_id) !== -1) {
    //             console.log('true');
    //             $(this).attr('disabled', true);
    //         } else {
    //             console.log('false');
    //             $(this).attr('disabled', false);
    //         }
    //     });
    // });

    if($('.campaign-list-container').length > 0){
        $('.campaign-list-container').perfectScrollbar();
    }

    if($('.tab-content-item-list-container').length > 0){
        $('.tab-content-item-list-container').perfectScrollbar();
    }

    if($('.email-app-mail-content').length > 0){
        $('.email-app-mail-content').perfectScrollbar();
    }

    if($('.modal-body').length > 0){
        $('.modal-body').perfectScrollbar();
    }

    if($('.arrangements').length > 0){
        $('.arrangements').perfectScrollbar();
    }

    if($('.categories').length > 0){
        $('.categories').perfectScrollbar();
    }

    $('.reset-button').on('click', function(e){
        e.preventDefault();
        var $card = $(this).closest('.card');
        if($card.find('select').length > 0) {
            $card.find('select').val('default');
            $card.find('select').selectpicker("refresh");
        }
        if($card.find('.sliderUI').length > 0) {
            $card.find('.sliderUI').each(function(){
               var $id = $(this).attr('id');
               var $nouislider = document.getElementById($id);
                $nouislider.noUiSlider.reset();
            });

        }
    });


$(document.body).on('click','.reply-offer', function (e) {
        $("#message_channel_id").val($(this).attr('data-channel-id'));
        <!--alert('i m clicked');-->
        $("#to_email_id").val($(this).attr('data-business-email'));
        $("#title").val($(this).attr('data-title'));
    });

$('.update-and-send-email').on('click', function(e){
        var channel_id = $(this).attr('data-channel-id');
        var message_id = $(this).attr('data-message-id');
        var email_id = $('#'+channel_id).val();
        var subject = $(this).attr('data-subject');
        var message = $(this).attr('data-message');
//        alert(message);
//        alert(subject);
        if(email_id!='')
            if(confirm("Update and Send Email to "+email_id)){
                $.ajax({
                    type: "GET",
                    url: '/update_and_send_email_youtube/'+channel_id+'/'+message_id+'/'+email_id+'/'+subject+'/'+message,
                    contentType: 'application/json;charset=UTF-8',
                    success: function(data)
                    {
                        alert(data);
                        location.reload();
                    }
                });
            }
            else{
                return false;
            }
        else{
            alert('Please Enter Email Address !');
        }

    });

$("#add_insta_channel_form").submit(function(e) {
        var form = $(this);
        var url = form.attr('action');
        $.ajax({
            type: "POST",
            url: url,
            data: form.serialize(), // serializes the form's elements.
            success: function(data)
            {
                alert(data); // show response from the python script.
                $('#add_insta_modal_form').modal('toggle');
                location.reload();
            }
        });
        e.preventDefault(); // avoid to execute the actual submit of the form.
    });

getAllUnreadMessagesCount();


//        var $pageLoad = jQuery('#loader');
//        $pageLoad.hide();
//
//        jQuery(this).ajaxStart(function() {
//            $pageLoad.show("fast");
////            alert('start');
////            $('body').addClass('loading');
//        }).ajaxStop(function() {
//            $pageLoad.hide();
////            alert('stop');
////            $('body').removeClass('loading');
//        });



});
//$( document ).ajaxStart(function() {
//  $("#loader").hide();
//  $( "#loader" ).show();
//});

function goBack() {
        window.history.back();
    }

function abbrNum(number, decPlaces) {
    // 2 decimal places => 100, 3 => 1000, etc
    decPlaces = Math.pow(10,decPlaces);

    // Enumerate number abbreviations
    var abbrev = [ " K", " M", " B", " T" ];

    // Go through the array backwards, so we do the largest first
    for (var i=abbrev.length-1; i>=0; i--) {

        // Convert array index to "1000", "1000000", etc
        var size = Math.pow(10,(i+1)*3);

        // If the number is bigger or equal do the abbreviation
        if(size <= number) {
             // Here, we multiply by decPlaces, round, and then divide by decPlaces.
             // This gives us nice rounding to a particular decimal place.
             number = Math.round(number*decPlaces/size)/decPlaces;

             // Handle special case where we round up to the next abbreviation
             if((number == 1000) && (i < abbrev.length - 1)) {
                 number = 1;
                 i++;
             }

             // Add the letter for the abbreviation
             number += abbrev[i];

             // We are done... stop
             break;
        }
    }

    return number;
}



function getAllUnreadMessagesCount(){
         $.ajax({
               type: "GET",
               url: '/get_all_unread_messages',
               success: function(data)
               {
//                   alert(data); // show response from the python script.
//                   $('#myinbox').append('<span class="badge badge-pill badge-danger">{{glob.total_unread_messages}}</span>');
                   jQuery.each(data.results, function (i, val) {
//                        alert(i);
                        $('#myinbox').append('<span class="badge badge-pill badge-danger">'+val+'</span>');
                        $('#myinbox_left_side_nav').append('<span class="badge badge-pill badge-danger">'+val+'</span>');
                    });
               }
         });

}

$(document).ajaxStart(function(){
    document.getElementById('loader-div').style.display="block";
})
$(document).ajaxStop(function(){
    document.getElementById('loader-div').style.display="none";
})

function imageExists(image_url){
            var http = new XMLHttpRequest();
            http.open('HEAD', image_url, false);
            http.send();
            return http.status != 404;
        }

function loadingTop10Influencers(){
    var channel=document.getElementById('top10Influencer').value;
    $.ajax({
               type: "GET",
               url: '/getTop20Influencers/'+channel,
               success: function(data)
               {
                   value1=(data.results).slice(0,9);
                   var loop = $('#top10Influencertable')[0].childNodes[3].childNodes;
                   for( var i=1,j=0;i<loop.length;i=i+2,j++){
                        // calculating engagement rate
                        total = (value1[j]['total_100video_likes'] + value1[j]['total_100video_comments'] + value1[j]['total_100video_shares']);
//                        total = parseInt(Math.round(total/value1[j]['totalVideos']));
                        total = (total/value1[j]['subscriberCount_gained']);
//                        total = parseFloat(total.toFixed(4))*100;
                        total = total.toFixed(2) + ' '+'%';
                        if(!(value1[j].channel_img).includes('https')){
                            value1[j].channel_img=value1[j].channel_img.replace('http','https');
                        }
                        var status = imageExists(value1[j].channel_img);
                        if(status === true){
                            loop[i].childNodes[5].childNodes[0].src=value1[j].channel_img; // image set

                        }
                        else{
                            alert(loop[i].childNodes[5].childNodes[0].src)
                            loop[i].childNodes[5].childNodes[0].src='../static/img/fixed_image.png'; // image set
                            alert(loop[i].childNodes[5].childNodes[0].src)
                        }
                        loop[i].childNodes[7].childNodes[5].innerText=total;          // engagement rate set
//                        loop[i].childNodes[5].childNodes[0].src=value1[j].channel_img; // image set
                        loop[i].childNodes[5].childNodes[1].data=value1[j].title;      // name set
                        var image=loop[i].childNodes[5].childNodes[0];
                        var engagementRate=loop[i].childNodes[7].childNodes[5];
                        var name=loop[i].childNodes[5].childNodes[1].data;
                   }
                   // changing engagement bar color
                   var influencerItem = document.getElementsByClassName('engagement-col');
                        var engagementBar = document.getElementsByClassName('engagement-bar');
                        var max=4;
                        var min=0.5;
                        var diff=(max-min)/3;
                        for(var i =0;i<influencerItem.length;i++){
                            var value = parseFloat(influencerItem[i].childNodes[5].innerText.split(' ')[0]);
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
               }
         });
}



