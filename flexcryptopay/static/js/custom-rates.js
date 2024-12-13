function changeSource(ind) {
    let rate_inputs = document.getElementsByClassName("rates-cost-value");

    let sourceType = selectArray[ind].value;
    if (sourceType == "manual") {
        rate_inputs[ind].readOnly = false
        rate_inputs[ind].dataset.manual = "on"
        rate_inputs[ind].value = rate_inputs[ind].dataset.manual_rate;
    } else {
        delete rate_inputs[ind].dataset.manual
        rate_inputs[ind].readOnly = true
        getRealTRates(rate_inputs[ind].dataset.pairname.toLowerCase(), rate_inputs[ind]);
    }
}

function change_fee_policy(ind) {
    let percentArray = document.getElementsByClassName("percent-fee");
    let fixedArray = document.getElementsByClassName("fixed-fee");
    let policy = selectArray2[ind].value;
    switch (policy) {
        case "NO_FEE":
            percentArray[ind].style.display = "none";
            fixedArray[ind].style.display = "none";
            break;
        case "PERCENT_FEE":
            percentArray[ind].style.display = "block";
            fixedArray[ind].style.display = "none";
            break;
        case "FIXED_FEE":
            percentArray[ind].style.display = "none";
            fixedArray[ind].style.display = "block";
            break;
        case "PERCENT_OR_MINIMAL_FIXED_FEE":
            percentArray[ind].style.display = "block";
            fixedArray[ind].style.display = "block";
            break;
    }
}

function getRealTRates(pairName, currentRate) {
    console.log('--->',currentRate)
    //let currentCrypto = currentRate.dataset.pairname.replace("USDT", "").toUpperCase();
    let currentCrypto = pairName.replace("usdt", "").toUpperCase();
    console.log('--->',currentCrypto)
    let url = "/" + currentCrypto + "/get-rate";
    let http2 = new XMLHttpRequest();
    http2.onload = function(){
        let data = "";
        if(http2.status == 200)
        {
            data = JSON.parse(this.responseText);
        }
        if(data[currentCrypto] !== false)
        {
            currentRate.value = data[currentCrypto];
        }
    }

    http2.open("GET", url, true);
    http2.send();
}

let selectArray = document.getElementsByClassName("select-rate");
for (let i = 0; i < selectArray.length; i++) {
    selectArray[i].addEventListener("change", function () { changeSource(i); });
    changeSource(i);
}

let selectArray2 = document.getElementsByClassName("fee_policy_select");
for (let i = 0; i < selectArray2.length; i++) {
    selectArray2[i].addEventListener("change", function () { change_fee_policy(i); });
}

document.getElementById("all_fee_policy").addEventListener("change", function () {
    let per_fee = document.getElementById("percent-fee-for-all-container");
    let fix_fee = document.getElementById("fixed-fee-for-all-container");
    let all_pol_sel = document.getElementById('all_fee_policy')
    console.log(all_pol_sel.value);
    switch (all_pol_sel.value) {
        case "NO_FEE":
            per_fee.style.display = "none";
            fix_fee.style.display = "none";
            break;
        case "PERCENT_FEE":
            per_fee.style.display = "block";
            fix_fee.style.display = "none";
            break;
        case "FIXED_FEE":
            per_fee.style.display = "none";
            fix_fee.style.display = "block";
            break;
        case "PERCENT_OR_MINIMAL_FIXED_FEE":
            per_fee.style.display = "block";
            fix_fee.style.display = "block";
            break;
    }
});


document.getElementById("set-all").addEventListener("click", function (e) {
    e.preventDefault()
    let percent_fee_input_array = document.getElementsByClassName("percent-fee-value");
    let fixed_fee_input_array = document.getElementsByClassName("fixed-fee-value");
    let source_select_array = document.getElementsByClassName("rates-source-value");
    let policy_select_array = document.getElementsByClassName("fee_policy_select");

    console.log(policy_select_array)

    let percent_fee_input = document.getElementById("percent-fee-value-for-all");
    let fixed_fee_input = document.getElementById("fixed-fee-value-for-all");
    let source_select = document.getElementById("select-all");
    let policy_select = document.getElementById("all_fee_policy");

    for (let i = 0; i < source_select_array.length; i++) {
        console.log(i)
        percent_fee_input_array[i].value = percent_fee_input.value;
        fixed_fee_input_array[i].value = fixed_fee_input.value;
        source_select_array[i].value = source_select.value;
        policy_select_array[i].value = policy_select.value;

        changeSource(i)
        change_fee_policy(i)
    }
});

window.addEventListener('DOMContentLoaded', function () {
    let currentRates = document.getElementsByClassName("rates-cost-value");
    for (let i = 0; i < currentRates.length; i++) {
        let pairName = currentRates[i].dataset.pairname.toLowerCase();
        getRealTRates(pairName, currentRates[i]);
    }
});
