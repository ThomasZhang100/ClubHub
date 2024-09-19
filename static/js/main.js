$(document).ready(function(){
    $("#0").css("display","block");
    var day = 0; 

    $('.back').click(function(){
        if (day>-32){
            $("#"+day).css("display","none");
            day--;
            $("#"+day).css("display","block");
        }
    });

    $('.eventRow').click(function(){
        var id = $(this).data("id");
        $("#eventPopup").modal('show');
        $(".club-title").text(eventDictJS[id].clubName)
        $("#event-subject").text(eventDictJS[id].eventSubject);
        $("#event-description").text(eventDictJS[id].eventDescription);
        $("#event-location").text(eventDictJS[id].eventLocation);
    });

    $('.forward').click(function(){
        if (day<32){
            $("#"+day).css("display","none");
            day++;
            $("#"+day).css("display","block");
        }
    });

    $('.today').click(function(){
        if (day!=0){
            $("#"+day).css("display","none");
            day=0;
            $("#"+day).css("display","block");
        }
    });

  });
  