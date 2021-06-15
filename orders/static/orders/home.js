console.log('JS múkodik!')

const make_orderBtn = document.getElementById('make-order');
var data = {};
make_orderBtn.addEventListener('click', ()=>{

//    init üres data dict

    console.log('make order clicked')
    var elements = document.getElementsByClassName('meal_inline');
//    console.log(elements)
     Array.from(elements).map(
        (element) => {
//               console.log(element)
                var element_meal_db = element.getElementsByClassName('meal_db')[0];
                var element_meal_db_input = element_meal_db.getElementsByClassName('meal_db_input')[0];
                var element_meal_db_input_id = element_meal_db_input.getAttribute("id");
                var element_meal_db_input_val = parseInt(element_meal_db_input.value);
                if (element_meal_db_input_val > 0) {
                    data[element_meal_db_input_id]=element_meal_db_input_val;
                }

                console.log(" ID: "+element_meal_db_input_id + " val: " + element_meal_db_input_val );
                console.log(data)


        }
    );
});

const orderBtn = document.getElementById('confirm-order')

console.log(orderBtn)

orderBtn.addEventListener('click', ()=>{
    console.log('clicked')
//    img.setAttribute('class', 'w-100')
//    modalBody.prepend(img)
//
//    console.log(img.src)
//
//    reportForm.addEventListener('submit', e=>{
//        e.preventDefault()
//        const formData = new FormData()
//        formData.append('csrfmiddlewaretoken', csrf)
//        formData.append('name', reportName.value)
//        formData.append('remarks', reportRemarks.value)
//        formData.append('image', img.src)
//
//        $.ajax({
//            type: 'POST',
//            url: '/reports/save/',
//            data: formData,
//            success: function(response){
//                console.log(response)
//                handleAlerts('success', 'report created')
//                reportForm.reset()
//            },
//            error: function(error){
//                console.log(error)
//                handleAlerts('danger', 'ups... something went wrong')
//            },
//            processData: false,
//            contentType: false,
//        })
//    })
})