function getCampaignsAddedToMessage() {
        var message_id = $("#message_id").val();
        $.ajax({
            type: "GET",
            url: '/getCampaignsAddedToMessage/' + message_id,
            contentType: 'application/json;charset=UTF-8',
            success: function (data) {
                var myjson = JSON.stringify(data);
                $("#campaignNameList").empty();
                $("#proposal_campaign_name").empty();
                $("#tab-proposal .tab-list").empty();
                $('#proposal_campaign_name').append('<option value=""></option>');
                jQuery.each(data.results, function (i, val) {
                    var status = val.status;
                    var cname = textShortcut(val.campaign_name, 16);

                    var proposal = '<li><a href="#" data-message-id="' + val.message_id + '" data-campaign-id="' + val.campaign_id + '" class="get-proposal">' + cname + '<a/> <div class="actions-icons-container"><span><a href="#" class="danger"><i class="fa fa-remove"></i></a></span></div></li>';

                    if($('body').attr('id') == "influencer-view"){
                        var proposal = '<li><a href="#" data-message-id="' + val.message_id + '" data-campaign-id="' + val.campaign_id + '" class="get-proposal">' + cname + '<a/> <div class="actions-icons-container"></div></li>';
                    }

                    if ($('#email-application').attr('data-email') == "true") {
                        if (val.status == 'Proposal Sent') {
                            status = 'Proposal Received';
                            proposal = '<li><a href="#" data-message-id="' + val.message_id + '" data-campaign-id="' + val.campaign_id + '" class="get-proposal">' + cname + '<a/> <div class="actions-icons-container"><span><a href="#" class="danger"><i class="fa fa-remove"></i></a></span> <span><a href="#" data-message-id="' + val.message_id + '" data-campaign-id="' + val.campaign_id + '" data-status="Reject" data-toggle = "tooltip" title="Decline" class="accept-decline fa fa-thumbs-down red"></a></span> <span><a href="#" data-message-id="' + val.message_id + '" data-campaign-id="' + val.campaign_id + '" data-status="Accept" data-toggle = "tooltip" title="Accept" class="accept-decline fa fa-thumbs-up green"></a></span></div></li>';
                            if($('body').attr('id') == "influencer-view"){
                                proposal = '<li><a href="#" data-message-id="' + val.message_id + '" data-campaign-id="' + val.campaign_id + '" class="get-proposal">' + cname + '<a/> <div class="actions-icons-container"><span><a href="#" data-message-id="' + val.message_id + '" data-campaign-id="' + val.campaign_id + '" data-status="Reject" data-toggle = "tooltip" title="Decline" class="accept-decline fa fa-thumbs-down red"></a></span> <span><a href="#" data-message-id="' + val.message_id + '" data-campaign-id="' + val.campaign_id + '" data-status="Accept" data-toggle = "tooltip" title="Accept" class="accept-decline fa fa-thumbs-up green"></a></span></div></li>';
                            }
                        }else if(val.status != 'Current Partner'){
                            proposal = '';
                        }
                    }else{
                        if(val.status != 'Proposal Sent' && val.status != 'Current Partner'){
                            proposal = '';
                        }
                    }
                    $('#tab-proposal .tab-list').append(proposal);
                    $('#campaignNameList').append('<li class="text-bold-400 font-medium-1">' + val.campaign_name + ' <div class="text-bold-300 font-small-3">' + status + '</div></li>');
                    $('#proposal_campaign_name').append('<option value="' + val.campaign_id + '">' + val.campaign_name + '</option>');

                    $("#proposal_campaign_name").selectpicker('refresh');
                });
            }
        });
    }