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
});