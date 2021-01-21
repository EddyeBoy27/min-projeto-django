const pksList = [];

async function orderList(event) {
    const orderQnt = document.getElementById('carrinho-qntd');
    const pk = event.target.getAttribute('value');
    const pedIdLs = localStorage.getItem('pedidoId');
    const pedInstLs = localStorage.getItem(`pediInstId${pk}`);
    axios.defaults.xsrfCookieName = 'csrftoken';
    axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
    if (!pedIdLs) {
        const { data: { pedId, pedQnt } } = await axios.post(
            `http://127.0.0.1:8000/produtos/orders/add/${pk}/`,
        );
        localStorage.setItem('pedidoId', pedId);
        localStorage.setItem(`pediInstId${pk}`, JSON.stringify({
            pedQnt: pedQnt.aprinid,
            pkProd: pk
        }));
        pksList.push(pk);
    } else if (pedIdLs && !pksList.includes(pk)) {
        const { data: { pedQnt }} = await axios.post(
            `http://127.0.0.1:8000/produtos/orders/update/${pk}/`,
            { data: {
                'pedInst': JSON.parse(pedInstLs),
                'pediId': pedIdLs,
            }},
        )
        localStorage.setItem(`pediInstId${pk}`, JSON.stringify({
            pedQnt: pedQnt.aprinid,
            pkProd: pk
        }));
        pksList.push(pk);
    } else {
        await axios.put(
            `http://127.0.0.1:8000/produtos/orders/update/${pk}/`,
            { data: {
                'pedInst': JSON.parse(pedInstLs),
                'pediId': pedIdLs,
            }},
        );
        pksList.push(pk);
    }
    orderQnt.innerHTML = Number(orderQnt.innerHTML) + 1;
    localStorage.setItem('carrinho-qnt', orderQnt.innerHTML);
    return
}

async function increaseQnt({ target }) {
    const aprinid = target.getAttribute('value');
    const qntHTML = document.getElementById(`qnt-span${aprinid}`);
    const valHTML = document.getElementById(`val-span${aprinid}`);
    axios.defaults.xsrfCookieName = 'csrftoken';
    axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
    await axios.put(
        "http://127.0.0.1:8000/produtos/orders/update/",
        { data: { 'aprinid': aprinid, 'method': 'increase' } },
    );
    const updateResult = await axios.get(
        "http://127.0.0.1:8000/produtos/orders/update/",
        { data: { 'aprinid': aprinid } },
    );
    console.log(updateResult);
    const { data: { qnt, value }} = updateResult;
    qntHTML.innerHTML = qnt;
    valHTML.innerHTML = value;
    return
}

async function decreaseQnt({ target }) {
    const aprinid = target.getAttribute('value');
    const qntHTML = document.getElementById(`qnt-span${aprinid}`);
    const valHTML = document.getElementById(`val-span${aprinid}`);
    axios.defaults.xsrfCookieName = 'csrftoken';
    axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
    await axios.put(
        "http://127.0.0.1:8000/produtos/orders/update/",
        { data: { 'aprinid': aprinid, 'method': 'decrease' } },
    );
    const updateResult = await axios.get(
        "http://127.0.0.1:8000/produtos/orders/update/",
        { data: { 'aprinid': aprinid } },
    );
    const { data: { qnt, value }} = updateResult;
    qntHTML.innerHTML = qnt;
    valHTML.innerHTML = value;
    return
}

async function finishOrder(event) {
    const { target } = event;
    event.preventDefault();
    axios.defaults.xsrfCookieName = 'csrftoken';
    axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
    const pediId = localStorage.getItem('pedidoId');
    await axios.put(
        "http://127.0.0.1:8000/produtos/orders/done/",
        { data: { 'apediId': pediId } },
    );
    localStorage.clear();
    window.location.replace("http://127.0.0.1:8000/index/")
    return
}

window.onload = () => {
    const orderDefaultQnt = localStorage.getItem('carrinho-qnt') || 0;
    const carrinhoId = document.getElementById('carrinho-qntd');
    if (carrinhoId) {
        carrinhoId.innerHTML = orderDefaultQnt;
    }
}