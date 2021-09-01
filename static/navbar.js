$(document).ready(function() {
//    console.log("Ready!2");
    $.ajax({
        type: 'GET',
        url: '/blog/blog-count/',
        data: '',
        success: function(response){
//             console.log('siker')
                var count = parseInt(response['count'])
//                console.log(count)
                if (count > 0) {
                    var span = document.getElementById('counter');
                    span.innerHTML = `
                        <span style="color: red;">
                            (${count})
                        </span>
                    `
                }
        },
        error: function(error){
            console.log(error)

        },
        processData: false,
        contentType: false,
     });

     $.ajax({
        type: 'GET',
        url: '/my-profile/get-daily-waiter/',
        data: '',
        success: function(response){
                console.log('siker');
                var last_waiter = response['last_waiter'];
                console.log(last_waiter);
                var span = document.getElementById('last_waiter');
                if (last_waiter) {
                    span.innerHTML = `
                        <span style="color: red;">
                            ${last_waiter}!
                        </span>
                    `
                }
                else {
                    span.innerHTML = 'Még nincs vállalkozó... :('
                }
        },
        error: function(error){
            console.log(error)

        },
        processData: false,
        contentType: false,
     });
});