console.log('JS múkodik!')

const alertBox = document.getElementById('alert-box')
const handleAlerts = (type, msg) => {
    alertBox.innerHTML = `
        <div class="alert alert-${type}" role="alert">
            ${msg}
        </div>
    `
}

const orderForm = document.getElementById('order_form')
const csrf = document.getElementsByName('csrfmiddlewaretoken')[0].value
const orderBtn = document.getElementById('confirm-order')
var make_orderBtn = document.getElementById('make-order');

let order_sum = 0
let data = {};
let boxdb = 0
make_orderBtn.addEventListener('click', ()=>{
    console.log('Rendelés véglegesítése megnyomva!!');

    //SUM mező kinullázása:
    var sum_document = document.getElementById('sum');
    sum_document.innerHTML = "Nincs rendelés!"

    //LI lista kinullázása:
    var myList = document.getElementById('mylist');
    myList.innerHTML = '';

    //Változók lista kinullázása:
    order_sum = 0
    data = {}
    boxdb = 0

    var elements = document.getElementsByClassName('meal_inline');

    Array.from(elements).map(
        (element) => {
                boxdb = 0
                // név kiszedése a labelből
                var element_meal_label = element.getElementsByClassName('col-form-label')[0];
                var element_meal_label_value = element_meal_label.innerHTML;

                // ID és darabszám
                var element_meal_db = element.getElementsByClassName('meal_db')[0];
                var element_meal_db_input = element_meal_db.getElementsByClassName('meal_db_input')[0];
                var element_meal_db_input_id = element_meal_db_input.getAttribute("id");
                var element_meal_db_input_val = parseInt(element_meal_db_input.value);

                //DOBOZOK
                var checkedValue = 0;
                var inputElements = element.getElementsByClassName('meal_box_1')[0];
                if (inputElements) {
                        if(inputElements.checked){
                            checkedValue += 50;
                            boxdb = boxdb + 1;
                        }
                }
                var inputElements = element.getElementsByClassName('meal_box_2')[0];
                if (inputElements) {
                        if(inputElements.checked){
                            checkedValue += 50;
                            boxdb = boxdb + 1;
                        }
                }

                // HA VAN DARABSZÁM, DATA és a LISTA feltöltése
                if (element_meal_db_input_val > 0) {
                    data[element_meal_db_input_id]=element_meal_db_input_val;
                    var meal_price = parseInt(element.getElementsByClassName('meal_price')[0].innerHTML);
                    var node = document.createElement("LI");
                    var textnode = document.createTextNode("ID: "+element_meal_db_input_id+" név: "+ element_meal_label_value+ " - " + element_meal_db_input_val+ " db"+" + " + element_meal_db_input_val*checkedValue + " Ft");
                    node.appendChild(textnode);
                    document.getElementById("mylist").appendChild(node);
                    order_sum += element_meal_db_input_val*(checkedValue+meal_price)
                }
        }
    );
    console.log('Rendelés véglegesítése megnyomva -> lefutott');
    if (order_sum > 0){
        var sum_document = document.getElementById('sum');
        sum_document.innerHTML = "Összesen: " + order_sum + " Ft"
    }
});

//RENDELÉS
orderBtn.addEventListener('click', e=>{
            e.preventDefault()
            console.log('Megrendelem! megnyomva!');
            console.log(data)
            console.log('submit')
            const formData = new FormData()
            formData.append('csrfmiddlewaretoken', csrf);
            formData.append('data', JSON.stringify(data));
            formData.append('boxdb', boxdb);
            $('#order-modal').modal('hide')
            $.ajax({
                type: 'POST',
                url: '/orders-new/',
                data: formData,
                success: function(response){
                    console.log(response)
                    handleAlerts('success', 'A megrendelésed rögzítésre került!')
                },
                error: function(error){
                    console.log(error)
                    handleAlerts('danger', 'Ups... Valami nem jóóó!')
                },
                processData: false,
                contentType: false,
            })
})

// TOGGLE BUTTON
$('.order-toggle').click(function(){
    alert(this.id);
    console.log(this.id + ' megnyomva!')
});