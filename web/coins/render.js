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


html_date.innerHTML = `updated UTC ${DATE}`
html_evaluation.innerHTML = `정확도: ${ACCURACY} <br> 정밀도: ${PRECISION}(상승한다 예측했을때 실제로 상승한 비율)`

for(let coin of coins){
    let chart = ''
    let recentUP = false
    let lastUP = ''
    for(let i=0; i<40 && y_pred[coin][i]!=-1; i++){
        const UP = y_pred[coin][i]==1
        if(UP && !recentUP){
            lastUP = `<span style="color:red">${i}일전 상승을 예측했습니다</span>`
            recentUP = true
        }
        let color = UP ? "red" : "blue"
        let symbol = UP ? "▲" : "▼"
        chart+=`<span style="color:${color};">${symbol}<span>`
    }
    let text = `<span class="upbit-link">${coin}</span> ${lastUP}<br>${chart}`
    if(recentUP)addListFirst(text)
    else addList(text)
}

document.addEventListener("click",(event)=>{
    if(event.target.classList.contains("upbit-link")){
        window.open('https://upbit.com/exchange?code=CRIX.UPBIT.'+event.target.innerText);
    }
})