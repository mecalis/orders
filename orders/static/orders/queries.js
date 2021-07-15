var show_order_btn = document.getElementById("show-meals");
console.log("múkodj7!")

show_order_btn.addEventListener('click', ()=>{
    console.log('bent a lisenerben')
    var clipboard = new ClipboardJS('.show-meals', {
        text: function() {

//            var $copytext = document.getElementById("modal-to-copy").innerHTML.replace("<p>","");
            var $copytext = document.getElementById("modal-to-copy").innerText;
			return $copytext; // document.getElementById(savedID).innerHTML;

        }
    });

    clipboard.on('success', function(e) {
        console.log(e);
    });

    clipboard.on('error', function(e) {
        console.log(e);
    });


    try {
        var successful = document.execCommand('copy');
        var msg = successful ? 'successful' : 'unsuccessful';
        console.log('Copying text command was ' + msg);
    }
    catch (err) {
        console.log('Oops, unable to copy');
    }

})

var clipboard = new ClipboardJS('.menu-item_copy', {
        text: function() {

            var $copytext = "TESZT";
			return $copytext; // document.getElementById(savedID).innerHTML;

        }
    });

    clipboard.on('success', function(e) {
        console.log(e);
    });

    clipboard.on('error', function(e) {
        console.log(e);
    });