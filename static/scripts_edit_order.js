var total_price;
var count = document.querySelectorAll("#foodorder > li").length
var menuorder = true;
calTotal()
console.log(window.screen.width)
if (window.screen.availWidth < 896) {
    document.getElementById("order").style.display = "none"
}

function switchmenu() {
    var menu = document.getElementById("order")
    var order = document.getElementById("menu")
    if (menuorder == false) {
        menu.style.display = "none"
        order.style.display = ""
        menuorder = true

    } else {
        menu.style.display = ""
        order.style.display = "none"
        menuorder = false
    }

}

//ฟังก์ชันคำนวนราคามรวม และ เก็บรหัสเมนูอาหาร
function toData() {
    let text = ""
    let ul = document.querySelectorAll("#foodorder > li")
    let input;
    for (let i = 0; i < ul.length; i++) {
        input = ul[i].firstElementChild.nextSibling.nextSibling
        text += input.name + "=" + input.value + "&"
    }
    return text
}

function sendForm(button) {
    if (button.value === "sendorder"){
        if (!confirm("ต้องการจะส่งออเดอร์ใช่หรือไม่")){
            return 0;
        }
    }
    let save_data = toData()
    save_data += "action=" + button.value + "&order_foods=" + document.getElementById("order_foods").value
    console.log(save_data)
    var httpRequest = new XMLHttpRequest()
    httpRequest.onreadystatechange = function() {
        if (httpRequest.readyState === XMLHttpRequest.DONE) {
            if (httpRequest.status === 200) {
                let response = JSON.parse(httpRequest.responseText)
                console.log(response)
                notification(button.value)
            }
        }
    }
    console.log("Asd")
    console.log(button.getAttribute("order"))
    httpRequest.open('POST', '/work_in/save_order/' + button.getAttribute("order") + '/')
    httpRequest.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded')
    httpRequest.send(save_data)
}

function calTotal() {
    total_price = 0;
    let input_order_food = document.getElementById("order_foods")
    input_order_food.value = ""
    let inputs = document.getElementsByClassName("form-control")
    for (let i = 1; i < inputs.length; i++) {
        if (inputs[i].getAttribute("status") == "none") {
            input_order_food.value += inputs[i].getAttribute("name") + ","
        }
        total_price += inputs[i].value * Number(inputs[i].getAttribute("price"))
    }
    console.log(total_price)
    document.getElementById("total_price").innerHTML = total_price
    document.getElementById("form_total").value = total_price
}


function addtoOrder(list) {
    if (window.screen.availWidth < 896){
        switchmenu()
    }
    var order_ul = document.querySelectorAll("#foodorder > li")
    var have_menu = false
        //สำหรับบันทึกข้อมูล
    let text = ""
    let input

    //เพิ่มของเดิม
    for (i = 0; i < order_ul.length; i++) {
        input = order_ul[i].firstElementChild.nextSibling.nextSibling
        var status = input.getAttribute("status")
        text += "&" + input.name + "=" + input.value
        if ((list.getAttribute("value") == order_ul[i].firstElementChild.textContent) && (status == "none")) {

            var num = input.value
            input.value = parseInt(num) + 1
            have_menu = true
        }
    }
    save_data = text
        //สร้างใหม่
    if (have_menu == false) {
        ul = document.querySelector("#foodorder")
        li = document.createElement("li")
        li.className = "list-group-item d-flex justify-content-between align-items-center"
        li.innerHTML = '<div class="foodname p-1 flex-grow-1 bd-highlight">' + list.getAttribute("value") + '</div>'
        li.innerHTML = li.innerHTML + 'จำนวน : <input id="amount' + count + '"class="notsave form-control" status="none" price="' + list.getAttribute("price") + '" name="' + list.getAttribute("food-id") + '" style="width: 60px; margin-right: 10px; margin-left: 10px;" onchange="input_event(this)" type="number" value="1" min="0" max="999"/>'
        li.innerHTML = li.innerHTML + '<button type="button" class="btn btn-danger" onclick="deleteMenu(this)"><i class="fas fa-trash-alt"></i> ลบ</button><div class="changetosend p-1 bd-highlight alert alert-warning m-0 mr-1" style="display:none;"></div>'
        li.style.animation = "expand .25s ease-in-out"
        ul.appendChild(li)
        count = count + 1
    }
    calTotal()
}

function deleteMenu(menuname) {
    menuname.parentNode.remove()
    calTotal()
}

function input_event(input) {
    if (input.value <= 0) {
        deleteMenu(input)
    }
    calTotal()
}

function search_menu() {
    var input, filter, ul, li, a, i, txtValue;
    input = document.getElementById('foodname_input');
    filter = input.value.toUpperCase();
    ul = document.getElementById("foodmenu");
    li = ul.getElementsByTagName('li');

    for (i = 0; i < li.length; i++) {
        a = li[i].getElementsByClassName("foodname")[0];

        txtValue = a.textContent
        if (txtValue.toUpperCase().indexOf(filter) > -1) {
            li[i].parentNode.style.display = "";
        } else {
            li[i].parentNode.style.display = "none";
        }
    }
}
calTotal()

function notification(status) {
    var flex = document.getElementById("flex")
    var div = document.createElement("div")
    if (status == "save") {
        console.log(status)
        div.id = "notification"
        div.style.background = "#66BB6A"
        div.innerHTML =
            "<span style='font-size:50px;'><i class='fas fa-check-circle'></i></span> บันทึกข้อมูลออเดอร์เสร็จสิ้น"
        flex.appendChild(div)
        setTimeout(function() {
            document.getElementById("notification").style.opacity = "0"
        }, 2500);
        setTimeout(function() {
            document.getElementById("notification").remove()
        }, 4000);

    } else {
        div.id = "notification"
        div.style.background = "#BDE5F8"
        div.style.color = "#00529B"
        div.innerHTML =
            "<span style='font-size:50px;'><i class='fas fa-check-circle'></i></span> ส่งออเดอร์เรียบร้อย"
        flex.appendChild(div)
        setTimeout(function() {
            document.getElementById("notification").style.opacity = "0"
        }, 2500);
        setTimeout(function() {
            document.getElementById("notification").remove()
        }, 4000);
        document.getElementById("order_foods").value = ""
        updateorder()
    }

}

function updateorder() {
    var change = document.getElementsByClassName("notsave")
    var text = '<div class="p-1 bd-highlight alert alert-warning m-0 mr-1"><i class="fas fa-paper-plane"></i> เมนูถูกส่งแล้ว</div>'
    var num = document.getElementsByClassName("notsave").length
    var notsave = document.getElementsByClassName("notsave")
    for (i = 0; i < change.length; i++) {
        if (notsave[i].getAttribute("status") == "none") {
            console.log("true")
            notsave[i].disabled = true
            notsave[i].nextElementSibling.remove()
            notsave[i].nextElementSibling.innerHTML = '<i class="fas fa-paper-plane"></i> เมนูถูกส่งแล้ว'
            notsave[i].nextElementSibling.style.display = ""
            notsave[i].setAttribute("status", "false")
        }
    }
}