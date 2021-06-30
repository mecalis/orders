// TOGGLE BUTTON


$('.order-toggle').click(function(){
    var data = {'id': this.id }
    const csrf = document.getElementsByName('csrfmiddlewaretoken')[0].value
    console.log(this.id + ' megnyomva!')
    const formData = new FormData()
    formData.append('csrfmiddlewaretoken', csrf);
    formData.append('data', JSON.stringify(data));
    $.ajax({
                type: 'POST',
                url: '/order-toggle/',
                data: formData,
                success: function(response){
                    var id = '#' + response['id'];
                    console.log(response);
                     if (response['msg'] === 'FALSE') {

                        $(id).html("Beállítva: 'MÉG TARTOZÁS' Módosítás?");


                     };
                     if (response['msg'] === 'TRUE') {

                        $(id).html("Beállítva: 'KIFIZETTVE' Módosítás?");
                      };
                },


                error: function(error){
                    console.log(error)
//                    handleAlerts('danger', 'Ups... Valami nem jóóó!')
                },
                processData: false,
                contentType: false,
            })

});