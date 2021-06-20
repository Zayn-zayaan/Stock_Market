const stocksBox = document.getElementById('stocks-box')
const spinnerBox = document.getElementById('spinner-box')
const loadBtn = document.getElementById('load-btn')
const loadBox = document.getElementById('loading-box')

// number of visible stock names on a load 
let visible = 5

// ajax request of getting the stocks data 
const handleGetData = () => {
    $.ajax({
        type: 'GET',
        url: `/stocks-json/${visible}`,
        success: function(response){
            max_size = response.max
            const data = response.data
            spinnerBox.classList.remove('not-visible')
            setTimeout(() => {
                spinnerBox.classList.add('not-visible')
                data.map(stock=>{
                    stocksBox.innerHTML += `<form method="post" action="/query">
                    <a href="${stock.Sno}/"<h6>${stock.title}</h6></a>
                    <input style="width:70%" class="query-input mt-3 form-control" type="text" placeholder="Ask a query..." name="askquery" id="askquery"
                      aria-label="Search">
                    <input class="form-control" type="hidden" name="stockname" id="stockname"
                      aria-label="Search" value="${stock.title}">
                    <button class="btn btn-outline-success my-2" type="submit">Ask</button>
                  </form><hr />`
                })
                if(max_size){
                    loadBox.innerHTML = "<h4>No more data to load...</h4><br /><br />"
                }
            }, 700)
        },
        error: function(error){
            console.log(error)
        } 
    })
}

handleGetData()

loadBtn.addEventListener('click', ()=>{
    visible += 5;
    handleGetData()
})