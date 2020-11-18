const pksList = []

async function orderList(event) {
    const { target } = event;
    event.preventDefault();
    const bodyAppend = document.getElementById('aside-container');
    const pk = target.getAttribute('value');
    const qntValue = document.getElementById('order-qnt')
    const apediid = document.getElementById('apediid');
    let apiResult;
    axios.defaults.xsrfCookieName = 'csrftoken';
    axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
    if (!pksList.includes(pk)) {
        apiResult = await axios.post(
            `http://127.0.0.1:8000/produtos/orders/add/${pk}/`,
        );
        localStorage.setItem('apediid', apediid);
    } else if (pksList.includes(pk)) {
        const pedidoId = localStorage.getItem('apediid')
        const qntUpdate = await axios.post(`http://127.0.0.1:8000/produtos/orders/update/${pk}/`,
        { data: qntValue}
        );
    }
    // bodyAppend.innerHTML += apiResult.data;
    pksList.push(pk);
    return
}

async function increaseQnt({ target }) {
    return
}
