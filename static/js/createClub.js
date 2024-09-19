$(document).ready(function(){
    $('#upload-create').change(function(){
      const file = this.files[0];
      var fileExtension = ['jpeg', 'jpg', 'png', 'gif', 'bmp'];
        if ($.inArray($(this).val().split('.').pop().toLowerCase(), fileExtension) == -1) {
            console.log("hi")
            alert("Only formats are allowed : "+fileExtension.join(', '));
        }
        else {
            if (file){
                let reader = new FileReader();
                reader.onload = function(event){
                  $('#imgClubMaker').css('background-image', 'url(' + event.target.result + ')');
                }
                reader.readAsDataURL(file);
            }
        }
    });

    $('#upload-edit').change(function(){
      const file = this.files[0];
      var fileExtension = ['jpeg', 'jpg', 'png', 'gif', 'bmp'];
        if ($.inArray($(this).val().split('.').pop().toLowerCase(), fileExtension) == -1) {
            console.log("hi")
            alert("Only formats are allowed : "+fileExtension.join(', '));
        }
        else {
            if (file){
                let reader = new FileReader();
                reader.onload = function(event){
                  $('#imgClubEditor').css('background-image', 'url(' + event.target.result + ')');
                }
                reader.readAsDataURL(file);
            }
        }
    });

    $(".editor-button").click(function(){
      var id = $(this).data("id");
      console.log(id);
      $("#editorModalLabel").text(clubs[id].clubname)
      $("#imgClubEditor").css('background-image','url(' + staticURL+"/"+clubs[id].imgName + ')')
      console.log('url(' + staticURL+"/"+clubs[id].imgName + ')')
      $("#club-name-edit").attr('value',clubs[id].clubname)
      $("#club-name-mission").text(clubs[id].mission)
      $("#club-name-description").text(clubs[id].description)
      $("#clubIDEdit").attr('value',id)
    });

    $(".scheduler-button").click(function(){
      var id = $(this).data("id");
      console.log(id);
      $("#schedulerModalLabel").text(clubs[id].clubname)
      $("#clubIDSchedule").attr('value',id)
    });
  });
  