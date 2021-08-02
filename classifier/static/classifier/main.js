console.log('JS működik14')

const alertBox = document.getElementById('alert-box')
const handleAlerts = (type, msg) => {
    alertBox.innerHTML = `
        <div class="alert alert-${type}" role="alert">
            ${msg}
        </div>
    `
}

$("#mehet-button-div").hide();

$('.search_btn').click(function(){
    console.log(this.id + ' megnyomva!')
    let btn = document.getElementById('btn-holder');
    handleAlerts('success', 'Elindult a keresés!')
    btn.innerHTML = '<span>Keresés elindult, ~30 másodpercig fog tartani.</span>'
    $.ajax({
        type: 'GET',
        url: '/classifier/get_data/',
        data: '',
        success: function(response){
            $("#mehet-button-div").show();
            handleAlerts('success', 'Keresés lefutott.')
//             console.log(response);
             if (response['msg'] === false) {
                    console.log('nem siker')
             };
             if (response['msg'] === true) {
                    console.log(response['day_data']);
                    var day_datas = response['day_data'];
//                    console.log(Object.keys(day_datas));
                    var days = ["HETFO", "KEDD", "SZERDA", "CSÜTÖRTÖK", "PÉNTEK", "SZOMBAT"];
                    Array.from(days).map(
                        (day) => {
                        var day_str = String(day);
//                        console.log('Aktuális nap: ' + day_str);
//                        console.log(response['day_data'][day_str]);
                        var day_data = response['day_data'][day_str];
                        var date = day_data['date'];
                        var fozi_ar = day_data['fozi_ar'];
                        var fozi_nev = day_data['fozi_nev'];
                        var feltet_ar = day_data['feltet_ar'];
                        var feltet_nev = day_data['feltet_nev'];
                        var M1_leves = day_data['M1_leves'];
                        var M1_fo = day_data['M1_fo'];
                        var M2_leves = day_data['M2_leves'];
                        var M2_fo =day_data['M2_fo'];

                        day_table = document.getElementById(day_str);
                        var text_date = day_table.getElementsByClassName('date')[0];
                        text_date.value = date
                        var input_M1_leves_nev = day_table.getElementsByClassName('M1_leves_nev')[0];
                        input_M1_leves_nev.value = M1_leves
                        var input_M1_leves_ar = day_table.getElementsByClassName('M1_leves_ar')[0];
                        input_M1_leves_ar.value = 300
                        var input_M1_fo_nev = day_table.getElementsByClassName('M1_fo_nev')[0];
                        input_M1_fo_nev.value = M1_fo
                        var input_M1_fo_ar = day_table.getElementsByClassName('M1_fo_ar')[0];
                        input_M1_fo_ar.value = 700
                        var input_M2_leves_nev = day_table.getElementsByClassName('M2_leves_nev')[0];
                        input_M2_leves_nev.value = M2_leves
                        var input_M2_leves_ar = day_table.getElementsByClassName('M2_leves_ar')[0];
                        input_M2_leves_ar.value = 300
                        var input_M2_fo_nev = day_table.getElementsByClassName('M2_fo_nev')[0];
                        input_M2_fo_nev.value = M2_fo
                        var input_M2_fo_ar = day_table.getElementsByClassName('M2_fo_ar')[0];
                        input_M2_fo_ar.value = 800
                        var input_fozi_ar = day_table.getElementsByClassName('fozelek_ar')[0];
                        input_fozi_ar.value = fozi_ar
                        var input_fozi_nev = day_table.getElementsByClassName('fozelek_nev')[0];
                        input_fozi_nev.value = fozi_nev
                        var input_feltet_ar = day_table.getElementsByClassName('feltet_ar')[0];
                        input_feltet_ar.value = feltet_ar
                        var input_feltet_nev = day_table.getElementsByClassName('feltet_nev')[0];
                        input_feltet_nev.value = feltet_nev

                    });
              };
        },
        error: function(error){
            console.log(error)
            handleAlerts('danger', 'Ups... Valami nem jóóó!')
        },
        processData: false,
        contentType: false,
    });
});

