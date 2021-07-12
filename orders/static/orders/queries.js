var show_order_btn = document.getElementById("show-meals");
console.log("múkodj7!")

show_order_btn.addEventListener('click', ()=>{
    console.log('bent a lisenerben')

    d = $('#masolni').focus().select();
//    var copyText = document.querySelector("js-copytextarea");
//    copyText.focus();
//    copyText.select();
    console.log(d)

    try {
        var successful = document.execCommand('copy');
        var msg = successful ? 'successful' : 'unsuccessful';
        console.log('Copying text command was ' + msg);
    }
    catch (err) {
        console.log('Oops, unable to copy');
    }

})