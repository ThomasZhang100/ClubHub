
$(document).ready(function(){

    console.log(clubs['1'].clubname);

    function Ascending_sort(a, b) {
        return ($(b).text().toUpperCase()) < 
            ($(a).text().toUpperCase()) ? 1 : -1; 
    }

    $("#clubList li").sort(Ascending_sort).appendTo('#clubList');

    $("#filter").keyup(function(){
 
        // Retrieve the input field text and reset the count to zero
        var filter = $(this).val(), count = 0;
 
        // Loop through the comment list
        $("#clubList li").each(function(){
            
            console.log("loop")

            // If the list item does not contain the text phrase fade it out
            if ($(this).text().search(new RegExp(filter, "i")) < 0) {
                $(this).fadeOut();
            
            // Show the list item if the phrase matches and increase the count by 1
            } else {
                $(this).show();
                count++;
            }
        });
    });

    $("#clubList li").click(function(){
        var id = $(this).data("id");
        console.log(id);
        $(".club-title").text(clubs[id].clubname)
        $("#club-image").attr('src',staticURL+"/"+clubs[id].imgName)
        $("#club-mission").text(clubs[id].mission)
        $("#club-description").text(clubs[id].description)
        $("#clubIDSub").attr('value',id)
        $("#isFollow").attr('value',clubs[id].isFollowed)
        if (clubs[id].isFollowed==="true"){
            $("#submitButton").attr('value','Leave club')
            $("#submitButton").css('background-color','#f7f7f7')
            $("#submitButton").css('color','black')
            $("#buttonDesc").text('Club will removed from your calendar')
        }
        else{
            $("#submitButton").attr('value','Sign Up!')
            $("#submitButton").css('background-color','#0275d8')
            $("#submitButton").css('color','white')
            $("#buttonDesc").text('Club will be added to your calendar')
        }
    });
});