$('.mehet').click(function(){
    var days = ["HETFO", "KEDD", "SZERDA", "CSÜTÖRTÖK", "PÉNTEK", "SZOMBAT"];
//    console.log(days);
    let day_data = {};
    let btn = document.getElementById('mehet');
    handleAlerts('success', 'Dolgozik a script!')
    btn.innerHTML = '<span>Dolgozik a szerver.</span>'
    Array.from(days).map(
        (day) => {
            let day_str = String(day);
//            console.log('Aktuális nap a visszaolvasáskor: ' + day_str);

            day_table = document.getElementById(day_str);
            var data_text_date = day_table.getElementsByClassName('date')[0].value;
            var data_M1_leves_nev = day_table.getElementsByClassName('M1_leves_nev')[0].value;
            var data_M1_leves_ar = day_table.getElementsByClassName('M1_leves_ar')[0].value;
            var data_M1_fo_nev = day_table.getElementsByClassName('M1_fo_nev')[0].value;
            var data_M1_fo_ar = day_table.getElementsByClassName('M1_fo_ar')[0].value;
            var data_M2_leves_nev = day_table.getElementsByClassName('M2_leves_nev')[0].value;
            var data_M2_leves_ar = day_table.getElementsByClassName('M2_leves_ar')[0].value;
            var data_M2_fo_nev = day_table.getElementsByClassName('M2_fo_nev')[0].value;
            var data_M2_fo_ar = day_table.getElementsByClassName('M2_fo_ar')[0].value;
            var data_fozi_ar = day_table.getElementsByClassName('fozelek_ar')[0].value;
            var data_fozi_nev = day_table.getElementsByClassName('fozelek_nev')[0].value;
            var data_feltet_ar = day_table.getElementsByClassName('feltet_ar')[0].value;
            var data_feltet_nev = day_table.getElementsByClassName('feltet_nev')[0].value;

            day_data[day_str] = {
                'date': data_text_date,
                'fozi_ar': data_fozi_ar,
                'fozi_nev': data_fozi_nev,
                'feltet_ar': data_feltet_ar,
                'feltet_nev': data_feltet_nev,
                'M1_leves_nev': data_M1_leves_nev,
                'M1_leves_ar': data_M1_leves_ar,
                'M1_fo_nev': data_M1_fo_nev,
                'M1_fo_ar': data_M1_fo_ar,
                'M2_leves_nev': data_M2_leves_nev,
                'M2_leves_ar': data_M2_leves_ar,
                'M2_fo_nev': data_M2_fo_nev,
                'M2_fo_ar': data_M2_fo_ar
            };
            console.log(day_str+' adatai: ');
            console.log(day_data[day_str])
        }
    );
    handleAlerts('success', 'Adatok kigyűjtve a táblázatból!')
    const formData = new FormData();
    const csrf = document.getElementsByName('csrfmiddlewaretoken')[0].value;
    formData.append('csrfmiddlewaretoken', csrf);
    formData.append('data', JSON.stringify(day_data));
    $.ajax({
        type: 'POST',
        url: '/classifier/new_data/',
        data: formData,
        success: function(response){
            console.log(response)
            handleAlerts('success', 'Sikeresen bekerült az adatbázisba minden új étel!')
            let btn = document.getElementById('mehet-button-div');
            btn.innerHTML = ''
//            $("a[href='#top']").click(function() {
            $("html, body").animate({ scrollTop: 0 }, "slow");

//            });
//            $(window).scrollTop(0);
        },
        error: function(error){
            console.log(error)
            handleAlerts('danger', 'Ups... Valami nem jóóó! Az új adatok küldése során a szerver csúnyaságot válaszolt.')
        },
        processData: false,
        contentType: false,
    });
});
