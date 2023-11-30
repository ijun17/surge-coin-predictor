const html_box = document.querySelector(".box");
const html_date = document.querySelector(".date");
const html_evaluation = document.querySelector(".evaluation");

function html(type,innerHTML){
    let html_div = document.createElement(type)
    html_div.innerHTML = innerHTML
    return html_div
}

function addList(text){
    html_box.append(html("div",text))
}

function addListFirst(text){
    html_box.prepend(html("div",text))
}

function clearList(){
    html_box.innerHTML=""
}


html_date.innerHTML = `update ${DATE}`
html_evaluation.innerHTML = `정확도: ${ACCURACY}<br>정밀도: ${PRECISION}`

for(let coin of coins){
    const UP = y_pred[coin][0]==1
    const color_pred=UP?"red":"black"
    const text_pred=UP?"상승":"하락"
    let text = `<span class="upbit-link">${coin}</span> <span style="color:${color_pred}";>내일 ${text_pred}</span><br> `
    for(let i=0; i<Math.min(20,y_pred[coin].length); i++){
        let color;
        if(i<M)color="purple"
        else if(y_pred[coin][i] != y_true[coin][i])color="gray"
        else if(y_pred[coin][i]==1)color ="red"
        else color = "blue"

        let symbol = (y_pred[coin][i]==1 ? "▲" : "▼")
        text+=`<span style="color:${color};">${symbol}<span>`
    }
    if(UP)addListFirst(text)
    else addList(text)
}

document.addEventListener("click",(event)=>{
    if(event.target.classList.contains("upbit-link")){
        // window.location.href = 'https://upbit.com/exchange?code=CRIX.UPBIT.'+event.target.innerText;
        window.open('https://upbit.com/exchange?code=CRIX.UPBIT.'+event.target.innerText);
    }
})